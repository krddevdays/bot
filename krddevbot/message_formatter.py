from typing import Optional

from telegram import User
from telegram.helpers import escape_markdown


MAGIC_USER_STRING = "SOMEMAGICSTRING"


def md(template: str, user: Optional[dict | User] = None, **kwargs) -> str:
    if user:
        kwargs["username"] = MAGIC_USER_STRING

    result = escape_markdown(template.format(**kwargs), version=2)
    if user:
        if not isinstance(user, User):
            user = User(**user)
        result = result.replace(MAGIC_USER_STRING, user.mention_markdown_v2(user.username))
    return result
