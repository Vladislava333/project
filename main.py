from config import TOKEN


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from bd_scripts import *
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

import logging
import aioschedule, asyncio


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


async def schedule_message():
    vacs_list = get_all_vacs()
    print(vacs_list)
    v_types = get_vac_types()
    for v in vacs_list:
         animal_types = ['Кошка', 'Собака']
         try:
            '''await bot.send_message(v[0], f'{animal_types[v[3]]} {v[2]} - вакцина {v_types[v[5]]} - до {v[4]} ', reply_markup=remind_kb)'''
            await bot.send_message(v[0], f'{animal_types[v[3]]} {v[2]} - вакцина {v_types[v[5]]} - до {v[4]}', reply_markup=remind_kb)
         except:
             pass


async def scheduler():
    #aioschedule.every().day.at("12:00").do(mess)
    aioschedule.every(1).minutes.do(schedule_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


async def on_shutdown(_):
    await storage.close()
    await storage.wait_closed()


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
    vacs_list = get_vacs(message.from_user.id)
    if vacs_list:
        await message.reply(vacs_list, reply_markup=remind_kb)
    else:
        await message.reply("Нет записей", reply_markup=remind_kb)


@dp.message_handler(text='Новая вакцинация')
async def cmd_add_pet_vacs(message: types.Message):
    await Reminder.pet_id.set()
    pets = get_pets_id(message.from_user.id)
    animal_types = ['Кошка', 'Собака']
    kb_buttons = [InlineKeyboardButton(f'{animal_types[x[2]]} {x[1]}', callback_data="vacs_pet_"+str(x[0])) for x in pets]
    await message.reply("Кого Вы хотите зарегистрировать?", reply_markup=InlineKeyboardMarkup().add(*kb_buttons))


@dp.callback_query_handler(state=Reminder.pet_id)
async def cmd_app_date_vtype(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['pet_id'] = call.data.split('_')[-1]
        await Reminder.v_type.set()
        vacs = get_vac_types()
        print(vacs)
        v_buttons = [InlineKeyboardButton(x[1], callback_data="vacs_type_" + str(x[0])) for x in vacs]
        await bot.send_message(call.from_user.id, "Выберите тип вакцины", reply_markup=InlineKeyboardMarkup().add(*v_buttons))

@dp.callback_query_handler(state=Reminder.v_type)
async def cmd_app_date_vtype(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['v_type'] = int(call.data.split('_')[-1])
        print(call.data)
        await Reminder.date_.set()
        await bot.send_message(call.from_user.id, "Введите дату вакцинации", reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=Reminder.date_)
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['date_'] = date.strftime("%d.%m.%Y")
            saveVasc(data['pet_id'], data['v_type'], data['date_'], user=callback_query.from_user.id)
            await state.finish()
            await callback_query.message.reply(f"Вакцинация {data['date_']} сохранена", reply_markup=menu_kb)


@dp.message_handler()
async def echo_message(message: types.Message):
    mess = message.text
    user_id = message.from_user.id
    user_data = db_check_user(message.from_user.id)

    if not(user_data):
        username = mess
        db_add_user(username, user_id)
        await message.reply(f"Здравствуйте, {mess}", reply_markup=menu_kb)

    else:
        await message.reply(f"Здравствуйте, {user_data[1]}", reply_markup=menu_kb)


if __name__ == "__main__":
    # Запуск бота
    db_connect()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
