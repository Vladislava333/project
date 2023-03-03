from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


button_start = KeyboardButton('Регистрация')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_start)
# greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start)


menu_button1 = KeyboardButton('Мои питомцы')
menu_button2 = KeyboardButton('Напомнить')

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(menu_button1, menu_button2)


pet_button1 = KeyboardButton('Зарегистрировать собаку')
pet_button2 = KeyboardButton('Зарегистрировать кошку')
pet_button3 = KeyboardButton('Зарегистрировать вакцинацию')