import logging
import pathlib
import re
from asyncio import sleep
from random import randint

from pytz import UTC
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)
pattern = re.compile("авито", re.IGNORECASE | re.MULTILINE | re.UNICODE)


async def nice_ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and pattern.search(update.message.text):
        chat = update.effective_chat
        logger.debug("В группе %s (%s) опять срётся про Авито", chat.username, chat.id)

        await sleep(randint(1, 60))
        await update.message.reply_text("Может, хватит уже про Авито?")
