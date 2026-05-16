from __future__ import annotations

import asyncio
import logging
import threading

import uvicorn

from .bot import build_application
from .config import get_settings
from .storage import UserStorage
from .web import create_app
from .worker_bot import build_worker_application


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def run_web_server(settings, storage) -> None:
    app = create_app(settings, storage)
    uvicorn.run(
        app,
        host=settings.web_host,
        port=settings.web_port,
        log_level="info",
    )


def run_bot_application(application, name: str) -> None:
    asyncio.set_event_loop(asyncio.new_event_loop())
    logging.getLogger(__name__).info("Starting %s polling", name)
    application.run_polling(
        drop_pending_updates=True,
        close_loop=False,
        stop_signals=None,
    )


def main() -> None:
    settings = get_settings()
    if settings.enable_bot and not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is not set. Copy .env.example to .env and fill it in.")
    if settings.enable_worker_bot and not settings.worker_bot_token:
        raise RuntimeError("WORKER_BOT_TOKEN is not set while ENABLE_WORKER_BOT=true.")

    storage = UserStorage(settings.data_dir, database_url=settings.database_url)

    if not settings.enable_bot and not settings.enable_worker_bot and not settings.enable_web:
        raise RuntimeError("ENABLE_BOT, ENABLE_WORKER_BOT and ENABLE_WEB cannot all be false.")

    if settings.enable_web and not settings.enable_bot and not settings.enable_worker_bot:
        run_web_server(settings, storage)
        return

    if settings.enable_web:
        web_thread = threading.Thread(
            target=run_web_server,
            args=(settings, storage),
            name="mini-app-web",
            daemon=True,
        )
        web_thread.start()

    if settings.enable_worker_bot and settings.enable_bot:
        worker_application = build_worker_application(settings, storage)
        worker_thread = threading.Thread(
            target=run_bot_application,
            args=(worker_application, "worker-bot"),
            name="worker-bot",
            daemon=True,
        )
        worker_thread.start()

    if settings.enable_bot:
        application = build_application(settings, storage)
        run_bot_application(application, "main-bot")
        return

    if settings.enable_worker_bot:
        worker_application = build_worker_application(settings, storage)
        run_bot_application(worker_application, "worker-bot")


if __name__ == "__main__":
    main()
