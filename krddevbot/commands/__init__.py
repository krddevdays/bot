# commands/__init__.py

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from ..antispam.constance import (
    HELP_MESSAGE_TEMPLATE,
    LIST_MESSAGE_TEMPLATE,
    RULES_MESSAGE_TEMPLATE
)
from ..message_formatter import md


async def delete_messages(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes messages with a command and its response."""
    chat_id = context.job.data['chat_id']
    
    await context.bot.delete_message(chat_id=chat_id, message_id=context.job.data['command_message_id'])
    await context.bot.delete_message(chat_id=chat_id, message_id=context.job.data['help_message_id'])


async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, *, message_template: str, parse_mode: str = "") -> None:
    """Unified command handler."""
    command_message = update.message
    message = await command_message.reply_text(message_template, parse_mode=parse_mode)
    
    context.job_queue.run_once(delete_messages, when=30, data={
        'chat_id': command_message.chat_id,
        'command_message_id': command_message.message_id,
        'help_message_id': message.message_id
    })


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await command_handler(update=update, context=context, message_template=md("I'm alive, {username}!", user=update.effective_user), parse_mode=ParseMode.MARKDOWN_V2)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await command_handler(update=update, context=context, message_template=HELP_MESSAGE_TEMPLATE)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await command_handler(update=update, context=context, message_template=LIST_MESSAGE_TEMPLATE)


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await command_handler(update=update, context=context, message_template=RULES_MESSAGE_TEMPLATE)
