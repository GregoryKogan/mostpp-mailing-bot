import os
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


def allowed(update: Update) -> bool:
    return update.effective_user.id in map(
        int, os.environ.get("ALLOWED_USERS").split(",")
    )


def middleware(handler_func: callable) -> callable:
    async def wrap(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not allowed(update):
            await update.message.reply_text("You are not allowed to use this bot.")
            return
        await handler_func(update, context)

    return wrap
