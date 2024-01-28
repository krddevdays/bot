import logging
from typing import Optional, Tuple

import httpx
import random
from telegram import ChatMember, ChatMemberUpdated, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from krddevbot import settings
from krddevbot.antispam.constance import EMOJI, GREETING_MESSAGE_TEMPLATE, TIMEOUT_FAIL_MESSAGE_TEMPLATE, \
    TIMEOUT_OK_MESSAGE_TEMPLATE
from krddevbot.antispam.storage import CHECKING_MEMBERS

from krddevbot.message_formatter import md

logger = logging.getLogger(__name__)

def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
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


async def check_in_darkbyte(user_id):
    response = httpx.get(f"https://spam.darkbyte.ru/?a={user_id}")
    data = response.json()
    should_ban = data["banned"] or data["spam_factor"] > 30
    logger.info("%s => %s", response.content.decode(), should_ban)
    return should_ban


async def emoji_challenge(context, user, chat):
    challenge_text = random.choice(list(EMOJI.keys()))

    sent_msg = await chat.send_message(
        md(
            GREETING_MESSAGE_TEMPLATE,
            username=user,
            challenge_text=challenge_text,
            timeout=settings.EMOJI_TIMEOUT_SECONDS
        ),
        parse_mode=ParseMode.MARKDOWN_V2
    )

    key = f'{user.id}_{chat.id}_{sent_msg.id}'
    CHECKING_MEMBERS[key] = EMOJI[challenge_text]

    context.job_queue.run_once(
        kick_if_time_is_over,
        settings.EMOJI_TIMEOUT_SECONDS,
        user_id=user.id,
        chat_id=chat.id,
        message_id=sent_msg.id,
        data={
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name
        }
    )


async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result

    # Verifying the user is a new member
    if was_member or not is_member:
        return

    user = update.chat_member.new_chat_member.user

    if settings.DARKBYTE_ENABLED:
        if await check_in_darkbyte(user.id):
            await update.chat_member.chat.ban_member(user.id, revoke_messages=True)
            return

    await emoji_challenge(context, user, update.effective_chat)


async def kick_if_time_is_over(context: ContextTypes.DEFAULT_TYPE):
    key = f'{context.job.user_id}_{context.job.chat_id}_{context.job.message_id}'
    if key in CHECKING_MEMBERS:
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text=md(TIMEOUT_FAIL_MESSAGE_TEMPLATE, username=context.job.data),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await context.bot.delete_message(chat_id=context.job.chat_id, message_id=context.job.message_id)
        del CHECKING_MEMBERS[key]

        # kick, not ban
        await context.bot.ban_chat_member(
            chat_id=context.job.chat_id,
            user_id=context.job.user_id,
            revoke_messages=True
        )
        await context.bot.unban_chat_member(
            chat_id=context.job.chat_id,
            user_id=context.job.user_id
        )
    else:
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text=md(TIMEOUT_OK_MESSAGE_TEMPLATE, username=context.job.data),
            parse_mode=ParseMode.MARKDOWN_V2
        )
