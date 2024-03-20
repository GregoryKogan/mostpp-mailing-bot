from telegram import Update, constants, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import os

from .jobs import fetch_registrations, get_event_data
from . import keyboards
from EventManagement.NotificationScraper import RegistrationInfo
from Chatbot.CallbackHasher import unhash_event_name
from EmailGeneration.EmailGeneration import EventEmailGenerator
from Mailing.EmailSendingClient import EmailSendingClient
import config


async def generate_confirmation_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    await generate_emails(update, context, query, "pre-event")


async def generate_thankful_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    await generate_emails(update, context, query, "post-event")


async def generate_emails(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    query: Update.callback_query,
    mail_type: str,
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)
    recipients = [registration.email for registration in registrations[event]]
    msg_text = "<b>Адресаты</b>:\n" + ", ".join(recipients)
    msg_text += f"\nВсего: {len(recipients)}"
    await query.message.reply_text(msg_text, parse_mode=constants.ParseMode.HTML)
    await query.message.reply_text("Сгенерированное письмо: ")

    email_templates = EventEmailGenerator.read_templates(
        config.PRE_EVENT_EMAIL_TEMPLATE_PATH,
        config.PRE_EVENT_EMAIL_SUBJECT_TEMPLATE_PATH,
        config.POST_EVENT_EMAIL_TEMPLATE_PATH,
        config.POST_EVENT_EMAIL_SUBJECT_TEMPLATE_PATH,
    )
    email_generator = EventEmailGenerator(*email_templates)

    event_data = await get_event_data(update, context, event)
    email_content = (
        email_generator.generate_pre_event_email(event_data)
        if mail_type == "pre-event"
        else email_generator.generate_post_event_email(event_data)
    )

    send_message = await query.message.reply_text(
        f"<b>Тема:</b> {email_content.subject}\n\n{email_content.body}",
        parse_mode=constants.ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=keyboards.send_email_or_cancel(event),
    )
    context.user_data["send_message_id"] = send_message.message_id


async def cancel_sending(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    if context.user_data.get("send_message_id"):
        await context.bot.edit_message_reply_markup(
            chat_id=query.message.chat_id,
            message_id=context.user_data["send_message_id"],
            reply_markup=None,
        )
    await query.message.reply_text("Отправка отменена")
    context.user_data.clear()


async def send_confirmation_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    await send_emails(update, context, query, "pre-event")


async def send_thankful_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
) -> None:
    await send_emails(update, context, query, "post-event")


async def send_emails(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    query: Update.callback_query,
    mail_type: str,
) -> None:
    registrations = await fetch_registrations(update, context)
    event = unhash_event_name(query.data, registrations)
    recipients = [registration.email for registration in registrations[event]]

    email_templates = EventEmailGenerator.read_templates(
        config.PRE_EVENT_EMAIL_TEMPLATE_PATH,
        config.PRE_EVENT_EMAIL_SUBJECT_TEMPLATE_PATH,
        config.POST_EVENT_EMAIL_TEMPLATE_PATH,
        config.POST_EVENT_EMAIL_SUBJECT_TEMPLATE_PATH,
    )
    email_generator = EventEmailGenerator(*email_templates)
    event_data = await get_event_data(update, context, event)

    wait_message = await query.message.reply_text(
        "Отправка писем...\nЭто может занять некоторое время."
    )

    email_content = (
        email_generator.generate_pre_event_email(event_data)
        if mail_type == "pre-event"
        else email_generator.generate_post_event_email(event_data)
    )

    email_client = EmailSendingClient(
        os.environ.get("EMAIL_ADDRESS"),
        os.environ.get("EMAIL_APP_PASSWORD"),
        "smtp.mail.ru",
        "imap.mail.ru",
    )

    failed = email_client.send_email_to_mailing_list(recipients, email_content)

    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=wait_message.message_id
    )
    await query.message.reply_text("Письма отправлены")

    if len(failed):
        await query.message.reply_text(f"Не удалось отправить писем: {len(failed)}")
        await query.message.reply_text(", ".join(failed))

    if context.user_data.get("send_message_id"):
        await context.bot.edit_message_reply_markup(
            chat_id=query.message.chat_id,
            message_id=context.user_data["send_message_id"],
            reply_markup=None,
        )
    context.user_data.clear()
