from telegram import Message
from telegram.ext import ContextTypes
from krddevbot import garbage_collector


async def send_garbage_message(context: ContextTypes.DEFAULT_TYPE, *args, **kwargs) -> Message:
    message = await context.bot.send_message(*args, **kwargs)

    garbage_collector.job(context, message)

    return message
