from typing import Optional, Tuple

import httpx
import random
from telegram import ChatMember, ChatMemberUpdated, Update
from telegram.constants import ParseMode

from telegram.ext import ContextTypes

from krddevbot.service import get_md_user_name

# Feature Flags Inc. & Config Brothers
DARKBYTE_ENABLED = True
BAN_ENABLED = True
BAN_TIMEOUT_SECONDS = 60

# Main cluster database 100500 pods in k8s required
CHECKING_MEMBERS = {}

# Secret store
EMOJI = {
    "рукой": "👍👎👏🙏👌🖕🤝✍️💅",
    "огнем": "🔥",
    "сердцем": "❤️💘💔❤️‍🔥",
    "лицом": "🥰😁🤔🤯😱🤬😢🤩🤮🤡🥱🥴😍🌚🤣🤨😐😈😴😭🤓😇😨🤗🎅🤪😘😎😡",
    "животным": "🕊🐳🙈🙉🦄🙊👾☃️",
    "едой": "🍓🌭🍌🍾💊🎃",
}

GREETING_MESSAGE_TEMPLATE = """
Уважаемый {username}
Добро пожаловать в чаты сообщества krd\\.dev\\!

Подтвердите, что вы кожаный мешок, поставив эмодзи с {challenge_text} из стандартного набора этому сообщению\\.

У вас {timeout} секунд\\.\\.\\.
"""

TIMEOUT_FAIL_MESSAGE_TEMPLATE = 'Timeout\\! Лови BANAN 🍌, {username}\\!'
TIMEOUT_OK_MESSAGE_TEMPLATE = 'Проверка пройдена успешно 👍, просьба не сорить и убирать за собой, {username}\\!'

CHALLENGE_OK_MESSAGE_TEMPLATE = 'Добро пожаловать, {username}\\!'
CHALLENGE_FAIL_MESSAGE = 'Фатальная ошибка\\! Лови BANAN 🍌'


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

    # Verifying the user is a new member
    if was_member or not is_member:
        return

    user = update.chat_member.new_chat_member.user

    if DARKBYTE_ENABLED:
        response = httpx.get(f"https://spam.darkbyte.ru/?a={user.id}")
        data = response.json()
        should_ban = data["banned"] or data["spam_factor"] > 30
        message = f"`{response.content.decode()}` \\=\\> {should_ban}"
        await update.effective_chat.send_message(message, parse_mode=ParseMode.MARKDOWN_V2)

        if should_ban:
            if BAN_ENABLED:
                await update.chat_member.chat.ban_member(user.id, revoke_messages=True)
            return

    challenge_text = random.choice(list(EMOJI.keys()))

    message = GREETING_MESSAGE_TEMPLATE.format(username=get_md_user_name(user),
                                               challenge_text=challenge_text,
                                               timeout=BAN_TIMEOUT_SECONDS)

    sent_msg = await update.effective_chat.send_message(message, parse_mode=ParseMode.MARKDOWN_V2)

    CHECKING_MEMBERS[user.id] = {
        'message_id': sent_msg.id,
        'emoji': EMOJI[challenge_text],
    }

    context.job_queue.run_once(ban_if_time_is_over, BAN_TIMEOUT_SECONDS,
                               user_id=user.id,
                               chat_id=update.effective_chat.id,
                               data={'id': user.id,
                                     'username': user.username,
                                     'first_name': user.first_name})


async def ban_if_time_is_over(context: ContextTypes.DEFAULT_TYPE):
    if context.job.user_id in CHECKING_MEMBERS:
        await context.bot.send_message(chat_id=context.job.chat_id,
                                       text=TIMEOUT_FAIL_MESSAGE_TEMPLATE.format(
                                           username=get_md_user_name(context.job.data)),
                                       parse_mode=ParseMode.MARKDOWN_V2
                                       )
        if BAN_ENABLED:
            await context.bot.ban_chat_member(chat_id=context.job.chat_id,
                                              user_id=context.job.user_id,
                                              revoke_messages=True)
    else:
        await context.bot.send_message(chat_id=context.job.chat_id,
                                       text=TIMEOUT_OK_MESSAGE_TEMPLATE.format(
                                           username=get_md_user_name(context.job.data)),
                                       parse_mode=ParseMode.MARKDOWN_V2)
