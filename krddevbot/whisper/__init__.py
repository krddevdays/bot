import logging

import httpx
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from krddevbot import settings
from krddevbot.application import KrdDevBotApplication

logger = logging.getLogger(__name__)

GROQ_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
REQUEST_TIMEOUT = 60.0


async def transcribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    voice = message.voice

    tg_file = await context.bot.get_file(voice.file_id)
    audio = await tg_file.download_as_bytearray()

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
            files={"file": ("voice.ogg", audio, "audio/ogg")},
            data={"model": settings.GROQ_MODEL, "language": "ru", "response_format": "json"},
        )

    if response.is_error:
        logger.error("Groq вернул %s для chat=%s: %s", response.status_code, message.chat_id, response.text)
        return

    text = response.json().get("text", "").strip()
    if text:
        await message.reply_text(f"🎤 {text}")


def init(application: KrdDevBotApplication):
    if not settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY не задан, whisper отключён")
        return

    application.add_handler(MessageHandler(filters.VOICE, transcribe))
