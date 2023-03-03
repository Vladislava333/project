from config import TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types
from keyboards import *
from bd_scripts import *

# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

users = dict()

#TODO связать с БД
# Хэндлер на команду /test1
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    user_data = db_check_user(message.from_user.id)

    if user_data:
        await message.reply(f"Приветствую, {user_data[1]}", reply_markup=menu_kb) #TODO сделать клавиатуру
    else:
        await message.reply("Приветствую! Нажмите кнопку, чтобы зарегистрироваться", reply_markup=greet_kb)


@dp.message_handler(text='Регистрация')
async def cmd_register(message: types.Message):
    await message.reply("Напишите Ваше имя")


@dp.message_handler(text='Мои питомцы')
async def cmd_register(message: types.Message):
    await message.reply("Мои питомцы")

@dp.message_handler()
async def echo_message(message: types.Message):
    mess = message.text
    user_id = message.from_user.id
    user_data = db_check_user(message.from_user.id)
    if not(user_data):
        username = mess
        db_add_user(username, user_id)
        await message.reply(f"Здравствуйте, {mess}", reply_markup=menu_kb) #TODO сделать клавиатуру действий после регистрации

    else:
        await message.reply(f"Здравствуйте, {user_data[0]}", reply_markup=menu_kb)




if __name__ == "__main__":
    # Запуск бота
    db_connect()
    executor.start_polling(dp, skip_updates=True)


