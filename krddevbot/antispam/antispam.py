import logging
import random
from asyncio import sleep
from typing import Optional, Tuple

import httpx
from telegram import User, Chat
from telegram import ChatMember, ChatMemberUpdated, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from krddevbot import settings

from .constance import (
    EMOJI,
    GREETING_MESSAGE_TEMPLATE,
    TIMEOUT_FAIL_MESSAGE_TEMPLATE,
)
from krddevbot.storage import CHECKING_MEMBERS
from ..messages import send_garbage_message, md

logger = logging.getLogger(__name__)


def _extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def _check_in_lols_bot(user_id: int) -> bool:
    """
    Sends a request to lols bot.
    If the response from lols bot has not arrived or the response code is not equal to 200 or user_id is not int,
    It returns that the user is not banned.
    """
    if not isinstance(user_id, int):
        return False

    should_ban = False
    client = httpx.AsyncClient(timeout=10)

    try:
        response = await client.get(f"https://api.lols.bot/account", params={"id": user_id})
    except httpx.TransportError as e:
        logger.error("httpx.{err_class}: cannot connect to lols bot".format(err_class=e.__class__.__name__))
    else:
        if response.status_code != 200:
            logger.error("lols bot return {status} code".format(status=response.status_code))
            return should_ban

        logger.info('lols response: %s', response.content.decode())
        data = response.json()
        should_ban = data["banned"]

    return should_ban


async def _emoji_challenge(context: ContextTypes.DEFAULT_TYPE, user: User, chat: Chat) -> None:
    challenge_text = random.choice(list(EMOJI.keys()))

    sent_msg = await send_garbage_message(
        context,
        chat_id=chat.id,
        text=md(
            GREETING_MESSAGE_TEMPLATE,
            user=user,
            challenge_text=challenge_text,
            timeout=settings.EMOJI_TIMEOUT_SECONDS,
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
        message_timeout_seconds=settings.EMOJI_TIMEOUT_SECONDS,
    )

    key = f"{user.id}_{chat.id}_{sent_msg.id}"
    CHECKING_MEMBERS[key] = EMOJI[challenge_text]

    context.job_queue.run_once(
        kick_if_time_is_over,
        settings.EMOJI_TIMEOUT_SECONDS,
        user_id=user.id,
        chat_id=chat.id,
        data={
            "user": user.to_dict(),
            "message_id": sent_msg.id,
        },
    )


async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = _extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result

    # Verifying the user is a new member
    if was_member or not is_member:
        return

    user = update.chat_member.new_chat_member.user

    if settings.LOLS_BOT_ENABLED:
        if await _check_in_lols_bot(user.id):
            await update.chat_member.chat.ban_member(user.id, revoke_messages=True)
            return

    await _emoji_challenge(context, user, update.effective_chat)


async def kick_if_time_is_over(context: ContextTypes.DEFAULT_TYPE) -> None:
    message_id = context.job.data["message_id"]
    user = context.job.data["user"]

    key = f"{context.job.user_id}_{context.job.chat_id}_{message_id}"

    if key not in CHECKING_MEMBERS:
        return

    # User reaction on message is timed out
    await send_garbage_message(
        context,
        chat_id=context.job.chat_id,
        text=md(TIMEOUT_FAIL_MESSAGE_TEMPLATE, user=user),
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    # kick, not ban
    await context.bot.unban_chat_member(chat_id=context.job.chat_id, user_id=context.job.user_id, only_if_banned=False)

    # some bots send message immediately after kick
    # I suppose it's some kind of race condition when kick was not propagated to all servers
    await sleep(10)
    del CHECKING_MEMBERS[key]


async def track_user_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prefix = f"{update.effective_message.from_user.id}_{update.effective_chat.id}"

    if update.message and any([x.startswith(prefix) for x in CHECKING_MEMBERS]):
        await update.message.delete()
