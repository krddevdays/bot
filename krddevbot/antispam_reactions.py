from telegram import Update

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from krddevbot.antispam import CHECKING_MEMBERS, CHALLENGE_OK_MESSAGE_TEMPLATE, CHALLENGE_FAIL_MESSAGE
from krddevbot.service import get_md_user_name


async def antispam_reactions_checking(update: Update, new_reaction, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checking result of user reaction on greeting message"""

    msg = update.api_kwargs['message_reaction']
    chat_id = msg.get("chat", {}).get("id", 0)
    message_id = msg.get("message_id", 0)

    user = msg.get('user', {})
    user_id = user.get('id', 0)
    username = get_md_user_name(user)

    emoji = new_reaction.get('emoji', '')
    if challenge := CHECKING_MEMBERS.get(f'{user_id}_{chat_id}_{message_id}'):
        # Verify emoji on greeting message
        if emoji in challenge:
            # Remove greeting message and welcome user
            await context.bot.send_message(
                chat_id,
                CHALLENGE_OK_MESSAGE_TEMPLATE.format(username=username),
                parse_mode=ParseMode.MARKDOWN_V2
            )
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            del CHECKING_MEMBERS[f'{user_id}_{chat_id}_{message_id}']
        else:
            await context.bot.send_message(chat_id, CHALLENGE_FAIL_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)
