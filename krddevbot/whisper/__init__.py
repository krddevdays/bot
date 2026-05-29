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
    if not message or not message.voice:
        return

    if not settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY не задан, голосовое пропущено")
        return

    try:
        tg_file = await context.bot.get_file(message.voice.file_id)
        audio = await tg_file.download_as_bytearray()

        data = {"model": settings.GROQ_MODEL, "response_format": "json"}
        if settings.GROQ_LANGUAGE:
            data["language"] = settings.GROQ_LANGUAGE

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                files={"file": ("voice.ogg", bytes(audio), "audio/ogg")},
                data=data,
            )
            response.raise_for_status()
            text = response.json().get("text", "").strip()
    except Exception:
        logger.exception("Не удалось распознать голосовое")
        return

    if not text:
        return

    await message.reply_text(f"🎤 {text}")


def init(application: KrdDevBotApplication):
    application.add_handler(MessageHandler(filters.VOICE, transcribe))
