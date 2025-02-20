import logging
import re
from random import randint

from pytz import UTC
from datetime import datetime

from telegram import Update, ChatPermissions
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from krddevbot import settings
from krddevbot.application import KrdDevBotApplication
from krddevbot.messages import send_garbage_message, md

logger = logging.getLogger(__name__)
pattern_avito = re.compile(r'(\A|\W)("|avito|@vito|@вито|авито|")(\Z|\b)', re.IGNORECASE | re.MULTILINE | re.UNICODE)

ban_permissions = ChatPermissions(
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


def get_dices() -> list[int]:
    count, value = settings.AVITO_DICES.split("d")
    return [randint(1, int(value)) for _ in range(int(count))]


async def mute_user(context: ContextTypes.DEFAULT_TYPE, user_id: int, chat_id: int, duration: int) -> None:
    now_utc = datetime.now(UTC)
    unix_time = int(now_utc.timestamp())

    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ban_permissions,
        until_date=unix_time+duration,
    )


async def nice_ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and pattern_avito.search(update.message.text):
        chat = update.effective_chat
        user = update.message.from_user
        logger.debug("В группе %s (%s) опять срётся про Авито", chat.username, chat.id)

        dices = get_dices()

        result4d20 = ", ".join([str(dice) for dice in dices])
        lucky_user = f"@{user.username}" if user.username else f"#{user.id}"
        message = f"Пользователь {lucky_user} призвал Авито. Спас-бросок 4d20: {result4d20}."

        if sum(dices) <= settings.AVITO_THRESHOLD:
            if sum(dices) == len(dices):
                minutes = 30
                message += " Крит! Бан на полчаса."
            else:
                minutes = 5
                message += " Промах! Бан на 5 минут."
            await mute_user(
                context=context,
                user_id=user.id,
                chat_id=chat.id,
                duration=minutes * 60,
            )
        else:
            message += " Успех!"
        await send_garbage_message(context, chat_id=update.message.chat_id, text=md(message), parse_mode=ParseMode.MARKDOWN_V2, message_timeout_seconds=10)


def init(application: KrdDevBotApplication):
    application.messages.append(nice_ban)
