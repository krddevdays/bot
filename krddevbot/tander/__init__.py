import logging
import pathlib
import re
from pytz import UTC
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)
pattern = re.compile("тандер", re.IGNORECASE | re.MULTILINE | re.UNICODE)


async def days_without_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and pattern.search(update.message.text):
        chat = update.effective_chat
        logger.debug("В группе %s (%s) вспомнили Тандер", chat.username, chat.id)
        file_path = pathlib.Path(f"tander/{abs(chat.id)}")
        if file_path.is_file():
            diff = datetime.now(UTC) - datetime.fromtimestamp(file_path.stat().st_mtime, UTC)
            logger.debug("В последний раз это было %s назад", diff)
            if diff.days > 0:
                file_path.touch()
                await update.message.reply_text(f"Дней без упоминания Тандера: {diff.days}")
        else:
            logger.debug("Включён Тандер для группы %s (%s)", chat.username, chat.id)
            file_path.touch()
