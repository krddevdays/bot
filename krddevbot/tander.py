import pathlib
import re
from datetime import datetime, UTC

from telegram import Update
from telegram.ext import ContextTypes


pattern = re.compile("тандер", re.IGNORECASE | re.MULTILINE | re.UNICODE)


async def days_without_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if pattern.search(update.message.text):
        file_path = pathlib.Path(f'tander/{abs(update.effective_chat.id)}')
        if file_path.is_file():
            diff = datetime.now(UTC) - datetime.fromtimestamp(file_path.stat().st_mtime, UTC)
            if diff.days > 0:
                file_path.touch()
                await update.message.reply_text(f"Дней без упоминания Тандера: {diff.days}")
        else:
            file_path.touch()
