import logging
from typing import Union

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes, filters, MessageHandler, Application, ExtBot

logger = logging.getLogger("telegram.ext.ExtBot")


class KrdDevBotBot(ExtBot):
    async def delete_message(self, chat_id: Union[str, int], message_id: int, **kwargs) -> bool:
        try:
            await super().delete_message(chat_id, message_id, **kwargs)
        except BadRequest:
            logger.info("Message to delete (%s, %s) not found", chat_id, message_id)


class KrdDevBotApplication(Application):
    messages = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_messages))

    async def handle_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        for message in self.messages:
            await message(update, context)
