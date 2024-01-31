import pytest

from krddevbot.message_formatter import md

TEMPLATE = "Hello, {username} !"


@pytest.mark.parametrize("has_username", [True, False])
def test_md(has_username):
    user = {"id": 123123, "first_name": r"Jo\_hn", "last_name": "Doe", "username": None, "is_bot": False}
    if has_username:
        user["username"] = "jdoe"

    result = md(TEMPLATE, user)
    print(result)

    first_name = user['first_name'].replace(r'\_', r'\\\_')
    expect_username = user["username"] if has_username else f"{first_name} {user['last_name']}"
    assert result == f"Hello, [{expect_username}](tg://user?id=123123) \\!"
