from telegram import Message
from telegram.ext import ContextTypes

from krddevbot import settings


def job(context: ContextTypes.DEFAULT_TYPE, message: Message):
    """Creates new job for run garbage collector task with specified message after timeout"""
    context.job_queue.run_once(
        _gc_task,
        settings.GARBAGE_COLLECTOR_RUN_TASK_SECONDS,
        data={
            "chat_id": message.chat_id,
            "message_id": message.message_id,
        },
    )


async def _gc_task(context: ContextTypes.DEFAULT_TYPE):
    """Remove garbage message from chat"""
    chat_id = context.job.data["chat_id"]
    message_id = context.job.data["message_id"]

    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
