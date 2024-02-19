from telegram import Update, constants
from telegram.ext import ContextTypes
import logging

from .jobs import get_event_data, update_event_data
from .events import event_info


async def plaintext(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("event_to_change") is not None:
        logging.info("Changing event data from plaintext handler")
        event = context.user_data["event_to_change"]
        event_query = context.user_data["event_query"]
        field = context.user_data["field_to_change"]
        context.user_data["event_to_change"] = None
        context.user_data["field_to_change"] = None
        event_data = await get_event_data(update, context, event)
        event_data[field] = update.message.text
        update_event_data(update, context, event, event_data)
        await event_info(update, context, event_query)
        return

    logging.info("Plaintext handler: meaningless message")
    await update.message.reply_text(
        f"Бот не знает такой команды: '{update.message.text}'"
    )
