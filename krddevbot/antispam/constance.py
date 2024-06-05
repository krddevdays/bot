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

👋 Добро пожаловать в чат сообщества krd.dev!

🥦 Подтвердите что вы кожаный мешок, поставив реакцию к этому сообщению с эмодзи {challenge_text} из стандартного набора.

⏱ У вас {timeout} секунд...
"""

TIMEOUT_FAIL_MESSAGE_TEMPLATE = "📦 Status: 408 Request Timeout - Лови BANAN 🍌, {username}!"

CHALLENGE_FAIL_MESSAGE = "😡 Этот не подходит, попробуй другой."

CHALLENGE_OK_MESSAGE_TEMPLATE = """👋 testДобро пожаловать в чат сообщества krd.dev, {username}!

💬 Помимо этого чата у нас есть другие, по интересам:
- @krdfrontend для frontend разработчиков;
- @krdbackend для backend разработчиков;
- @pythonkrd для Python разработчиков;
- @krdQA для QA инженеров;
- @golangkrasnodar для Go разработчиков;
- @rubykrd для Ruby разработчиков;
- @androidkrd для Android разработчиков;
- @KrdDotNetCommunity для тех, кто пишет на DotNet;
- @phpkrd для PHP разработчиков;
- @krdmobile для мобильных разработчиков;
- @removedev для тех, кто работает удаленно.

📰 Так же у нас есть канал с новостями сообщества @krddevdays.

📕 Правила:
1) все что касается вакансий, поиска работы и карьеры обсуждается в чате @krddevcareer;
2) опубликовать вакансию можно в @krddevvacancies (читайте описание канала);
3) любые публикации о мероприятиях, конкурсах и прочем согласовываются с администраторами чата;
4) мы относимся друг к другу уважительно, не оскорбляем и не переходим на личности.

Нарушение этих правил карается бананом 🍌
"""
