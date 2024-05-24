import os
import json
import logging

from functools import partial

from telegram import Message
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from krddevbot import settings

logger = logging.getLogger(__name__)

GC_JOBS = {}


async def init_garbage_collector(context: ContextTypes.DEFAULT_TYPE):
    """Restores all gc jobs from file and runs tasks"""
    _restore_gc_jobs()

    for gc_msg in list(GC_JOBS.keys()):
        chat_id, _, message_id = gc_msg.partition("_")

        del GC_JOBS[gc_msg]

        await _gc_task(context, chat_id, message_id)

    _dump_gc_jobs()


def _save_gc_job(chat_id, message_id):
    GC_JOBS[f"{chat_id}_{message_id}"] = True
    _dump_gc_jobs()


def _remove_gc_job(chat_id, message_id):
    key = f"{chat_id}_{message_id}"
    if key not in GC_JOBS:
        return

    del GC_JOBS[key]
    _dump_gc_jobs()


def _dump_gc_jobs():
    global GC_JOBS

    try:
        with open(settings.GC_JOBS_BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(GC_JOBS, f, sort_keys=True, indent=4)
    except Exception as ex:
        logger.error(f"storage._dump_gc_jobs: {ex}")


def _restore_gc_jobs():
    global GC_JOBS

    try:
        if not os.path.exists(settings.GC_JOBS_BACKUP_FILE):
            return

        with open(settings.GC_JOBS_BACKUP_FILE, "r") as f:
            data = f.read()
            if not data:
                return

            GC_JOBS = json.loads(data)
    except Exception as ex:
        logger.error(f"storage.restore_gc_jobs: {ex}")


def job(context: ContextTypes.DEFAULT_TYPE, message: Message, message_timeout_seconds: int):
    """Creates new job for run garbage collector task with specified message after timeout"""

    _save_gc_job(chat_id=message.chat_id, message_id=message.message_id)

    context.job_queue.run_once(
        callback=partial(_gc_task, chat_id=message.chat_id, message_id=message.message_id),
        when=message_timeout_seconds,
        name=f"_gc_task_{message.chat_id}_{message.message_id}_{message_timeout_seconds}s",
    )


async def _gc_task(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    """Remove garbage message from chat"""
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        _remove_gc_job(chat_id=chat_id, message_id=message_id)
    except TelegramError as exc:
        if exc.message == "Message to delete not found":
            logger.info(f"{exc.message} chat_id={chat_id} message_id={message_id}")
        else:
            raise exc
