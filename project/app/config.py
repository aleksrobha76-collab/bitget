from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(slots=True)
class Settings:
    bot_token: str
    webapp_url: str
    web_host: str
    web_port: int
    enable_bot: bool
    enable_web: bool
    data_dir: Path
    database_url: str
    admin_telegram_ids: frozenset[int]
    admin_usernames: frozenset[str]

    @property
    def templates_dir(self) -> Path:
        return BASE_DIR / "app" / "templates"

    @property
    def static_dir(self) -> Path:
        return BASE_DIR / "app" / "static"


def get_settings() -> Settings:
    load_dotenv(BASE_DIR / ".env", override=True)
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    webapp_url = _get_webapp_url()
    web_host = os.getenv("WEB_HOST", "127.0.0.1").strip()
    web_port = int(os.getenv("WEB_PORT", "8000"))
    enable_bot = _parse_bool(os.getenv("ENABLE_BOT"), default=True)
    enable_web = _parse_bool(os.getenv("ENABLE_WEB"), default=True)
    data_dir = Path(os.getenv("DATA_DIR", "./data")).resolve()
    database_url = os.getenv("DATABASE_URL", "").strip()
    admin_telegram_ids = _parse_admin_ids(os.getenv("ADMIN_TELEGRAM_IDS", ""))
    admin_usernames = _parse_admin_usernames(os.getenv("ADMIN_USERNAMES", ""))

    return Settings(
        bot_token=bot_token,
        webapp_url=webapp_url,
        web_host=web_host,
        web_port=web_port,
        enable_bot=enable_bot,
        enable_web=enable_web,
        data_dir=data_dir,
        database_url=database_url,
        admin_telegram_ids=admin_telegram_ids,
        admin_usernames=admin_usernames,
    )


def _parse_bool(raw_value: str | None, *, default: bool) -> bool:
    if raw_value is None or not raw_value.strip():
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_webapp_url() -> str:
    explicit_url = os.getenv("WEBAPP_URL", "").strip()
    if explicit_url:
        return explicit_url.rstrip("/")

    render_url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
    if render_url:
        return render_url.rstrip("/")

    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
    if render_hostname:
        return f"https://{render_hostname}".rstrip("/")

    return "http://127.0.0.1:8000"


def _parse_admin_ids(raw_value: str) -> frozenset[int]:
    values: set[int] = set()
    for chunk in raw_value.split(","):
        candidate = chunk.strip()
        if not candidate:
            continue
        try:
            values.add(int(candidate))
        except ValueError:
            continue
    return frozenset(values)


def _parse_admin_usernames(raw_value: str) -> frozenset[str]:
    values = {
        chunk.strip().lstrip("@").lower()
        for chunk in raw_value.split(",")
        if chunk.strip()
    }
    return frozenset(values)
