from typing import Optional

from telegram import User
from telegram.helpers import escape_markdown


def md(template: str, user: Optional[dict | User] = None, **kwargs) -> str:
    if user:
        if not isinstance(user, User):
            user = User(**user)
        kwargs["username"] = user.mention_markdown_v2(user.username)

    return escape_markdown(template.format(**kwargs), version=2)
