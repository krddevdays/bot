#!/usr/bin/env python3

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    MessageReactionHandler,
    filters,
)
import os

from krddevbot import settings
from krddevbot.antispam import antispam_reactions_checking, greet_chat_members
from krddevbot.logging import init_logging
from krddevbot.message_formatter import md
from krddevbot.tander import days_without_mention

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /ping is issued."""
    env_vars = os.environ
    env_output = "\n".join(f"{name}: {value}" for name, value in env_vars.items())
    await update.message.reply_text(
        md(f"I'm alive, {update.effective_user.username}!!!\n\nEnvironment variables:\n{env_output}", user=update.effective_user),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


if __name__ == "__main__":
    init_logging()
    application = Application.builder().token(settings.BOT_TOKEN).build()

    application.add_handler(CommandHandler("ping", help_command))
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageReactionHandler(antispam_reactions_checking))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, days_without_mention))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
