import os
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import logging


def allowed(update: Update) -> bool:
    return update.effective_user.id in map(
        int, os.environ.get("ALLOWED_USERS").split(",")
    )


def middleware(handler_func: callable) -> callable:
    async def wrap(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info(
            f"User {update.effective_user.id} called {handler_func.__name__} handler"
        )
        if not allowed(update):
            logging.warning(f"User {update.effective_user.id} is not allowed")
            await update.message.reply_text("You are not allowed to use this bot.")
            return
        await handler_func(update, context)
        logging.info(
            f"User {update.effective_user.id} finished {handler_func.__name__} handler"
        )

    return wrap
