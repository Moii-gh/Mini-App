import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.types import InputMediaAnimation, InputMediaPhoto
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '6544091551:AAFiPC-KEmRB9zHF3d6R4cHMcDuBW87Vo74'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_pairs = {}


markup_request = ReplyKeyboardMarkup(resize_keyboard=True)
markup_request.add(
    KeyboardButton('Мальчик', request_contact=True)
).add(
    KeyboardButton('АААА Женщина')
).add(
    KeyboardButton('Неопознан(Фурри)', request_location=True)
)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Выбери свой пол", reply_markup=markup_request)


@dp.message_handler(commands=['connect'])
async def connect_users(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_pairs:
        await message.reply("Вы уже подключены. Отправь /disconnect, чтобы завершить текущий чат.")
        return

    available_users = [user for user in user_pairs if user_pairs[user] is None]

    if available_users:
        partner_id = available_users[0]
        user_pairs[user_id] = partner_id
        user_pairs[partner_id] = user_id

        await bot.send_message(partner_id, "Вы подключились! Поздоровайтесь. Отправь /disconnect чтоб отключиться.")
        await message.reply("Вы подключились! Поздоровайтесь. Отправь /disconnect чтоб отключиться.")
    else:
        user_pairs[user_id] = None
        await message.reply("Ищем собеседника. Подождите...")

@dp.message_handler(commands=['disconnect'])
async def disconnect_users(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_pairs or user_pairs[user_id] is None:
        await message.reply("Вы ни к кому не подключены.")
        return

    partner_id = user_pairs[user_id]

    if partner_id is not None:
        user_pairs[partner_id] = None
        await bot.send_message(partner_id, "Ваш собеседник отключился :(\nОтправь /connect чтобы найти собеседника.")

    del user_pairs[user_id]

    await message.reply("Вы отключились. Отправь /connect чтобы найти собеседника.")

    if partner_id is not None:
        del user_pairs[partner_id]

@dp.message_handler(content_types=['text', 'photo', 'animation', 'sticker'])
async def forward_message(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_pairs or user_pairs[user_id] is None:
        await message.reply("Вы ни к кому не подключены. Отправь /connect чтобы найти собеседника.")
        return

    partner_id = user_pairs[user_id]

    if message.animation:
        await bot.send_animation(partner_id, message.animation.file_id)
    elif message.photo:
        await bot.send_photo(partner_id,"иди нахуй со своим фото")
    elif message.sticker:
        await bot.send_sticker(partner_id, message.sticker.file_id)
    elif message.text:
        await bot.send_message(partner_id, message.text)
    else:
        await bot.send_message(partner_id, message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)