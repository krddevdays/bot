from typing import Optional

from telegram import User


def md(template: str, user: Optional[dict | User] = None, **kwargs) -> str:
    if user:
        if not isinstance(user, User):
            user = User(**user)
        username = user.username
        if not username:
            username = user.mention_markdown_v2(user.first_name)
        kwargs["username"] = f"@{username}"

    return template.format(**kwargs)\
        .replace('_', '\\_')\
        .replace('*', '\\*')\
        .replace('[', '\\]')\
        .replace('.', '\\.')\
        .replace('!', '\\!')
