from config import TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types
from keyboards import *

# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

users = dict()

# Хэндлер на команду /test1
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    if message.from_user.id in users:
        await message.reply("Приветствую!") #TODO сделать клавиатуру
    else:
        user_id = message.from_user.id
        users[user_id] = None
        await message.reply("Приветствую! Нажмите кнопку, чтобы зарегистрироваться", reply_markup=greet_kb)


@dp.message_handler(text='Регистрация')
async def cmd_register(message: types.Message):
    await message.reply("Напишите Ваше имя")


@dp.message_handler()
async def echo_message(message: types.Message):
    global users
    mess = message.text
    user_id = message.from_user.id

    if user_id in users.keys() and users[user_id] == None:
        users[user_id] = mess
        await message.reply(f"Здравствуйте, {mess}")
    else:
        await message.reply(f"Здравствуйте, {users[user_id]}")

# @dp.callback_query_handler(
#     lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка')


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)


