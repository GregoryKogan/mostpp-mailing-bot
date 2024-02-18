from telegram import Update
from telegram.ext import ContextTypes

from Chatbot.CallbackHasher import CallbackType, parse_callback_type
from .events import (
    event_specific_registrations,
    event_info,
    change_event_info,
    change_event_date,
    change_event_time,
    change_event_link,
    go_back_from_changing_event_info,
)


async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    callback_type = parse_callback_type(query.data)

    if callback_type == CallbackType.EVENT_REGISTRATIONS:
        await event_specific_registrations(update, context, query)
    elif callback_type == CallbackType.EVENT_INFO_BEFORE_SENDING_CONFIRMATIONS:
        context.user_data["mail_type"] = "confirmations"
        await event_info(update, context, query)
    elif callback_type == CallbackType.EVENT_INFO_BEFORE_SENDING_THANKS:
        context.user_data["mail_type"] = "thanks"
        await event_info(update, context, query)
    elif callback_type == CallbackType.GENERATE_EMAIL:
        ...
    elif callback_type == CallbackType.CHANGE_EVENT_DATA:
        await change_event_info(update, context, query)
    elif callback_type == CallbackType.CHANGE_EVENT_DATE:
        await change_event_date(update, context, query)
    elif callback_type == CallbackType.CHANGE_EVENT_TIME:
        await change_event_time(update, context, query)
    elif callback_type == CallbackType.CHANGE_EVENT_LINK:
        await change_event_link(update, context, query)
    elif callback_type == CallbackType.GO_BACK_FROM_CHANGING_EVENT_DATA:
        await go_back_from_changing_event_info(update, context, query)
    else:
        # TODO: Log unknown callback
        await query.message.reply_text(f"Нажата неизвестная боту кнопка: {query.data}")
