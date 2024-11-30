from telegram import Update
from telegram.ext import ChatMemberHandler, MessageReactionHandler, ContextTypes

from .antispam import greet_chat_members, track_user_messages
from .antispam_reactions import antispam_reactions_checking
from .storage import CHECKING_MEMBERS
from krddevbot.application import KrdDevBotApplication


def init(application: KrdDevBotApplication):
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageReactionHandler(antispam_reactions_checking))
    application.messages.append(track_user_messages)
