from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler

from krddevbot.commands import command_handler
from krddevbot.messages import md
from .constance import HELP_MESSAGE_TEMPLATE, LIST_MESSAGE_TEMPLATE, RULES_MESSAGE_TEMPLATE
from krddevbot.application import KrdDevBotApplication


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await command_handler(update=update,
                          context=context,
                          message_template=md("I'm alive, {username}!", user=update.effective_user),
                          parse_mode=ParseMode.MARKDOWN_V2)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await command_handler(update=update, context=context, message_template=HELP_MESSAGE_TEMPLATE)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await command_handler(update=update, context=context, message_template=LIST_MESSAGE_TEMPLATE)


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await command_handler(update=update, context=context, message_template=RULES_MESSAGE_TEMPLATE)


def init(application: KrdDevBotApplication):
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("rules", rules_command))
