from telegram import Update
from telegram.ext import ContextTypes
import os

from Chatbot.Cache import Cache
from Mailing.EmailReadingClient import EmailReadingClient
from EventManagement.EventManager import EventManager
import config


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    client = EmailSendingClient(
        os.environ.get("EMAIL_ADDRESS"),
        os.environ.get("EMAIL_APP_PASSWORD"),
        "smtp.mail.ru",
        "imap.mail.ru",
    )

    send_to = "grisha.koganovskiy@gmail.com"
    email_content = EmailContent("Test", "This is a test email from the bot.")

    client.send_email(send_to, email_content)

    await update.message.reply_text("Test")


async def fetch_registrations(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> any:
    cache = Cache()
    if cache.has_key("registrations"):
        return cache.get("registrations")

    if update.message:
        wait_message = await update.message.reply_text(
            "Обновление регистраций...\nЭто может занять некоторое время."
        )
    elif update.callback_query:
        wait_message = await update.callback_query.message.reply_text(
            "Обновление регистраций...\nЭто может занять некоторое время."
        )

    email_client = EmailReadingClient(
        os.environ.get("EMAIL_ADDRESS"),
        os.environ.get("EMAIL_APP_PASSWORD"),
        "imap.mail.ru",
    )
    event_manager = EventManager(email_client, os.environ.get("NOTIFIER_ADDRESS"))
    cache.store(
        "registrations",
        event_manager.get_registrations(),
        config.REGISTRATIONS_CACHE_LIFETIME,
    )

    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=wait_message.message_id
    )

    return cache.get("registrations")
