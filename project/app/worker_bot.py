from __future__ import annotations

import html
import logging
import re

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.error import Conflict
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .auth import is_owner_account
from .config import Settings
from .storage import UserStorage


LOGGER = logging.getLogger(__name__)
APPLICATION_ACTION_PATTERN = re.compile(r"^worker_app:(accept|reject):(\d+):([A-Za-z0-9_]+)$")

# Welcome photo path (relative to static_dir)
WELCOME_PHOTO_PATH = "images/welcome-worker.png"

# Welcome text (from screenshot 2)
WELCOME_TEXT = (
    "🎉 <b>Добро пожаловать в BlackChip Team!</b>\n\n"
    "Это бот для создания и управления заявками. "
    "Следуйте инструкциям, чтобы начать работу.\n\n"
    "🛡 <b>Быстро и безопасно</b>\n"
    "└ Ваши данные под защитой\n\n"
    "⚡ <b>Удобное управление</b>\n"
    "└ Простое создание и контроль заявок\n\n"
    "🎧 <b>ТС всегда на связи</b>\n"
    "└ Мы всегда готовы помочь"
)

# About project text
ABOUT_TEXT = (
    "🚀 <b>О НАШЕМ ПРОЕКТЕ</b>\n\n"
    "Мы предлагаем прозрачные условия, стабильную работу "
    "и высокий процент выплат.\n\n"
    "💰 Депозит — до 75%\n"
    "💸 Прямой перевод — до 70%\n"
    "🤝 Техническая поддержка — до 65%\n\n"
    "⚡️ Моментальная обработка заявок\n"
    "💳 Выплаты на любые криптокошельки\n"
    "🛠 Постоянная поддержка команды\n"
    "📈 Высокие проценты по каждому направлению\n"
    "🔒 Надёжная и удобная система работы\n\n"
    "Присоединяйтесь к команде и получайте максимум "
    "от каждого рабочего процесса."
)

# Training text (placeholder)
TRAINING_TEXT = (
    "📚 <b>ОБУЧЕНИЕ</b>\n\n"
    "Раздел обучения находится в разработке.\n"
    "Скоро здесь появятся подробные материалы и инструкции.\n\n"
    "Следите за обновлениями! 🔔"
)

# Channels for subscription check
INFO_CHANNEL_ID = "@+Qs_LBEPudk80ZmYy"
PROFIT_CHANNEL_ID = "@+tCgahEXfAqM5Y2Ri"
WORKER_CHAT_LINK = "https://t.me/+yWOrraCmRIoxYTI6"
INFO_CHANNEL_LINK = "https://t.me/+Qs_LBEPudk80ZmYy"
PROFIT_CHANNEL_LINK = "https://t.me/+tCgahEXfAqM5Y2Ri"
MAIN_BOT_LINK = "https://t.me/b1tget_bot"

# Reply keyboard button texts
BTN_FORM = "📋 Заполнить анкету"
BTN_EDIT_FORM = "✏️ Изменить анкету"
BTN_ABOUT = "🚀 О проекте"
BTN_TRAINING = "📚 Обучение"
BTN_CHAT = "💬 Чат воркеров"
BTN_BOT = "🤖 Бот"

# Conversation states for application form
(
    STATE_EXPERIENCE,
    STATE_PROFIT,
    STATE_TIME,
    STATE_VOLUMES,
    STATE_SOURCE,
    STATE_MOTIVATION,
    STATE_CONFIRM,
) = range(7)

FORM_QUESTIONS = [
    ("💼 Опыт работы в данной сфере:", STATE_EXPERIENCE),
    ("📈 Общий профит за всё время работы:", STATE_PROFIT),
    ("⏳ Сколько времени готовы уделять работе ежедневно:", STATE_TIME),
    ("📊 С какими объёмами работали ранее:", STATE_VOLUMES),
    ("📢 Откуда узнали о нас:", STATE_SOURCE),
    ("🎯 Почему хотите присоединиться к команде:", STATE_MOTIVATION),
]

FORM_KEYS = ["experience", "profit", "time", "volumes", "source", "motivation"]


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


def _main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Persistent reply keyboard menu."""
    keyboard = [
        [KeyboardButton(BTN_FORM), KeyboardButton(BTN_EDIT_FORM)],
        [KeyboardButton(BTN_ABOUT), KeyboardButton(BTN_TRAINING)],
        [KeyboardButton(BTN_CHAT), KeyboardButton(BTN_BOT)],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def _confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Отправить", callback_data="form_submit"),
            InlineKeyboardButton("❌ Отменить", callback_data="form_cancel"),
        ],
    ])


def _admin_keyboard(applicant_id: int, username: str) -> InlineKeyboardMarkup:
    payload = f"{applicant_id}:{username}"
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Принять", callback_data=f"worker_app:accept:{payload}"),
                InlineKeyboardButton("❌ Отклонить", callback_data=f"worker_app:reject:{payload}"),
            ]
        ]
    )


def _format_application(answers: dict) -> str:
    return (
        "📋 <b>АНКЕТА РАБОТНИКА</b>\n"
        "━━━━━━━━━━━━━━\n\n"
        f"💼 <b>Опыт работы в данной сфере:</b>\n"
        f"└ {html.escape(answers.get('experience', '—'))}\n\n"
        f"📈 <b>Общий профит за всё время работы:</b>\n"
        f"└ {html.escape(answers.get('profit', '—'))}\n\n"
        f"⏳ <b>Сколько времени готовы уделять работе ежедневно:</b>\n"
        f"└ {html.escape(answers.get('time', '—'))}\n\n"
        f"📊 <b>С какими объёмами работали ранее:</b>\n"
        f"└ {html.escape(answers.get('volumes', '—'))}\n\n"
        f"📢 <b>Откуда узнали о нас:</b>\n"
        f"└ {html.escape(answers.get('source', '—'))}\n\n"
        f"🎯 <b>Почему хотите присоединиться к команде:</b>\n"
        f"└ {html.escape(answers.get('motivation', '—'))}"
    )


def _format_applicant_for_admin(user, answers: dict) -> str:
    username = f"@{user.username}" if user.username else "без username"
    full_name = " ".join(
        part for part in (user.first_name, user.last_name) if part
    ) or "не указано"
    return (
        "<b>📩 Новая заявка воркера</b>\n\n"
        f"<b>Имя:</b> {html.escape(full_name)}\n"
        f"<b>Username:</b> {html.escape(username)}\n"
        f"<b>Telegram ID:</b> <code>{user.id}</code>\n\n"
        + _format_application(answers)
    )


async def _send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings: Settings = context.application.bot_data["settings"]
    message = update.message

    # Send photo
    photo_path = settings.static_dir / WELCOME_PHOTO_PATH
    if photo_path.exists():
        with photo_path.open("rb") as photo:
            await message.reply_photo(photo=photo)

    # Send welcome text + persistent reply keyboard
    await message.reply_text(
        WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=_main_menu_keyboard(),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    context.user_data.pop("form_answers", None)
    await _send_welcome(update, context)


# --- Reply keyboard button handlers ---

async def handle_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        ABOUT_TEXT,
        parse_mode="HTML",
        reply_markup=_main_menu_keyboard(),
    )


async def handle_training(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        TRAINING_TEXT,
        parse_mode="HTML",
        reply_markup=_main_menu_keyboard(),
    )


async def handle_bot_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 Перейти в основного бота:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Открыть бота", url=MAIN_BOT_LINK)],
        ]),
    )


async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    subscribed_info = True
    subscribed_profit = True

    try:
        member_info = await context.bot.get_chat_member(
            chat_id=INFO_CHANNEL_ID, user_id=user_id
        )
        if member_info.status in ("left", "kicked"):
            subscribed_info = False
    except Exception:
        subscribed_info = False

    try:
        member_profit = await context.bot.get_chat_member(
            chat_id=PROFIT_CHANNEL_ID, user_id=user_id
        )
        if member_profit.status in ("left", "kicked"):
            subscribed_profit = False
    except Exception:
        subscribed_profit = False

    if not subscribed_info or not subscribed_profit:
        buttons = []
        if not subscribed_info:
            buttons.append([InlineKeyboardButton(
                "📢 Инфо канал", url=INFO_CHANNEL_LINK
            )])
        if not subscribed_profit:
            buttons.append([InlineKeyboardButton(
                "💰 Канал профитов", url=PROFIT_CHANNEL_LINK
            )])
        buttons.append([InlineKeyboardButton(
            "🔄 Проверить подписку", callback_data="check_sub"
        )])

        await update.message.reply_text(
            "❌ Для доступа к чату воркеров необходимо подписаться на оба канала:\n\n"
            "1️⃣ Инфо канал\n"
            "2️⃣ Канал профитов\n\n"
            "Подпишитесь и нажмите «Проверить подписку».",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return

    await update.message.reply_text(
        "✅ Вы подписаны на оба канала!\n\n"
        "Нажмите кнопку ниже, чтобы войти в чат воркеров:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Войти в чат", url=WORKER_CHAT_LINK)],
        ]),
    )


async def handle_check_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Re-check subscription when user presses inline button."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    subscribed_info = True
    subscribed_profit = True

    try:
        member_info = await context.bot.get_chat_member(
            chat_id=INFO_CHANNEL_ID, user_id=user_id
        )
        if member_info.status in ("left", "kicked"):
            subscribed_info = False
    except Exception:
        subscribed_info = False

    try:
        member_profit = await context.bot.get_chat_member(
            chat_id=PROFIT_CHANNEL_ID, user_id=user_id
        )
        if member_profit.status in ("left", "kicked"):
            subscribed_profit = False
    except Exception:
        subscribed_profit = False

    if not subscribed_info or not subscribed_profit:
        buttons = []
        if not subscribed_info:
            buttons.append([InlineKeyboardButton(
                "📢 Инфо канал", url=INFO_CHANNEL_LINK
            )])
        if not subscribed_profit:
            buttons.append([InlineKeyboardButton(
                "💰 Канал профитов", url=PROFIT_CHANNEL_LINK
            )])
        buttons.append([InlineKeyboardButton(
            "🔄 Проверить подписку", callback_data="check_sub"
        )])

        await query.edit_message_text(
            "❌ Вы ещё не подписаны на все каналы.\n\n"
            "1️⃣ Инфо канал\n"
            "2️⃣ Канал профитов\n\n"
            "Подпишитесь и нажмите «Проверить подписку».",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return

    await query.edit_message_text(
        "✅ Вы подписаны на оба канала!\n\n"
        "Нажмите кнопку ниже, чтобы войти в чат воркеров:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Войти в чат", url=WORKER_CHAT_LINK)],
        ]),
    )


# --- Application form (ConversationHandler) ---

async def form_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["form_answers"] = {}
    await update.message.reply_text(
        "📋 <b>АНКЕТА РАБОТНИКА</b>\n"
        "━━━━━━━━━━━━━━\n\n"
        "Ответьте на несколько вопросов.\n"
        "Вы можете отменить заполнение командой /cancel\n\n"
        f"<b>{FORM_QUESTIONS[0][0]}</b>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
    return STATE_EXPERIENCE


async def _handle_form_step(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    key: str,
    next_state: int,
    next_question_idx: int | None,
) -> int:
    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("Пожалуйста, введите ответ текстом.")
        return next_state - 1 if next_state > 0 else STATE_EXPERIENCE

    answers = context.user_data.setdefault("form_answers", {})
    answers[key] = text

    if next_question_idx is not None and next_question_idx < len(FORM_QUESTIONS):
        await update.message.reply_text(
            f"<b>{FORM_QUESTIONS[next_question_idx][0]}</b>",
            parse_mode="HTML",
        )
        return next_state

    # All questions answered — show confirmation
    preview = _format_application(answers)
    await update.message.reply_text(
        f"{preview}\n\n"
        "━━━━━━━━━━━━━━\n"
        "Проверьте анкету и подтвердите отправку:",
        parse_mode="HTML",
        reply_markup=_confirm_keyboard(),
    )
    return STATE_CONFIRM


async def handle_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _handle_form_step(update, context, "experience", STATE_PROFIT, 1)


async def handle_profit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _handle_form_step(update, context, "profit", STATE_TIME, 2)


async def handle_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _handle_form_step(update, context, "time", STATE_VOLUMES, 3)


async def handle_volumes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _handle_form_step(update, context, "volumes", STATE_SOURCE, 4)


async def handle_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _handle_form_step(update, context, "source", STATE_MOTIVATION, 5)


async def handle_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _handle_form_step(update, context, "motivation", STATE_CONFIRM, None)


async def handle_form_submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    settings: Settings = context.application.bot_data["settings"]
    storage: UserStorage = context.application.bot_data["storage"]
    answers = context.user_data.get("form_answers", {})

    if not user.username:
        await query.message.reply_text(
            "❌ Для подачи заявки нужен Telegram username.\n"
            "Добавьте username в настройках Telegram и попробуйте снова.",
            reply_markup=_main_menu_keyboard(),
        )
        return ConversationHandler.END

    existing_worker = storage.get_worker_by_username(user.username)
    if existing_worker is not None:
        await query.message.reply_text(
            f"✅ Вы уже добавлены как воркер. Ваш код: {existing_worker['code']}.",
            reply_markup=_main_menu_keyboard(),
        )
        return ConversationHandler.END

    admin_ids = sorted(settings.admin_telegram_ids)
    if not admin_ids:
        await query.message.reply_text(
            "⚠️ Заявка заполнена, но ID админа пока не настроен.",
            reply_markup=_main_menu_keyboard(),
        )
        return ConversationHandler.END

    text = _format_applicant_for_admin(user, answers)
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
        await query.message.reply_text(
            "❌ Не получилось отправить заявку админу. Попробуйте позже.",
            reply_markup=_main_menu_keyboard(),
        )
        return ConversationHandler.END

    context.user_data.pop("form_answers", None)
    await query.message.reply_text(
        "✅ Анкета отправлена на рассмотрение!\n"
        "Ожидайте решение администратора.",
        reply_markup=_main_menu_keyboard(),
    )
    return ConversationHandler.END


async def handle_form_cancel_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.pop("form_answers", None)
    await query.message.reply_text(
        "❌ Заполнение анкеты отменено.",
        reply_markup=_main_menu_keyboard(),
    )
    return ConversationHandler.END


async def handle_form_cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("form_answers", None)
    await update.message.reply_text(
        "❌ Заполнение анкеты отменено.",
        reply_markup=_main_menu_keyboard(),
    )
    return ConversationHandler.END


# --- Admin accept/reject handler ---

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
                text="❌ Ваша заявка отклонена.",
            )
        except Exception as exc:
            LOGGER.warning("Failed to notify rejected applicant %s: %s", applicant_id, exc)
        return

    try:
        worker = storage.create_worker(username)
        admin_text = f"✅ Воркер @{worker['username']} принят. Код: {worker['code']}."
        worker_text = (
            "✅ Вас приняли! Ожидайте, админ свяжется с вами.\n"
            f"Ваш код воркера: <b>{worker['code']}</b>"
        )
    except ValueError:
        existing_worker = storage.get_worker_by_username(username)
        if existing_worker is None:
            await query.answer("Ошибка создания воркера", show_alert=True)
            return
        admin_text = f"@{existing_worker['username']} уже есть в воркерах. Код: {existing_worker['code']}."
        worker_text = (
            "✅ Вас приняли! Ожидайте, админ свяжется с вами.\n"
            f"Ваш код воркера: <b>{existing_worker['code']}</b>"
        )

    await query.answer("Принято")
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text(admin_text)
    try:
        await context.bot.send_message(
            chat_id=applicant_id, text=worker_text, parse_mode="HTML"
        )
    except Exception as exc:
        LOGGER.warning("Failed to notify accepted applicant %s: %s", applicant_id, exc)


def build_worker_application(settings: Settings, storage: UserStorage) -> Application:
    application = (
        ApplicationBuilder()
        .token(settings.worker_bot_token)
        .post_init(_post_init)
        .build()
    )
    application.bot_data["settings"] = settings
    application.bot_data["storage"] = storage

    # Conversation handler for the application form
    form_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Text([BTN_FORM]), form_start),
            MessageHandler(filters.Text([BTN_EDIT_FORM]), form_start),
        ],
        states={
            STATE_EXPERIENCE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_experience),
            ],
            STATE_PROFIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profit),
            ],
            STATE_TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_time),
            ],
            STATE_VOLUMES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_volumes),
            ],
            STATE_SOURCE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_source),
            ],
            STATE_MOTIVATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_motivation),
            ],
            STATE_CONFIRM: [
                CallbackQueryHandler(handle_form_submit, pattern="^form_submit$"),
                CallbackQueryHandler(handle_form_cancel_button, pattern="^form_cancel$"),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", handle_form_cancel_command),
            CommandHandler("start", start),
        ],
        per_user=True,
        per_chat=True,
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(form_handler)
    application.add_handler(MessageHandler(filters.Text([BTN_ABOUT]), handle_about))
    application.add_handler(MessageHandler(filters.Text([BTN_TRAINING]), handle_training))
    application.add_handler(MessageHandler(filters.Text([BTN_CHAT]), handle_chat))
    application.add_handler(MessageHandler(filters.Text([BTN_BOT]), handle_bot_button))
    application.add_handler(CallbackQueryHandler(handle_check_sub_callback, pattern="^check_sub$"))
    application.add_handler(CallbackQueryHandler(handle_application_action, pattern=APPLICATION_ACTION_PATTERN))
    application.add_error_handler(log_error)

    return application
