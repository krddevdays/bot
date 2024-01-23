#!/usr/bin/env python3
import logging
import os
import sys

from telegram import Update
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ContextTypes, MessageHandler, filters

from krddevbot.antispam import greet_chat_members
from krddevbot.tander import days_without_mention
from krddevbot.help import help_command


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



def main():
    """main function for export"""
    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    if not BOT_TOKEN: 
        raise Exception("Setup env variable BOT_TOKEN")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, days_without_mention))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
