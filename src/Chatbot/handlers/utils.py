from telegram import Update
from telegram.ext import ContextTypes


async def delete_last_confirmation_message(
    context: ContextTypes.DEFAULT_TYPE, chat_id: int
) -> None:
    if "last_confirmation_message" in context.user_data:
        await context.bot.delete_message(
            chat_id=chat_id, message_id=context.user_data["last_confirmation_message"]
        )
        del context.user_data["last_confirmation_message"]
