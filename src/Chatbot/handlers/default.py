from telegram import Update, constants
from telegram.ext import ContextTypes
import os

import config


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Здравствуйте, {user.full_name}!\n"
        "Это бот для управления регистрациями на мероприятия.\n"
        "Для получения справки используйте команду /help."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "<b>Для этого бота доступны следующие команды:</b>\n"
        "/start - начать работу с ботом\n"
        "/help - получить справку\n"
        "/registrations - просмотреть регистрации на мероприятия\n\n"
        "<b>Конфигурация:</b>\n"
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
