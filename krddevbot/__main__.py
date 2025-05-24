import importlib

from telegram import Update
from telegram.ext import Application

from krddevbot import settings
from krddevbot.application import KrdDevBotApplication, KrdDevBotBot
from krddevbot.logging import init_logging
from krddevbot.request import HTTPXRequestWithRetry


if __name__ == "__main__":
    init_logging()
    bot = KrdDevBotBot(
        settings.BOT_TOKEN,
        request=HTTPXRequestWithRetry(),
        get_updates_request=HTTPXRequestWithRetry()
    )
    application = Application.builder()\
        .application_class(KrdDevBotApplication)\
        .bot(bot)\
        .build()

    for app_name in settings.APPS:
        pkg = importlib.import_module('.'.join(('krddevbot', app_name)))
        pkg.init(application)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
