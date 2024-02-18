from telegram import Update
from telegram.ext import ContextTypes

from .events import (
    event_callback_query,
    confirmation_callback_query,
    thanks_callback_query,
)
from .mailing import (
    send_confirmation_emails,
    cancel_sending_confirmation_emails,
    send_thankful_emails,
    cancel_sending_thankful_emails,
)


async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Event-related callbacks
    if query.data.startswith("event$"):
        await event_callback_query(update, context, query)
    elif query.data.startswith("conf$"):
        await confirmation_callback_query(update, context, query)
    elif query.data.startswith("thank$"):
        await thanks_callback_query(update, context, query)
    # Mailing-related callbacks
    elif query.data.startswith("yconf$"):
        await send_confirmation_emails(update, context, query)
    elif query.data.startswith("nconf$"):
        await cancel_sending_confirmation_emails(update, context, query)
    elif query.data.startswith("ythan$"):
        await send_thankful_emails(update, context, query)
    elif query.data.startswith("nthan$"):
        await cancel_sending_thankful_emails(update, context, query)
    # Unknown callback
    else:
        # TODO: Log unknown callback
        await query.message.reply_text(f"Нажата неизвестная боту кнопка: {query.data}")
