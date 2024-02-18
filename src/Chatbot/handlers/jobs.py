from telegram import Update
from telegram.ext import ContextTypes
import os

from Chatbot.Cache import Cache
from Mailing.EmailReadingClient import EmailReadingClient
from EventManagement.EventManager import EventManager
from WebScraping.EventScraper import EventScraper, EventData
import config


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from .callback import CallbackType

    print(CallbackType.EVENT_INFO_BEFORE_SENDING_CONFIRMATIONS.name)
    print(CallbackType.EVENT_INFO_BEFORE_SENDING_THANKS)
    print(CallbackType.EVENT_REGISTRATIONS.value)

    await update.message.reply_text("Test")


async def fetch_registrations(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> any:
    cache = Cache()
    if cache.has_key("registrations"):
        return cache.get("registrations")

    if update.message:
        wait_message = await update.message.reply_text(
            "Обновление регистраций...\nЭто может занять некоторое время."
        )
    elif update.callback_query:
        wait_message = await update.callback_query.message.reply_text(
            "Обновление регистраций...\nЭто может занять некоторое время."
        )

    email_client = EmailReadingClient(
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

    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=wait_message.message_id
    )

    return cache.get("registrations")


async def scrape_event_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE, event: str
) -> EventData:
    if update.message:
        wait_message = await update.message.reply_text(
            "Получение информации о мероприятии с официального сайта...\nЭто может занять некоторое время."
        )
    elif update.callback_query:
        wait_message = await update.callback_query.message.reply_text(
            "Получение информации о мероприятии с официального сайта...\nЭто может занять некоторое время."
        )

    scraper = EventScraper(
        config.EVENTS_BASE_URL,
        config.FUTURE_EVENTS_PAGE_URL,
        config.PAST_EVENTS_PAGE_URL,
    )

    data = scraper.get_event_data(event)

    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=wait_message.message_id
    )

    return data


async def get_event_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE, event: str
) -> EventData:
    cache = Cache()
    if cache.has_key(f"{event}-data"):
        return cache.get(f"{event}-data")

    data = await scrape_event_data(update, context, event)
    cache.store(f"{event}-data", data, config.EVENT_DATA_CACHE_LIFETIME)

    return cache.get(f"{event}-data")


def update_event_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE, event: str, data: EventData
) -> None:
    cache = Cache()
    cache.store(f"{event}-data", data, config.EVENT_DATA_CACHE_LIFETIME)
