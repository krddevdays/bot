from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypeVar, Union

from telegram import Update
from telegram._utils.defaultvalue import DEFAULT_TRUE
from telegram._utils.types import DVType
from telegram.ext._basehandler import BaseHandler
from telegram.ext._utils.types import CCT, HandlerCallback

RT = TypeVar("RT")

MESSAGE_REACTION = "message_reaction"

class ReactionsHandler(BaseHandler[Update, CCT]):
    def __init__(
        self,        
        callback: HandlerCallback[Update, CCT, RT],
        block: DVType[bool] = DEFAULT_TRUE,
    ):
        super().__init__(callback, block=block)

    def check_update(self, update: object) -> Optional[Union[bool, Dict[str, List[Any]]]]:
      """Checking message type and has it any new reaction"""
      msg = update.api_kwargs.get('message_reaction', None)
      if not msg:
        return None

      new_reaction = msg.get('new_reaction', [])
      reaction = next(iter(new_reaction), None)
      if not reaction:      
        return None

      return True        
