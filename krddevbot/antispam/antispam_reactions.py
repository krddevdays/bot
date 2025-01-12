from telegram import Update

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from .constance import CHALLENGE_OK_MESSAGE_TEMPLATE, CHALLENGE_FAIL_MESSAGE
from krddevbot.storage import CHECKING_MEMBERS
from ..messages import md, send_garbage_message


async def antispam_reactions_checking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checking result of user reaction on greeting message"""

    chat_id = update.message_reaction.chat.id
    message_id = update.message_reaction.message_id
    user = update.message_reaction.user
    new_reactions = update.message_reaction.new_reaction

    if challenge := CHECKING_MEMBERS.get(f"{user.id}_{chat_id}_{message_id}"):
        for reaction in new_reactions:
            if reaction.emoji in challenge:
                context.user_data['joined'] = False

                await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                del CHECKING_MEMBERS[f"{user.id}_{chat_id}_{message_id}"]

                await send_garbage_message(
                    context,
                    chat_id=chat_id,
                    text=md(CHALLENGE_OK_MESSAGE_TEMPLATE, user=user),
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
                break
            else:
                await send_garbage_message(
                    context,
                    chat_id=chat_id,
                    text=md(CHALLENGE_FAIL_MESSAGE),
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
