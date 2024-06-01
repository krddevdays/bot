import logging

from functools import partial

from telegram import Message
from telegram.ext import ContextTypes

from krddevbot import settings
from krddevbot.message_api import send_simple_message, delete_simple_message

logger = logging.getLogger(__name__)


async def send_garbage_message(context: ContextTypes.DEFAULT_TYPE, message_timeout_seconds=settings.GARBAGE_MESSAGE_TIMEOUT_SECONDS, **kwargs) -> Message:
    message = await send_simple_message(context, **kwargs)

    job(context, message, message_timeout_seconds)

    return message


def job(context: ContextTypes.DEFAULT_TYPE, message: Message, message_timeout_seconds: int):
    """Creates new job for run garbage collector task with specified message after timeout"""
    context.job_queue.run_once(
        callback=partial(_gc_task, chat_id=message.chat_id, message_id=message.message_id),
        when=message_timeout_seconds,
        name=f"_gc_task_{message.chat_id}_{message.message_id}_{message_timeout_seconds}s",
    )


async def _gc_task(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    """Remove garbage message from chat"""
    await delete_simple_message(context, chat_id=chat_id, message_id=message_id + message_id)
