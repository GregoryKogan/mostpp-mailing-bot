from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os

import config
from EventManager import EventManager, EmailClient
from CallbackHasher import CallbackHasher
from Cache import Cache


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Здравствуйте, {user.full_name}!\n"
        "Это бот для управления регистрациями на мероприятия.\n"
        "Для получения справки используйте команду /help."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "<b>Для этого бота доступны следующие команды:</b>\n"
        "/start - начать работу с ботом\n"
        "/help - получить справку\n"
        "/registrations - просмотреть регистрации на мероприятия\n\n"
        "<b>Конфигурация:</b>\n"
        f" - Рабочий email: \n{os.environ.get('EMAIL_ADDRESS')}\n"
        f" - Email уведомителя: \n{os.environ.get('NOTIFIER_ADDRESS')}\n"
        f" - Максимальное время регистрации: \n{config.REGISTRATION_PERIOD} мес.\n"
        f" - Ключевые слова в теме письма: \n<code>{', '.join(config.REGISTRATION_SUBJECT_KEYWORDS)}</code>\n"
        f" - Время жизни кеша регистраций: \n{config.REGISTRATIONS_CACHE_LIFETIME} сек.\n\n"
        "Тех. поддержка: @GregoryKogan\n",
        parse_mode=constants.ParseMode.HTML,
    )


async def meaningless(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"I don't know this command: '{update.message.text}'"
    )


async def registrations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    fetch_registrations()

    cache = Cache()
    registrations = cache.get("registrations")
    msg_text = "Registrations:\n"
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


async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("event$"):
        await event_callback_query(update, context, query)
    elif query.data.startswith("conf$"):
        await confirmation_callback_query(update, context, query)
    elif query.data.startswith("thank$"):
        await thanks_callback_query(update, context, query)
    elif query.data.startswith("yconf$"):
        await send_confirmation_emails(update, context, query)
    elif query.data.startswith("nconf$"):
        await cancel_sending_confirmation_emails(update, context, query)
    elif query.data.startswith("ythan$"):
        await send_thankful_emails(update, context, query)
    elif query.data.startswith("nthan$"):
        await cancel_sending_thankful_emails(update, context, query)
    else:
        await query.message.reply_text(f"Unknown callback query: {query.data}")


async def event_callback_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    fetch_registrations()
    cache = Cache()
    registrations = cache.get("registrations")

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
                        "Send confirmation",
                        callback_data=f"conf${CallbackHasher.hash_callback(event)}",
                    ),
                    InlineKeyboardButton(
                        "Send thanks",
                        callback_data=f"thank${CallbackHasher.hash_callback(event)}",
                    ),
                ]
            ]
        ),
    )


async def confirmation_callback_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    fetch_registrations()
    cache = Cache()
    registrations = cache.get("registrations")

    event = CallbackHasher.unhash_callback(
        query.data.split("$")[1], list(registrations.keys())
    )

    msg_text = "".join(
        f"{registration.email}\n" for registration in registrations[event]
    )
    msg_text += f"\n Are you sure you want to send confirmation emails for '{event}' to all these people?"
    confirmation_message = await query.message.reply_text(
        msg_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Yes",
                        callback_data=f"yconf${CallbackHasher.hash_callback(event)}",
                    ),
                    InlineKeyboardButton(
                        "No",
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
    fetch_registrations()
    cache = Cache()
    registrations = cache.get("registrations")

    event = CallbackHasher.unhash_callback(
        query.data.split("$")[1], list(registrations.keys())
    )

    msg_text = "".join(
        f"{registration.email}\n" for registration in registrations[event]
    )
    msg_text += f"\n Are you sure you want to send thankful emails for '{event}' to all these people?"
    confirmation_message = await query.message.reply_text(
        msg_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Yes",
                        callback_data=f"ythan${CallbackHasher.hash_callback(event)}",
                    ),
                    InlineKeyboardButton(
                        "No",
                        callback_data=f"nthan${CallbackHasher.hash_callback(event)}",
                    ),
                ]
            ]
        ),
    )
    context.user_data["last_confirmation_message"] = confirmation_message.message_id


async def send_confirmation_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    await query.message.reply_text(
        "Sending confirmation emails feature is not yet implemented."
    )

    if "last_confirmation_message" in context.user_data:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_confirmation_message"],
        )
        del context.user_data["last_confirmation_message"]


async def cancel_sending_confirmation_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    await query.message.reply_text("Confirmation emails were not sent.")

    if "last_confirmation_message" in context.user_data:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_confirmation_message"],
        )
        del context.user_data["last_confirmation_message"]


async def send_thankful_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    await query.message.reply_text(
        "Sending thankful emails feature is not yet implemented."
    )

    if "last_confirmation_message" in context.user_data:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_confirmation_message"],
        )
        del context.user_data["last_confirmation_message"]


async def cancel_sending_thankful_emails(
    update: Update, context: ContextTypes.DEFAULT_TYPE, query: Update.callback_query
):
    await query.message.reply_text("Thankful emails were not sent.")

    if "last_confirmation_message" in context.user_data:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_confirmation_message"],
        )
        del context.user_data["last_confirmation_message"]


def fetch_registrations():
    cache = Cache()
    if cache.has_key("registrations"):
        return

    email_client = EmailClient(
        os.environ.get("EMAIL_ADDRESS"),
        os.environ.get("EMAIL_APP_PASSWORD"),
        "imap.mail.ru",
    )
    event_manager = EventManager(email_client, os.environ.get("NOTIFIER_ADDRESS"))
    cache.store(
        "registrations",
        event_manager.get_registrations(),
        config.REGISTRATIONS_CACHE_LIFETIME,
    )
