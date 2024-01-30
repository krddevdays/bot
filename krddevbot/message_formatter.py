from typing import Optional

from telegram import User
from telegram.helpers import escape_markdown


def md(template: str, user: Optional[dict | User] = None, **kwargs) -> str:
    if user:
        if not isinstance(user, User):
            user = User(**user)        
        kwargs["username"] = user.mention_markdown_v2(user.name)

    # kwargs should be valid markdown syntax
    return escape_template(template).format(**kwargs)


def escape_template(template: str) -> str:
    # escape template text for markdown syntax
    escaped_template = escape_markdown(template, version=2)
    
    # recover template syntax
    result = escaped_template.replace('\\{', '{').replace('\\}', '}')

    return result
