from telegram import Update, constants, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from .jobs import fetch_registrations, scrape_event_data
from .utils import delete_last_confirmation_message
from Chatbot.CallbackHasher import CallbackHasher, unhash_event_name
from EmailGeneration.EmailGeneration import EventEmailGenerator
import config


async def send_confirmation_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    await delete_last_confirmation_message(context, update.effective_chat.id)
    await query.message.reply_text(
        "Возможность отправки писем-напоминаний об участии в мероприятии пока не реализована."
    )


async def cancel_sending_confirmation_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    await delete_last_confirmation_message(context, update.effective_chat.id)
    await query.message.reply_text(
        "Письма-напоминания <b>не</b> были отправлены.",
        parse_mode=constants.ParseMode.HTML,
    )


async def send_thankful_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    await delete_last_confirmation_message(context, update.effective_chat.id)
    await query.message.reply_text(
        "Возможность отправки писем благодарности за участие в мероприятии пока не реализована."
    )


async def cancel_sending_thankful_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    await delete_last_confirmation_message(context, update.effective_chat.id)
    await query.message.reply_text(
        "Письма благодарности <b>не</b> были отправлены.",
        parse_mode=constants.ParseMode.HTML,
    )
