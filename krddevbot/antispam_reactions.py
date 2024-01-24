from telegram import Update

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from krddevbot.antispam import CHECKING_MEMBERS, BAN_ENABLED


async def antispam_reactions_checking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checking result of user reaction on greeting message"""
    msg = update.api_kwargs.get('message_reaction', None)
    if not msg:
      return

    chat_id = msg.get("chat", {}).get("id", 0)
    message_id = msg.get("message_id", 0)

    new_reaction = msg.get('new_reaction', [])
    reaction = next(iter(new_reaction), None)
    if not reaction:
      return    

    user = msg.get('user', {})
    user_id = user.get('id', 0)
    username = user.get('username', "")

    emoji = reaction.get('emoji', '')
    challenge = CHECKING_MEMBERS.get(user_id)
    if not challenge:
      return
    
    # Checking reaction only on greeting message
    if challenge['message_id'] != message_id:
      return

    # Remove greeting message
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    # Verify emoji on greeting message
    if emoji in challenge['emoji']:
      await context.bot.send_message(chat_id, f"Добро пожаловать, @{username}!")

      if user_id in CHECKING_MEMBERS:
        del CHECKING_MEMBERS[user_id]
    else:      
      await context.bot.send_message(chat_id, "Фатальная ошибка! Лови BANAN 🍌")

      if BAN_ENABLED:
        await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id, revoke_messages=True)


