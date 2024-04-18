# Secret store
EMOJI = {
    "рукой": "👍👎👏🙏👌🖕🤝✍️💅",
    "огнем": "🔥",
    "сердцем": "❤️💘💔❤️‍🔥",
    "лицом": "🥰😁🤔🤯😱🤬😢🤩🤮🤡🥱🥴😍🌚🤣🤨😐😈😴😭🤓😇😨🤗🎅🤪😘😎😡",
    "животным": "🕊🐳🙈🙉🦄🙊👾☃️",
    "едой": "🍓🌭🍌🍾💊🎃",
}

GREETING_MESSAGE_TEMPLATE = """
Уважаемый {username}
Добро пожаловать в чаты сообщества krd.dev!

Подтвердите что вы кожаный мешок, поставив реакцию к этому сообщению с эмодзи {challenge_text} из стандартного набора.

У вас {timeout} секунд...
"""

TIMEOUT_FAIL_MESSAGE_TEMPLATE = "Status: 408 Request Timeout - Лови BANAN 🍌, {username}!"

CHALLENGE_FAIL_MESSAGE = "Этот не подходит, попробуй другой."

CHALLENGE_OK_MESSAGE_TEMPLATE = "Добро пожаловать, {username}!"
