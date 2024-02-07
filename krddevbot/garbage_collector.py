import logging

from functools import partial

from telegram import Message
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from krddevbot import settings

logger = logging.getLogger(__name__)


def job(context: ContextTypes.DEFAULT_TYPE, message: Message):
    """Creates new job for run garbage collector task with specified message after timeout"""
    context.job_queue.run_once(
        callback=partial(_gc_task, chat_id=message.chat_id, message_id=message.message_id),
        when=settings.GARBAGE_COLLECTOR_RUN_TASK_SECONDS,
        name=f"_gc_task_{message.chat_id}_{message.message_id}",
    )


async def _gc_task(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    """Remove garbage message from chat"""
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramError as exc:
        if exc.message == "Message to delete not found":
            logger.info(f"{exc.message} chat_id={chat_id} message_id={message_id}")
        else:
            raise exc
