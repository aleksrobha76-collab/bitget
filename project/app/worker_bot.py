from __future__ import annotations

import html
import logging
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import Conflict
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .auth import is_owner_account
from .config import Settings
from .storage import UserStorage


LOGGER = logging.getLogger(__name__)
APPLICATION_ACTION_PATTERN = re.compile(r"^worker_app:(accept|reject):(\d+):([A-Za-z0-9_]+)$")
AWAITING_RESUME_KEY = "awaiting_worker_resume"


RULES_TEXT = """Привет! Здесь можно оставить заявку на роль воркера.

Правила:
1. Не спамить клиентам.
2. Не обещать то, чего нет в условиях.
3. Работать только со своего Telegram username.

Пример резюме:
Имя: Иван
Опыт: 6 месяцев
Откуда трафик: TikTok / Telegram / личные контакты
Сколько времени готов уделять: 3-4 часа в день
Почему хотите работать: хочу развиваться и приводить клиентов

Отправьте резюме одним сообщением."""


async def _post_init(application: Application) -> None:
    await application.bot.delete_webhook(drop_pending_updates=True)


async def log_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    error = context.error
    if isinstance(error, Conflict):
        LOGGER.error(
            "Worker bot polling conflict: another process is already using this bot token."
        )
        return
    LOGGER.exception("Unhandled worker bot error", exc_info=error)


def build_worker_application(settings: Settings, storage: UserStorage) -> Application:
    application = (
        ApplicationBuilder()
        .token(settings.worker_bot_token)
        .post_init(_post_init)
        .build()
    )
    application.bot_data["settings"] = settings
    application.bot_data["storage"] = storage

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_application_action, pattern=APPLICATION_ACTION_PATTERN))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_resume))
    application.add_error_handler(log_error)

    return application


def _admin_keyboard(applicant_id: int, username: str) -> InlineKeyboardMarkup:
    payload = f"{applicant_id}:{username}"
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Принять", callback_data=f"worker_app:accept:{payload}"),
                InlineKeyboardButton("Отклонить", callback_data=f"worker_app:reject:{payload}"),
            ]
        ]
    )


def _format_applicant(user, resume: str) -> str:
    username = f"@{user.username}" if user.username else "без username"
    full_name = " ".join(
        part for part in (user.first_name, user.last_name) if part
    ) or "не указано"
    safe_resume = html.escape(resume.strip())
    return (
        "<b>Новая заявка воркера</b>\n\n"
        f"<b>Имя:</b> {html.escape(full_name)}\n"
        f"<b>Username:</b> {html.escape(username)}\n"
        f"<b>Telegram ID:</b> <code>{user.id}</code>\n\n"
        f"<b>Резюме:</b>\n{safe_resume}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    context.user_data[AWAITING_RESUME_KEY] = True
    await update.message.reply_text(RULES_TEXT)


async def handle_resume(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.message
    if user is None or message is None:
        return

    settings: Settings = context.application.bot_data["settings"]
    storage: UserStorage = context.application.bot_data["storage"]

    if is_owner_account(user.id, user.username, settings):
        await message.reply_text("Вы админ. Заявки воркеров будут приходить сюда на проверку.")
        return

    if not user.username:
        await message.reply_text(
            "Для заявки нужен Telegram username. Добавьте username в настройках Telegram и отправьте резюме ещё раз."
        )
        return

    existing_worker = storage.get_worker_by_username(user.username)
    if existing_worker is not None:
        await message.reply_text(
            f"Вы уже добавлены как воркер. Ваш код: {existing_worker['code']}."
        )
        return

    resume = (message.text or "").strip()
    if len(resume) < 20:
        context.user_data[AWAITING_RESUME_KEY] = True
        await message.reply_text("Напишите резюме чуть подробнее: опыт, источник трафика и сколько времени готовы работать.")
        return

    admin_ids = sorted(settings.admin_telegram_ids)
    if not admin_ids:
        await message.reply_text("Заявка заполнена, но ID админа пока не настроен. Напишите администратору напрямую.")
        LOGGER.warning("Worker application cannot be delivered: ADMIN_TELEGRAM_IDS is empty")
        return

    text = _format_applicant(user, resume)
    delivered = 0
    for admin_id in admin_ids:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=text,
                parse_mode="HTML",
                reply_markup=_admin_keyboard(user.id, user.username),
            )
            delivered += 1
        except Exception as exc:
            LOGGER.warning("Failed to deliver worker application to admin %s: %s", admin_id, exc)

    if delivered == 0:
        await message.reply_text("Не получилось отправить заявку админу. Попробуйте позже.")
        return

    context.user_data.pop(AWAITING_RESUME_KEY, None)
    await message.reply_text("Резюме отправлено админу. Ожидайте решение.")


async def handle_application_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    admin = update.effective_user
    if query is None or admin is None:
        return

    settings: Settings = context.application.bot_data["settings"]
    storage: UserStorage = context.application.bot_data["storage"]
    if not is_owner_account(admin.id, admin.username, settings):
        await query.answer("Нет доступа", show_alert=True)
        return

    match = APPLICATION_ACTION_PATTERN.fullmatch(query.data or "")
    if match is None:
        await query.answer("Некорректная заявка", show_alert=True)
        return

    action, applicant_id_raw, username = match.groups()
    applicant_id = int(applicant_id_raw)

    if action == "reject":
        await query.answer("Заявка отклонена")
        await query.edit_message_reply_markup(reply_markup=None)
        try:
            await context.bot.send_message(
                chat_id=applicant_id,
                text="Ваша заявка отклонена.",
            )
        except Exception as exc:
            LOGGER.warning("Failed to notify rejected applicant %s: %s", applicant_id, exc)
        return

    try:
        worker = storage.create_worker(username)
        admin_text = f"Воркер @{worker['username']} принят. Код: {worker['code']}."
        worker_text = (
            "Вас приняли. Ожидайте, админ свяжется с вами.\n"
            f"Ваш код воркера: {worker['code']}"
        )
    except ValueError as exc:
        existing_worker = storage.get_worker_by_username(username)
        if existing_worker is None:
            await query.answer(str(exc), show_alert=True)
            return
        admin_text = f"@{existing_worker['username']} уже есть в воркерах. Код: {existing_worker['code']}."
        worker_text = (
            "Вас приняли. Ожидайте, админ свяжется с вами.\n"
            f"Ваш код воркера: {existing_worker['code']}"
        )

    await query.answer("Принято")
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text(admin_text)
    try:
        await context.bot.send_message(chat_id=applicant_id, text=worker_text)
    except Exception as exc:
        LOGGER.warning("Failed to notify accepted applicant %s: %s", applicant_id, exc)
