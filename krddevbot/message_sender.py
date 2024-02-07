from telegram import Message
from telegram.ext import ContextTypes

from krddevbot import settings
from krddevbot import garbage_collector


async def send_garbage_message(context: ContextTypes.DEFAULT_TYPE, message_timeout_seconds=settings.GARBAGE_MESSAGE_TIMEOUT_SECONDS, **kwargs) -> Message:
    message = await context.bot.send_message(**kwargs)

    garbage_collector.job(context, message, message_timeout_seconds)

    return message
