import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
SENTRY_DSN = os.environ.get("SENTRY_DSN")
DARKBYTE_ENABLED = bool(os.environ.get("DARKBYTE_ENABLED", "True"))
EMOJI_TIMEOUT_SECONDS = int(os.environ.get("EMOJI_TIMEOUT_SECONDS", "60"))
GARBAGE_COLLECTOR_RUN_TASK_SECONDS = int(os.environ.get("GARBAGE_COLLECTOR_RUN_TASK_SECONDS", "30"))
