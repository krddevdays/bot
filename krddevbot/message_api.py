import logging
import asyncio

from telegram import Message
from telegram.ext import ContextTypes
from telegram.error import TelegramError, TimedOut

from krddevbot import settings

logger = logging.getLogger(__name__)


def retry_on_timeout(retry_times):
    def decorator(func):
        async def fn(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except TimedOut as exc:
                    attempt += 1
                    if attempt >= retry_times:
                        logger.error(f"{func.__name__}: {exc.message}: kwargs={kwargs} [mission failed]")
                        raise exc
                    logger.error(f"{func.__name__}: {exc.message}: kwargs={kwargs} attempt={attempt}")

                await asyncio.sleep(settings.BOT_ACTION_RETRY_SLEEP_SECONDS)

        return fn

    return decorator


@retry_on_timeout(settings.BOT_ACTION_RETRY_TIMES)
async def send_simple_message(context: ContextTypes.DEFAULT_TYPE, **kwargs) -> Message:
    return await context.bot.send_message(**kwargs)


@retry_on_timeout(settings.BOT_ACTION_RETRY_TIMES)
async def delete_simple_message(context: ContextTypes.DEFAULT_TYPE, **kwargs) -> None:
    try:
        await context.bot.delete_message(**kwargs)
    except TelegramError as exc:
        if exc.message == "Message to delete not found":
            logger.info(f"delete_simple_message: {exc.message}: kwargs={kwargs}")
        else:
            raise exc
