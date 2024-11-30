import logging

from functools import partial
from typing import Optional

from telegram import Message, User
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from telegram.helpers import escape_markdown

from krddevbot import settings

logger = logging.getLogger(__name__)


def job(context: ContextTypes.DEFAULT_TYPE, message: Message, message_timeout_seconds: int) -> None:
    """Creates new job for run garbage collector task with specified message after timeout"""
    context.job_queue.run_once(
        callback=partial(_gc_task, chat_id=message.chat_id, message_id=message.message_id),
        when=message_timeout_seconds,
        name=f"_gc_task_{message.chat_id}_{message.message_id}_{message_timeout_seconds}s",
    )


async def _gc_task(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int) -> None:
    """Remove garbage message from chat"""
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramError as exc:
        if exc.message == "Message to delete not found":
            logger.info(f"{exc.message} chat_id={chat_id} message_id={message_id}")
        else:
            raise exc


async def send_garbage_message(context: ContextTypes.DEFAULT_TYPE, message_timeout_seconds=settings.GARBAGE_MESSAGE_TIMEOUT_SECONDS, **kwargs) -> Message:
    message = await context.bot.send_message(**kwargs)
    job(context, message, message_timeout_seconds)
    return message


MAGIC_USER_STRING = "SOMEMAGICSTRING"


def md(template: str, user: Optional[dict | User] = None, **kwargs) -> str:
    if user:
        kwargs["username"] = MAGIC_USER_STRING

    result = escape_markdown(template.format(**kwargs), version=2)
    if user:
        if not isinstance(user, User):
            user = User(**user)
        result = result.replace(MAGIC_USER_STRING, user.mention_markdown_v2(user.username))
    return result
