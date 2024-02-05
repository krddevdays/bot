from telegram import Update, User

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from .constance import CHALLENGE_OK_MESSAGE_TEMPLATE, CHALLENGE_FAIL_MESSAGE
from .storage import CHECKING_MEMBERS
from ..message_formatter import md
from ..message_sender import send_garbage_message


async def antispam_reactions_checking(update: Update, new_reactions, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checking result of user reaction on greeting message"""

    msg = update.api_kwargs["message_reaction"]
    chat_id = msg.get("chat", {}).get("id", 0)
    message_id = msg.get("message_id", 0)

    user = User(**msg.get("user", {}))

    if challenge := CHECKING_MEMBERS.get(f"{user.id}_{chat_id}_{message_id}"):
        # Verify emoji on greeting message
        for reaction in new_reactions:
            emoji = reaction.get("emoji", "")
            if emoji in challenge:
                # Remove greeting message and welcome user
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                del CHECKING_MEMBERS[f"{user.id}_{chat_id}_{message_id}"]

                await send_garbage_message(
                    context,
                    chat_id,
                    md(CHALLENGE_OK_MESSAGE_TEMPLATE, user=user),
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
                break
        else:
            await send_garbage_message(
                context,
                chat_id,
                md(CHALLENGE_FAIL_MESSAGE),
                parse_mode=ParseMode.MARKDOWN_V2,
            )
