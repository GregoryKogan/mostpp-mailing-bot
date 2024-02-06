from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os

from EventManager import EventManager, EmailClient
from CallbackHasher import CallbackHasher


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(rf"Hi {user.mention_html()}!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


async def meaningless(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"I don't know this command: '{update.message.text}'"
    )


async def registrations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Collecting registrations... Please wait.")

    email_client = EmailClient(
        os.environ.get("EMAIL_ADDRESS"),
        os.environ.get("EMAIL_APP_PASSWORD"),
        "imap.mail.ru",
    )
    event_manager = EventManager(email_client, os.environ.get("NOTIFIER_ADDRESS"))

    msg_text = "Registrations:\n"
    registrations = event_manager.get_registrations()
    events = list(registrations.keys())
    for event in events:
        msg_text += f"\n\n<b>{event}:</b>\n"
        for registration in registrations[event]:
            msg_text += f"\n{registration.pretty_str()}\n"

    await update.message.reply_text(msg_text, parse_mode=constants.ParseMode.HTML)
    await update.message.reply_text(
        "You may select an event to see more options.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        event,
                        callback_data=f"event${CallbackHasher.hash_callback(event)}",
                    )
                ]
                for event in events
            ]
        ),
    )
