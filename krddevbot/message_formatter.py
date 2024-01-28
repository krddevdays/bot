from telegram import User


def md(template: str, **kwargs) -> str:
    if not isinstance(user, User):
        user = User(
            id=user.get('id'),
            first_name=user.get('first_name'),
            is_bot=user.get('is_bot'),
            username=user.get('username')
        )

    username = user.username
    if username:
        username = username.replace('_', '\\_')
        return f"@{username}"
    else:
        return user.mention_markdown_v2(user.first_name)
