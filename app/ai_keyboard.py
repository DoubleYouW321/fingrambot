from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

consult_choose = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Информация о консультанте', callback_data='consult_info')],
    [InlineKeyboardButton(text='Задать вопрос', callback_data='start_consult')],
])

back_to_consult = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Задать вопрос', callback_data='start_consult')],
])