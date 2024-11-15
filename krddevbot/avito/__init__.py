import logging
import re
from asyncio import sleep
from random import randint, random

from pytz import UTC
from datetime import datetime

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

from krddevbot.application import KrdDevBotApplication

logger = logging.getLogger(__name__)
pattern_avito = re.compile("авито|avito|@vito|@вито|aвито", re.IGNORECASE | re.MULTILINE | re.UNICODE)


def your_lucky(probability: float) -> bool:
    return random() < probability


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
                duration=30 * 60,
            )
            await update.message.reply_text(
                f"Пользователь {lucky_user} призвал Авито. Спас-бросок 4d20: {result4d20}. Промах! Бан на пол часа."
                )
        elif your_lucky(0.05):
            await mute_user(
                context=context,
                user_id=user.id,
                chat_id=chat.id,
                duration=5 * 60,
            )
            await update.message.reply_text(
                f"Пользователь {lucky_user} призвал Авито. Спас-бросок 4d20: {result4d20}. Промах! Бан на пять минут."
                )
        else:
            await update.message.reply_text("Может, хватит уже про Авито?")


def init(application: KrdDevBotApplication):
    application.messages.append(nice_ban)
