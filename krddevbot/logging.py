import logging

import sentry_sdk

from krddevbot import settings


def init_logging():
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=settings.LOG_LEVEL)

    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.INFO)
    logging.getLogger("telegram.ext.ExtBot").setLevel(logging.INFO)

    sentry_sdk.init(dsn=settings.SENTRY_DSN)
