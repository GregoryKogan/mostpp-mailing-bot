from telegram import Update, constants
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import os
import traceback
import html
import json

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
        "DEV": "Разработка",
        "PROD": "Продакшн",
        "TEST": "Тестирование",
    }
    await update.message.reply_text(
        "<b>Для этого бота доступны следующие команды:</b>\n"
        "/start - начать работу с ботом\n"
        "/help - получить справку\n"
        "/registrations - просмотреть регистрации на мероприятия\n\n"
        "<b>Конфигурация:</b>\n"
        f" - Режим работы: \n{mode_names[config.MODE]}\n"
        f" - Рабочий email: \n{os.environ.get('EMAIL_ADDRESS')}\n"
        f" - Email уведомителя: \n{os.environ.get('NOTIFIER_ADDRESS')}\n"
        f" - Максимальное время регистрации: \n{config.REGISTRATION_PERIOD} мес\n"
        f" - Ключевые слова в теме письма: \n<code>{', '.join(config.REGISTRATION_SUBJECT_KEYWORDS)}</code>\n"
        f" - Время жизни кеша регистраций: \n{config.REGISTRATIONS_CACHE_LIFETIME} сек\n\n"
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
    if is_library_error(context.error):
        if config.MODE == "DEV":
            raise context.error
        logger.warning(f"Library error: {context.error.__str__()}")
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


def is_library_error(error: Exception) -> bool:
    tb = error.__traceback__
    while tb is not None:
        if "site-packages" in tb.tb_frame.f_code.co_filename:
            return True
        tb = tb.tb_next
    return False
