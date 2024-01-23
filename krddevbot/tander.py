import logging
import pathlib
import re
from datetime import datetime, UTC
import tempfile

from telegram import Update
from telegram.ext import ContextTypes


pattern = re.compile("тандер", re.IGNORECASE | re.MULTILINE | re.UNICODE)


async def days_without_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger = logging.getLogger(__name__)
    logger.info("Tander pattern found.")
    if pattern.search(str(update.message.text)):
        file_path = pathlib.Path(f'{tempfile.gettempdir()}/{__name__}__tander_{abs(update.effective_chat.id)}')
        logger.info(f"Tander lock file: {file_path}")
        if file_path.is_file():
            diff = datetime.now(UTC) - datetime.fromtimestamp(file_path.stat().st_mtime, UTC)
            if diff.days > 0:
                file_path.touch()
                await update.message.reply_text(f"Дней без упоминания Тандера: {diff.days}")
        else:
            file_path.touch()
            await update.message.reply_text(f"Дней без упоминания Тандера: 0")
