import logging
from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger = logging.getLogger(__name__)
    logging.info("Help command found")

    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")
