from telegram import Update
from telegram.ext import ContextTypes, filters, MessageHandler, Application


class KrdDevBotApplication(Application):
    messages = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_messages))

    async def handle_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        for message in self.messages:
            await message(update, context)
