from typing import Any, Dict, List, Optional, Union

from telegram import Update
from telegram.ext._basehandler import BaseHandler, RT, UT
from telegram.ext._utils.types import CCT

MESSAGE_REACTION = "message_reaction"


class ReactionsHandler(BaseHandler[Update, CCT]):
    """Нужен исключительно пока не добавят поддержку эмодзи в python-telegram-bot."""

    async def handle_update(
        self,
        update: UT,
        application: "Application[Any, CCT, Any, Any, Any, Any]",
        check_result: object,
        context: CCT,
    ) -> RT:
        self.collect_additional_context(context, update, application, check_result)
        return await self.callback(update, check_result, context)

    def check_update(self, update: object) -> Optional[Union[bool, Dict[str, List[Any]]]]:
        """Checking message type and has it any new reaction"""
        if msg := update.api_kwargs.get('message_reaction'):
            new_reaction = msg.get('new_reaction')
            if new_reaction:
                return new_reaction
