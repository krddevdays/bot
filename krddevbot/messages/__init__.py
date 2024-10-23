import logging
import pathlib
import re
from random import randint, random
from asyncio import sleep
from datetime import datetime, UTC

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

from ..antispam.storage import CHECKING_MEMBERS

logger = logging.getLogger(__name__)
pattern_tander = re.compile("тандер", re.IGNORECASE | re.MULTILINE | re.UNICODE)
pattern_avito = re.compile("авито|avito|@vito|@вито|девито|devito", re.IGNORECASE | re.MULTILINE | re.UNICODE)


def your_lucky(probability: float) -> bool:
    return random() < probability


def is_checking_member(prefix: str) -> str | None:
    for item in CHECKING_MEMBERS:
        if item.startswith(prefix):
            return item
    return None


async def mute_user(context: ContextTypes.DEFAULT_TYPE, user_id: int, chat_id: int, duration: int) -> None:
    now_utc = datetime.now(UTC)
    unix_time = int(now_utc.timestamp())

    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_send_audios=False,
        can_send_documents=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
    )

    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=permissions,
        until_date=unix_time+duration,
    )


async def track_user_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    member = f"{update.message.from_user.id}_{update.effective_chat.id}"

    if update.message and is_checking_member(member):
        await update.message.delete()
    else:
        await days_without_mention(update=update, context=context)
        await nice_ban(update=update, context=context)


async def days_without_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and pattern_tander.search(update.message.text):
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


async def nice_ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and pattern_avito.search(update.message.text):
        chat = update.effective_chat
        user = update.message.from_user
        logger.debug("В группе %s (%s) опять срётся про Авито", chat.username, chat.id)

        await sleep(randint(1, 60))

        results = []
        
        for _ in range(4):
            results.append(str(randint(1, 20)))
        
        result4d20 = ", ".join(results)

        lucky_user = f"@{user.username}" if user.username else f"#{user.id}"
        
        if your_lucky(0.005):
            await mute_user(
                context=context,
                user_id=user.id,
                chat_id=chat.id,
                duration=30*60,
            )
            await update.message.reply_text(f"Пользователь {lucky_user} призвал Авито. Спас-бросок 4d20: {result4d20}. Промах! Бан на пол часа.")
        elif your_lucky(0.05):
            await mute_user(
                context=context,
                user_id=user.id,
                chat_id=chat.id,
                duration=5*60,
            )
            await update.message.reply_text(f"Пользователь {lucky_user} призвал Авито. Спас-бросок 4d20: {result4d20}. Промах! Бан на пять минут.")
        else:
            await update.message.reply_text("Может, хватит уже про Авито?")
