import logging
import pathlib
import re
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ContextTypes

from krddevbot.application import KrdDevBotApplication

logger = logging.getLogger(__name__)
pattern_tander = re.compile(r'(\A|\b)тандер(\Z|\b)', re.IGNORECASE | re.MULTILINE | re.UNICODE)


async def days_without_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and pattern_tander.search(update.message.text):
        chat = update.effective_chat
        logger.debug("В группе %s (%s) вспомнили Тандер", chat.username, chat.id)
        file_path = pathlib.Path(f"tander/{abs(chat.id)}")
        if file_path.is_file():
            diff = datetime.now(timezone.utc) - datetime.fromtimestamp(file_path.stat().st_mtime, timezone.utc)
            logger.debug("В последний раз это было %s назад", diff)
            if diff.days > 0:
                file_path.touch()
                await update.message.reply_text(f"Дней без упоминания Тандера: {diff.days}")
        else:
            logger.debug("Включён Тандер для группы %s (%s)", chat.username, chat.id)
            file_path.touch()


def init(application: KrdDevBotApplication):
    application.messages.append(days_without_mention)
