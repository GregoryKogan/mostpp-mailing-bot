from telegram import Update, constants
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import os
import traceback
import html
import json
from httpx import RemoteProtocolError, ConnectError

from Logging.logger_config import logger
import config


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Здравствуйте, {user.full_name}!\n"
        "Это бот для управления регистрациями на мероприятия.\n"
        "Для получения справки используйте команду /help."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mode_names = {
        "DEV": "разработка",
        "PROD": "продакшн",
        "TEST": "тестирование",
    }
    await update.message.reply_text(
        "<b>Для этого бота доступны следующие команды:</b>\n"
        "/start - начать работу с ботом\n"
        "/help - получить справку\n"
        "/registrations - просмотреть регистрации на мероприятия\n\n"
        "<b>Конфигурация:</b>\n"
        f" • Режим работы: {mode_names[config.MODE]}\n"
        f" • Рабочий email: {os.environ.get('EMAIL_ADDRESS')}\n"
        f" • Email уведомителя: {os.environ.get('NOTIFIER_ADDRESS')}\n"
        f" • Максимальное время регистрации: {config.REGISTRATION_PERIOD} мес\n"
        f" • Время жизни кеша регистраций: {config.REGISTRATIONS_CACHE_LIFETIME // 60} мин\n"
        f" • Время жизни кеша данных о мероприятиях: {config.EVENT_DATA_CACHE_LIFETIME // 60 // 60} ч\n"
        f" • Базовый URL мероприятий: {config.EVENTS_BASE_URL}\n"
        f" • URL страницы будущих мероприятий: {config.FUTURE_EVENTS_PAGE_URL}\n"
        f" • URL страницы прошедших мероприятий: {config.PAST_EVENTS_PAGE_URL}\n"
        f" • Временная зона: {config.TIMEZONE}\n\n"
        "Исходный код: <a href='https://github.com/GregoryKogan/mostpp-mailing-bot'>GitHub</a>\n\n"
        "Тех. поддержка: @GregoryKogan\n",
        parse_mode=constants.ParseMode.HTML,
        disable_web_page_preview=True,
    )


async def meaningless(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Бот не знает такой команды: '{update.message.text}'"
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    if is_connection_error(context.error):
        if config.MODE == "DEV":
            raise context.error
        return

    logger.error(
        "An exception was raised while handling an update:", exc_info=context.error
    )

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )

    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    await context.bot.send_message(
        chat_id=os.environ.get("DEVELOPER_CHAT_ID"),
        text=message,
        parse_mode=ParseMode.HTML,
    )


def is_connection_error(error: Exception) -> bool:
    return isinstance(error, (RemoteProtocolError, ConnectError))
