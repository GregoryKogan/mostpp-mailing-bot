import logging
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ApplicationBuilder,
)

from Chatbot.middleware import middleware
from Chatbot.handlers import (
    meaningless,
    help_command,
    start,
    registrations,
    get_logs,
    clear_logs,
    callback_query,
    generate_excel,
    plaintext,
)
import config


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log" if config.MODE == "PROD" else None,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main():
    application = (
        ApplicationBuilder()
        .token(os.environ.get("BOT_TOKEN"))
        .concurrent_updates(False)
        .build()
    )

    application.add_handler(CommandHandler("start", middleware(start)))
    application.add_handler(CommandHandler("help", middleware(help_command)))
    application.add_handler(CommandHandler("registrations", middleware(registrations)))
    application.add_handler(
        CommandHandler("generate_excel", middleware(generate_excel))
    )

    application.add_handler(CommandHandler("get_logs", middleware(get_logs)))
    application.add_handler(CommandHandler("clear_logs", middleware(clear_logs)))

    application.add_handler(CallbackQueryHandler(middleware(callback_query)))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, middleware(plaintext))
    )

    application.add_handler(MessageHandler(filters.TEXT, middleware(meaningless)))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    load_dotenv(verbose=True, override=True)
    main()
