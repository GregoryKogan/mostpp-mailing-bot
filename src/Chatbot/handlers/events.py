from telegram import Update, constants, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from .jobs import fetch_registrations, get_event_data
from . import keyboards
from Chatbot.CallbackHasher import unhash_event_name
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
        reply_markup=keyboards.select_event(events),
    )


async def event_specific_registrations(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)

    msg_text = f"<b>{event}:</b>\n"
    for registration in registrations[event]:
        msg_text += f"\n{registration.pretty_str()}\n"

    await query.message.reply_text(
        msg_text,
        parse_mode=constants.ParseMode.HTML,
        reply_markup=keyboards.select_mail_type(event),
    )


async def event_info(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)
    event_data = await get_event_data(update, context, event)
    await query.message.reply_text("Полная информация о мероприятии: ")
    info_message = await query.message.reply_text(
        str(event_data),
        parse_mode=constants.ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=keyboards.build_email_or_change_event(event),
    )
    context.user_data["last_event_info_message_id"] = info_message.message_id


async def change_event_info(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)
    await context.bot.edit_message_reply_markup(
        chat_id=update.effective_chat.id,
        message_id=context.user_data["last_event_info_message_id"],
        reply_markup=keyboards.select_field_to_change(event),
    )


async def go_back_from_changing_event_info(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)
    await context.bot.edit_message_reply_markup(
        chat_id=update.effective_chat.id,
        message_id=context.user_data["last_event_info_message_id"],
        reply_markup=keyboards.build_email_or_change_event(event),
    )


async def change_event_date(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)

    await query.message.reply_text("Введите дату проведения мероприятия:")

    context.user_data["event_to_change"] = event
    context.user_data["event_query"] = query
    context.user_data["field_to_change"] = "date"


async def change_event_time(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)

    await query.message.reply_text("Введите время проведения мероприятия:")

    context.user_data["event_to_change"] = event
    context.user_data["event_query"] = query
    context.user_data["field_to_change"] = "time"


async def change_event_link(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)

    await query.message.reply_text("Введите ссылку на мероприятие:")

    context.user_data["event_to_change"] = event
    context.user_data["event_query"] = query
    context.user_data["field_to_change"] = "link"
