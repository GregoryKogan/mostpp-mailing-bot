from telegram import Update
from telegram.ext import ContextTypes

from .jobs import fetch_registrations
from Chatbot.Cache import Cache
from Chatbot.CallbackHasher import CallbackHasher
from EmailGeneration.EmailGeneration import EventEmailGenerator
from WebScraping.EventScraper import EventScraper
import config


async def send_confirmation_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    if "last_confirmation_message" in context.user_data:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_confirmation_message"],
        )
        del context.user_data["last_confirmation_message"]

    registrations = await fetch_registrations(update, context)

    event = CallbackHasher.unhash_callback(
        query.data.split("$")[1], list(registrations.keys())
    )

    await query.message.reply_text(
        "Получение информации о мероприятии с официального сайта...\nЭто может занять некоторое время."
    )

    scraper = EventScraper(
        config.EVENTS_BASE_URL,
        config.FUTURE_EVENTS_PAGE_URL,
        config.PAST_EVENTS_PAGE_URL,
    )

    event_data = scraper.get_event_data(event)
    if event_data is None:
        await query.message.reply_text(
            f'Не удалось найти информацию о мероприятии "{event}". Письма <b>не</b> были отправлены.',
            parse_mode=constants.ParseMode.HTML,
        )
        return

    email_templates = EventEmailGenerator.read_templates(
        config.PRE_EVENT_EMAIL_TEMPLATE_PATH,
        config.PRE_EVENT_EMAIL_SUBJECT_TEMPLATE_PATH,
        config.POST_EVENT_EMAIL_TEMPLATE_PATH,
        config.POST_EVENT_EMAIL_SUBJECT_TEMPLATE_PATH,
    )
    email_generator = EventEmailGenerator(*email_templates)
    email_content = email_generator.generate_pre_event_email(event_data)

    await query.message.reply_text(
        "Всем зарегистрированным на мероприятие пользователям будет отправлено письмо: "
    )
    await query.message.reply_text(
        str(email_content),
        parse_mode=constants.ParseMode.HTML,
        disable_web_page_preview=True,
    )
    await query.message.reply_text(
        "Внимательно проверьте письмо перед отправкой.\nСгенерировано ли оно верно?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Да, отправить",
                        callback_data=f"gycon${CallbackHasher.hash_callback(event)}",
                    ),
                    InlineKeyboardButton(
                        "Нет, изменить",
                        callback_data=f"gnconf${CallbackHasher.hash_callback(event)}",
                    ),
                ]
            ]
        ),
    )


async def cancel_sending_confirmation_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    msg_text = "Письма-напоминания <b>не</b> были отправлены."

    if "last_confirmation_message" in context.user_data:
        await context.bot.edit_message_text(
            msg_text,
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_confirmation_message"],
            parse_mode=constants.ParseMode.HTML,
        )
        del context.user_data["last_confirmation_message"]
    else:
        await query.message.reply_text(msg_text)


async def send_thankful_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    msg_text = "Возможность отправки писем благодарности за участие в мероприятии пока не реализована."

    if "last_confirmation_message" in context.user_data:
        await context.bot.edit_message_text(
            msg_text,
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_confirmation_message"],
        )
        del context.user_data["last_confirmation_message"]
    else:
        await query.message.reply_text(msg_text)


async def cancel_sending_thankful_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    msg_text = "Письма благодарности <b>не</b> были отправлены."

    if "last_confirmation_message" in context.user_data:
        await context.bot.edit_message_text(
            msg_text,
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_confirmation_message"],
            parse_mode=constants.ParseMode.HTML,
        )
        del context.user_data["last_confirmation_message"]
    else:
        await query.message.reply_text(msg_text)
