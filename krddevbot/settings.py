import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_READ_WRITE_TIMEOUT_SECONDS = int(os.environ.get("BOT_READ_WRITE_TIMEOUT_SECONDS", "30"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
SENTRY_DSN = os.environ.get("SENTRY_DSN")
LOLS_BOT_ENABLED = bool(os.environ.get("LOLS_BOT_ENABLED", "True"))
EMOJI_TIMEOUT_SECONDS = int(os.environ.get("EMOJI_TIMEOUT_SECONDS", "60"))
GARBAGE_MESSAGE_TIMEOUT_SECONDS = int(os.environ.get("GARBAGE_MESSAGE_TIMEOUT_SECONDS", "30"))
