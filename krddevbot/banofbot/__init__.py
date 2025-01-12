from asyncio import sleep

from redis import asyncio as aioredis
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

from krddevbot import settings
from krddevbot.application import KrdDevBotApplication
from krddevbot.messages import md


def get_redis_client():
    url = f'redis://default:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}'
    return aioredis.from_url(url)


ACTIONS = {
    'ban': 'Забанить',
    'forgive': 'Простить'
}


async def get_keyboard(message_id, user_id) -> InlineKeyboardMarkup:
    keyboard = []
    redis_client = get_redis_client()

    for action, value in ACTIONS.items():
        key = f'{action}_{message_id}_{user_id}'
        count = await redis_client.smembers(key)
        keyboard.append(InlineKeyboardButton(f"{value} ({len(count)})", callback_data=key))

    return InlineKeyboardMarkup([keyboard])


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message is None:
        await update.message.reply_text("Пожалуйста, ответьте на сообщение пользователя, которого хотите забанить.")
        return

    user_to_ban = update.message.reply_to_message.from_user
    username = md('{username}', user=update.message.reply_to_message.from_user)
    redis_client = get_redis_client()
    await redis_client.set(f'user_{user_to_ban.id}', username)
    await redis_client.set(f'original_{update.message.id}_{user_to_ban.id}', update.message.reply_to_message.id)
    keyboard = await get_keyboard(update.message.id, user_to_ban.id)
    await update.message.reply_text(f"Вы хотите забанить пользователя {username}?", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN_V2)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    action, message_id, user_id = query.data.split('_')

    redis_client = get_redis_client()
    await redis_client.sadd(query.data, md('{username}', user=update.effective_user))
    members = await redis_client.smembers(query.data)
    if len(members) >= settings.BANOFBOT_LIMIT:
        mems = ', '.join(m.decode() for m in members)
        username = await redis_client.get(f'user_{user_id}')
        if action == "ban":
            await query.message.reply_text(f"Пользователь {username.decode()} был забанен\nКаратели: {mems}", parse_mode=ParseMode.MARKDOWN_V2)
            original_id = await redis_client.get(f'original_{message_id}_{user_id}')
            await context.bot.delete_message(update.effective_message.chat_id, int(original_id.decode()))
            if not settings.BANOFBOT_DRY_RUN:
                await context.bot.ban_chat_member(update.effective_message.chat_id, user_id)
        elif action == "forgive":
            await query.message.reply_text(f"Пользователь {username.decode()} был прощён\nСпасители: {mems}", parse_mode=ParseMode.MARKDOWN_V2)
        await sleep(60)
        await context.bot.delete_message(update.effective_message.chat_id, update.effective_message.message_id)
        await context.bot.delete_message(update.effective_message.chat_id, message_id)
    else:
        key = next(k for k in ACTIONS.keys() if k != action)  # просто ищем противоположный ключ
        await redis_client.srem(f"{key}_{message_id}_{user_id}", update.effective_user.full_name)  # человек мог изменить своё мнение
        keyboard = await get_keyboard(message_id, user_id)
        try:
            await query.edit_message_reply_markup(keyboard)
        except BadRequest as exc:
            if 'Message is not modified' in exc.message:
                pass
            else:
                raise exc


def init(application: KrdDevBotApplication):
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CallbackQueryHandler(button))
