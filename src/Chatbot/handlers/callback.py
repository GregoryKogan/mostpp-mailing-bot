from telegram import Update
from telegram.ext import ContextTypes
import logging

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
from .mailing import (
    generate_confirmation_emails,
    generate_thankful_emails,
    cancel_sending,
    send_confirmation_emails,
    send_thankful_emails,
)


async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    callback_type = parse_callback_type(query.data)

    routing = {
        CallbackType.EVENT_REGISTRATIONS: {
            "function": event_specific_registrations,
            "args": [update, context, query],
        },
        CallbackType.EVENT_INFO_BEFORE_SENDING_CONFIRMATIONS: {
            "function": event_info_case,
            "args": [update, context, query, "confirmations"],
        },
        CallbackType.EVENT_INFO_BEFORE_SENDING_THANKS: {
            "function": event_info_case,
            "args": [update, context, query, "thanks"],
        },
        CallbackType.GENERATE_EMAIL: {
            "function": generate_email_case,
            "args": [update, context, query],
        },
        CallbackType.CHANGE_EVENT_DATA: {
            "function": change_event_info,
            "args": [update, context, query],
        },
        CallbackType.CHANGE_EVENT_DATE: {
            "function": change_event_date,
            "args": [update, context, query],
        },
        CallbackType.CHANGE_EVENT_TIME: {
            "function": change_event_time,
            "args": [update, context, query],
        },
        CallbackType.CHANGE_EVENT_LINK: {
            "function": change_event_link,
            "args": [update, context, query],
        },
        CallbackType.GO_BACK_FROM_CHANGING_EVENT_DATA: {
            "function": go_back_from_changing_event_info,
            "args": [update, context, query],
        },
        CallbackType.CANCEL_SENDING_EMAIL: {
            "function": cancel_sending,
            "args": [update, context, query],
        },
        CallbackType.SEND_EMAIL: {
            "function": send_email_case,
            "args": [update, context, query],
        },
    }

    if routing.get(callback_type):
        await routing[callback_type]["function"](*routing[callback_type]["args"])
    else:
        logging.warning(f"Unknown callback type: {callback_type}")
        await query.message.reply_text(f"Нажата неизвестная боту кнопка: {query.data}")


async def event_info_case(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    query: Update.callback_query,
    mail_type: str,
) -> None:
    context.user_data["mail_type"] = mail_type
    await event_info(update, context, query)


async def generate_email_case(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    if context.user_data.get("mail_type") == "confirmations":
        await generate_confirmation_emails(update, context, query)
    elif context.user_data.get("mail_type") == "thanks":
        await generate_thankful_emails(update, context, query)
    else:
        logging.warning(f"Unknown mail type: {context.user_data.get('mail_type')}")
        await query.message.reply_text(
            f"Неизвестный тип письма: '{context.user_data.get('mail_type')}'.\nВозможно, вы нажали кнопку на старом сообщении."
        )


async def send_email_case(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    if context.user_data.get("mail_type") == "confirmations":
        await send_confirmation_emails(update, context, query)
    elif context.user_data.get("mail_type") == "thanks":
        await send_thankful_emails(update, context, query)
    else:
        logging.warning(f"Unknown mail type: {context.user_data.get('mail_type')}")
        await query.message.reply_text(
            f"Неизвестный тип письма: '{context.user_data.get('mail_type')}'.\nВозможно, вы нажали кнопку на старом сообщении."
        )
