from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

calculators_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сложных %', callback_data='hard_procents_calc')],
    [InlineKeyboardButton(text='Ипотечный', callback_data='ipotek_calc')],
    [InlineKeyboardButton(text='Инфляции', callback_data='infl_calc')],
    [InlineKeyboardButton(text='Кредитный', callback_data='credit_calc')]
])

hard_proc = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Как пользоваться', callback_data='hard_proc_info')],
    [InlineKeyboardButton(text='Запустить калькулятор', callback_data='hard_proc_start')],
])
back_to_hard_proc = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='hard_procents_calc')],
    [InlineKeyboardButton(text='Запустить калькулятор', callback_data='hard_proc_start')],
])

ipotek = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Как пользоваться', callback_data='ipotek_info')],
    [InlineKeyboardButton(text='Запустить калькулятор', callback_data='ipotek_start')],
])

back_to_ipotek = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='ipotek_calc')],
    [InlineKeyboardButton(text='Запустить калькулятор', callback_data='ipotek_start')],
])

infl = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Как пользоваться', callback_data='infl_info')],
    [InlineKeyboardButton(text='Запустить калькулятор', callback_data='infl_start')],
])

back_to_infl = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='infl_calc')],
    [InlineKeyboardButton(text='Запустить калькулятор', callback_data='infl_start')],
])

credit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Как пользоваться', callback_data='credit_info')],
    [InlineKeyboardButton(text='Запустить калькулятор', callback_data='credit_start')],
])

back_to_credit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='credit_calc')],
    [InlineKeyboardButton(text='Запустить калькулятор', callback_data='credit_start')],
])