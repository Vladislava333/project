from config import TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from bd_scripts import *
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


class RegisterPet(StatesGroup):
    name = State()
    birthday = State()
    animal_type = State()
    #breed = State()


class Reminder(StatesGroup):
    v_type = State()
    date_ = State()
    pet_id = State()

storage = MemoryStorage()
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot, storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)



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


@dp.message_handler(text='Назад')
async def cmd_back(message: types.Message):
    await message.reply("Выберите действие", reply_markup=menu_kb)


@dp.message_handler(text='Мои питомцы')
async def cmd_pets(message: types.Message):
    pets_list = get_pets(message.from_user.id)
    if pets_list:
        await message.reply(pets_list, reply_markup=pet_kb1)
    else:
        await message.reply("Нет питомцев", reply_markup=pet_kb1)


@dp.message_handler(text='Добавить питомца')
async def cmd_add_pet(message: types.Message):
    await RegisterPet.animal_type.set()
    await message.reply("Кого вы хотите зарегистрировать?", reply_markup=reg_kb)


@dp.message_handler(state=RegisterPet.animal_type)
async def cmd_pet_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        animal_types = ['Кошку', 'Собаку']
        data['animal_type'] = animal_types.index(message.text)
        await RegisterPet.name.set()
        await message.reply("Введите имя", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=RegisterPet.name)
async def cmd_birthday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await RegisterPet.birthday.set()
        await message.reply("Введите дату рождения", reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=RegisterPet.birthday)
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['birthday'] = date.strftime("%d.%m.%Y")
            savePet(data['name'], data['animal_type'], data['birthday'], user=callback_query.from_user.id)
            await state.finish()
            await callback_query.message.reply(f"Питомец {data['name']} сохранен", reply_markup=menu_kb)

@dp.message_handler(text='Напомнить')
async def cmd_remind(message: types.Message):
    #vacs_list = get_vacs(message.from_user.id)
    vacs_list = 'Вакцинации'
    if vacs_list:
        await message.reply(vacs_list, reply_markup=remind_kb)
    else:
        await message.reply("Нет записей", reply_markup=remind_kb)


@dp.message_handler(text='Новая вакцинация')
async def cmd_add_pet(message: types.Message):
    await Reminder.pet_id.set()
    pets = get_pets_id(message.from_user.id)
    animal_types = ['Кошка', 'Собака']
    kb_buttons = [InlineKeyboardButton(f'{animal_types[x[2]]} {x[1]}', callback_data="vacs_pet_"+str(x[0])) for x in pets]
    await message.reply("Кого Вы хотите зарегистрировать?", reply_markup=InlineKeyboardMarkup().add(*kb_buttons))

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
        await message.reply(f"Здравствуйте, {user_data[1]}", reply_markup=menu_kb)




if __name__ == "__main__":
    # Запуск бота
    db_connect()
    executor.start_polling(dp, skip_updates=True)
