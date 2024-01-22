from typing import Optional, Tuple

import httpx
from telegram import ChatMember, ChatMemberUpdated, Update
from telegram.constants import ParseMode

from telegram.ext import ContextTypes


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


async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    if not was_member and is_member:
        response = httpx.get(f"https://spam.darkbyte.ru/?a={update.chat_member.new_chat_member.user.id}")
        data = response.json()
        should_ban = data["banned"] or data["spam_factor"] > 30
        message = f"`{response.content.decode()}` \=\> {should_ban}"
        await update.effective_chat.send_message(message, parse_mode=ParseMode.MARKDOWN_V2)

        if should_ban:
            await update.chat_member.chat.ban_member(update.chat_member.new_chat_member.user.id, revoke_messages=True)
