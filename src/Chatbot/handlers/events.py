from telegram import Update, constants, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from .jobs import fetch_registrations
from Chatbot.Cache import Cache
from Chatbot.CallbackHasher import CallbackHasher
import config


async def registrations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    registrations = await fetch_registrations(update, context)

    msg_text = (
        f"<b>Все регистрации за последение {config.REGISTRATION_PERIOD} мес:</b>\n"
    )
    events = list(registrations.keys())
    for event in events:
        msg_text += f"\n\n<b>{event}:</b>\n"
        for registration in registrations[event]:
            msg_text += f"\n{registration.pretty_str()}\n"

    await update.message.reply_text(msg_text, parse_mode=constants.ParseMode.HTML)
    await update.message.reply_text(
        "Вы можете посмотреть регистрации на конкретное мероприятие, выбрав его ниже:",
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


async def event_callback_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    registrations = await fetch_registrations(update, context)

    event = CallbackHasher.unhash_callback(
        query.data.split("$")[1], list(registrations.keys())
    )

    msg_text = f"<b>{event}:</b>\n"
    for registration in registrations[event]:
        msg_text += f"\n{registration.pretty_str()}\n"

    await query.message.reply_text(
        msg_text,
        parse_mode=constants.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Напоминания",
                        callback_data=f"conf${CallbackHasher.hash_callback(event)}",
                    ),
                    InlineKeyboardButton(
                        "Благодарности",
                        callback_data=f"thank${CallbackHasher.hash_callback(event)}",
                    ),
                ]
            ]
        ),
    )


async def confirmation_callback_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    registrations = await fetch_registrations(update, context)

    event = CallbackHasher.unhash_callback(
        query.data.split("$")[1], list(registrations.keys())
    )

    msg_text = "".join(
        f"{registration.email}\n" for registration in registrations[event]
    )
    msg_text += f"\nВы уверены, что хотите отправить письма, напоминающие о мероприятии \n<b>'{event}'</b>,\nвсем этим людям? \nВсего писем: {len(registrations[event])}"
    confirmation_message = await query.message.reply_text(
        msg_text,
        parse_mode=constants.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Да",
                        callback_data=f"yconf${CallbackHasher.hash_callback(event)}",
                    ),
                    InlineKeyboardButton(
                        "Нет",
                        callback_data=f"nconf${CallbackHasher.hash_callback(event)}",
                    ),
                ]
            ]
        ),
    )
    context.user_data["last_confirmation_message"] = confirmation_message.message_id


async def thanks_callback_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    registrations = await fetch_registrations(update, context)

    event = CallbackHasher.unhash_callback(
        query.data.split("$")[1], list(registrations.keys())
    )

    msg_text = "".join(
        f"{registration.email}\n" for registration in registrations[event]
    )
    msg_text += f"\nВы уверены, что хотите отправить письма благодарности за участие в мероприятии \n<b>'{event}'</b>\nвсем этим людям? \nВсего писем: {len(registrations[event])}"
    confirmation_message = await query.message.reply_text(
        msg_text,
        parse_mode=constants.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Да",
                        callback_data=f"ythan${CallbackHasher.hash_callback(event)}",
                    ),
                    InlineKeyboardButton(
                        "Нет",
                        callback_data=f"nthan${CallbackHasher.hash_callback(event)}",
                    ),
                ]
            ]
        ),
    )
    context.user_data["last_confirmation_message"] = confirmation_message.message_id
