from __future__ import annotations

import logging
import time
from typing import Any

import httpx


LOGGER = logging.getLogger(__name__)
BINANCE = "https://api.binance.com/api/v3"
COINBASE = "https://api.exchange.coinbase.com"
CACHE_TTL_SECONDS = 120
BINANCE_BLOCK_COOLDOWN_SECONDS = 3600
FALLBACK_PRICES = {
    "BTCUSDT": 104000.0,
    "ETHUSDT": 2600.0,
    "SOLUSDT": 175.0,
    "BNBUSDT": 680.0,
    "XRPUSDT": 2.2,
}

_INTERVAL_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "4h": 14400,
    "1d": 86400,
}

_price_cache: dict[str, tuple[float, dict[str, Any]]] = {}
_klines_cache: dict[tuple[str, str, int], tuple[float, list[dict[str, float]]]] = {}
_binance_blocked_until = 0.0


def _normalize_symbol(symbol: str) -> str:
    return (symbol or "BTCUSDT").strip().upper()


def _coinbase_product(symbol: str) -> str:
    if symbol.endswith("USDT"):
        return f"{symbol[:-4]}-USDT"
    if symbol.endswith("USDC"):
        return f"{symbol[:-4]}-USDC"
    return f"{symbol[:-3]}-{symbol[-3:]}"


def _cache_fresh(created_at: float) -> bool:
    return time.time() - created_at <= CACHE_TTL_SECONDS


def _fallback_price(symbol: str) -> float:
    return FALLBACK_PRICES.get(_normalize_symbol(symbol), FALLBACK_PRICES["BTCUSDT"])


def _binance_available() -> bool:
    return time.time() >= _binance_blocked_until


def _mark_binance_failure(exc: Exception) -> None:
    global _binance_blocked_until
    response = getattr(exc, "response", None)
    if getattr(response, "status_code", None) == 418:
        _binance_blocked_until = time.time() + BINANCE_BLOCK_COOLDOWN_SECONDS
        LOGGER.warning(
            "binance returned 418; skipping binance for %s seconds",
            BINANCE_BLOCK_COOLDOWN_SECONDS,
        )


async def _get_json(client: httpx.AsyncClient, url: str, **kwargs: Any) -> Any:
    last_error: Exception | None = None
    for attempt in range(2):
        try:
            response = await client.get(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as exc:  # pragma: no cover - network dependent
            last_error = exc
            _mark_binance_failure(exc)
            if attempt == 0:
                await _sleep_before_retry()
    raise RuntimeError(str(last_error)) from last_error


async def _sleep_before_retry() -> None:
    import asyncio

    await asyncio.sleep(0.25)


def _build_ticker_from_candles(symbol: str, candles: list[dict[str, float]]) -> dict[str, str]:
    last = candles[-1]
    first = candles[0]
    price = float(last["c"])
    open_price = float(first["o"]) or price
    change = ((price - open_price) / open_price) * 100 if open_price else 0.0
    high = max(float(item["h"]) for item in candles)
    low = min(float(item["l"]) for item in candles)
    volume = sum(float(item.get("v", 0.0)) for item in candles)
    return {
        "symbol": symbol,
        "price": f"{price:.8f}",
        "change": f"{change:.4f}",
        "high": f"{high:.8f}",
        "low": f"{low:.8f}",
        "volume": f"{volume:.8f}",
        "source": "fallback",
    }


def _synthetic_candles(price: float, limit: int) -> list[dict[str, float]]:
    now_ms = int(time.time() // 60 * 60 * 1000)
    candles: list[dict[str, float]] = []
    base = float(price)
    for index in range(limit):
        offset = index - limit + 1
        drift = base * offset * 0.00003
        wave = base * 0.0008 * ((index % 7) - 3) / 3
        open_price = base + drift - wave
        close_price = base + drift + wave
        high = max(open_price, close_price) * 1.0005
        low = min(open_price, close_price) * 0.9995
        candles.append({
            "t": float(now_ms - (limit - index - 1) * 60_000),
            "o": float(open_price),
            "h": float(high),
            "l": float(low),
            "c": float(close_price),
            "v": 0.0,
        })
    return candles


def _fallback_ticker(symbol: str) -> dict[str, str]:
    price = _fallback_price(symbol)
    candles = _synthetic_candles(price, 80)
    ticker = _build_ticker_from_candles(_normalize_symbol(symbol), candles)
    ticker["price"] = f"{price:.8f}"
    ticker["source"] = "synthetic"
    return ticker


async def get_klines(symbol: str, interval: str = "1m", limit: int = 80) -> list[dict[str, float]]:
    symbol = _normalize_symbol(symbol)
    interval = interval if interval in _INTERVAL_SECONDS else "1m"
    limit = max(1, min(int(limit), 200))
    cache_key = (symbol, interval, limit)
    cached = _klines_cache.get(cache_key)

    async with httpx.AsyncClient(timeout=10) as client:
        if _binance_available():
            try:
                data = await _get_json(
                    client,
                    f"{BINANCE}/klines",
                    params={"symbol": symbol, "interval": interval, "limit": limit},
                )
                candles = [
                    {
                        "t": candle[0],
                        "o": float(candle[1]),
                        "h": float(candle[2]),
                        "l": float(candle[3]),
                        "c": float(candle[4]),
                        "v": float(candle[5]),
                    }
                    for candle in data
                ]
                _klines_cache[cache_key] = (time.time(), candles)
                return candles
            except Exception as exc:
                LOGGER.warning("binance klines failed for %s: %s", symbol, exc)

        try:
            product = _coinbase_product(symbol)
            data = await _get_json(
                client,
                f"{COINBASE}/products/{product}/candles",
                params={"granularity": _INTERVAL_SECONDS[interval]},
            )
            candles = [
                {
                    "t": int(row[0]) * 1000,
                    "o": float(row[3]),
                    "h": float(row[2]),
                    "l": float(row[1]),
                    "c": float(row[4]),
                    "v": float(row[5]),
                }
                for row in sorted(data, key=lambda item: item[0])[-limit:]
            ]
            if candles:
                _klines_cache[cache_key] = (time.time(), candles)
                return candles
        except Exception as exc:
            LOGGER.warning("coinbase klines failed for %s: %s", symbol, exc)

    if cached:
        return cached[1]

    ticker = _price_cache.get(symbol)
    if ticker:
        return _synthetic_candles(float(ticker[1]["price"]), limit)

    return _synthetic_candles(_fallback_price(symbol), limit)


async def get_ticker24h(symbol: str) -> dict[str, str]:
    symbol = _normalize_symbol(symbol)
    cached = _price_cache.get(symbol)

    async with httpx.AsyncClient(timeout=6) as client:
        if _binance_available():
            try:
                data = await _get_json(client, f"{BINANCE}/ticker/24hr", params={"symbol": symbol})
                ticker = {
                    "symbol": symbol,
                    "price": data["lastPrice"],
                    "change": data["priceChangePercent"],
                    "high": data["highPrice"],
                    "low": data["lowPrice"],
                    "volume": data["volume"],
                    "source": "binance",
                }
                _price_cache[symbol] = (time.time(), ticker)
                return ticker
            except Exception as exc:
                LOGGER.warning("binance ticker failed for %s: %s", symbol, exc)

        try:
            product = _coinbase_product(symbol)
            spot = await _get_json(client, f"https://api.coinbase.com/v2/prices/{product}/spot")
            price = float(spot["data"]["amount"])
            try:
                candles = await get_klines(symbol, "1m", 80)
            except Exception:
                candles = _synthetic_candles(price, 80)
            ticker = _build_ticker_from_candles(symbol, candles)
            ticker["price"] = f"{price:.8f}"
            ticker["source"] = "coinbase"
            _price_cache[symbol] = (time.time(), ticker)
            return ticker
        except Exception as exc:
            LOGGER.warning("coinbase ticker failed for %s: %s", symbol, exc)

    if cached and _cache_fresh(cached[0]):
        return {**cached[1], "source": "cache"}
    if cached:
        return {**cached[1], "source": "stale-cache"}

    candles_key = (symbol, "1m", 80)
    candles = _klines_cache.get(candles_key)
    if candles:
        ticker = _build_ticker_from_candles(symbol, candles[1])
        _price_cache[symbol] = (time.time(), ticker)
        return ticker

    ticker = _fallback_ticker(symbol)
    _price_cache[symbol] = (time.time(), ticker)
    return ticker


async def get_current_price(symbol: str) -> float:
    ticker = await get_ticker24h(symbol)
    return float(ticker["price"])
