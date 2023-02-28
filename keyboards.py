from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


button_start = KeyboardButton('Регистрация')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_start)
# greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start)



inline_btn_1 = InlineKeyboardButton('Зарегистрироваться', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)