#!/usr/bin/env python3
import logging
import os

from telegram import Update
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ContextTypes, MessageHandler, filters

from krddevbot.antispam import greet_chat_members
from krddevbot.tander import days_without_mention


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def main():
    """main function for export"""
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if BOT_TOKEN: 
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, days_without_mention))

        application.run_polling(allowed_updates=Update.ALL_TYPES)
    else:
        logger.error("Environment variable BOT_TOKEN not exists!")

if __name__ == "__main__":
    main()
