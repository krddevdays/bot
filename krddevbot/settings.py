import os

APPS = os.environ.get('KRDDEVBOT_APPS', "").split(",")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
SENTRY_DSN = os.environ.get("SENTRY_DSN")
LOLS_BOT_ENABLED = bool(os.environ.get("LOLS_BOT_ENABLED", "True"))
EMOJI_TIMEOUT_SECONDS = int(os.environ.get("EMOJI_TIMEOUT_SECONDS", "60"))
GARBAGE_MESSAGE_TIMEOUT_SECONDS = int(os.environ.get("GARBAGE_MESSAGE_TIMEOUT_SECONDS", "30"))
AVITO_DICES = os.environ.get("AVITO_DICES", "4d20")
AVITO_THRESHOLD = int(os.environ.get("AVITO_THRESHOLD", "8"))
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
BANOFBOT_LIMIT = int(os.environ.get("BANOFBOT_LIMIT", "10"))
BANOFBOT_DRY_RUN = bool(os.environ.get("BANOFBOT_DRY_RUN", "True"))
