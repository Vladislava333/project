from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton




button_start = KeyboardButton('Регистрация')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_start)
# greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start)


menu_button1 = KeyboardButton('Мои питомцы')
menu_button2 = KeyboardButton('Напомнить')

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(menu_button1, menu_button2)


pet_button1 = KeyboardButton('Добавить питомца')
back_button = KeyboardButton('Назад')

pet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(pet_button1, back_button)

reg_button1 = KeyboardButton('Собаку')
reg_button2 = KeyboardButton('Кошку')

reg_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(reg_button1, reg_button2)

reg_button3 = KeyboardButton('Новая вакцинация')

remind_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(reg_button3, back_button)

