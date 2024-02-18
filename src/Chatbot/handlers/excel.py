from telegram import Update
from telegram.ext import ContextTypes
import os

from .jobs import fetch_registrations
from Chatbot.excel import generate_workbook


async def generate_excel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    registrations = await fetch_registrations(update, context)

    await update.message.reply_text("Генерация Excel-файла...")
    filename = generate_workbook(registrations)
    await update.message.reply_document(
        document=open(filename, "rb"), filename=filename
    )
    os.remove(filename)
