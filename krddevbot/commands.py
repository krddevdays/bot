from telegram import Update
from telegram.ext import ContextTypes


async def delete_messages(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes messages with a command and its response."""
    chat_id = context.job.data['chat_id']

    await context.bot.delete_message(chat_id=chat_id, message_id=context.job.data['command_message_id'])
    await context.bot.delete_message(chat_id=chat_id, message_id=context.job.data['answer_message_id'])


async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, *, message_template: str, parse_mode: str = "") -> None:
    """Unified command handler."""
    command_message = update.message
    message = await command_message.reply_text(message_template, parse_mode=parse_mode)

    context.job_queue.run_once(delete_messages, when=30, data={
        'chat_id': command_message.chat_id,
        'command_message_id': command_message.message_id,
        'answer_message_id': message.message_id,
    })
