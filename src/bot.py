import logging
from time import sleep
from dotenv import load_dotenv
import os

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ApplicationBuilder,
)

from middleware import middleware
from handlers import meaningless, help_command, start, registrations, callback_query

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main():
    application = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", middleware(start)))
    application.add_handler(CommandHandler("help", middleware(help_command)))
    application.add_handler(CommandHandler("registrations", middleware(registrations)))

    application.add_handler(CallbackQueryHandler(middleware(callback_query)))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, middleware(meaningless))
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    load_dotenv(verbose=True, override=True)
    main()
