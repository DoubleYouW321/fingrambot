from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


learning_materials = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кредиты', callback_data='credits')],
    [InlineKeyboardButton(text='Кредитная история', callback_data='credit_story')],
    [InlineKeyboardButton(text='Ипотека', callback_data='ipoteka')],
    [InlineKeyboardButton(text='Планирование', callback_data='plans')],
    [InlineKeyboardButton(text='Фишинг', callback_data='fishing')],
    [InlineKeyboardButton(text='Мошенничество', callback_data='hackers')],
    [InlineKeyboardButton(text='Начать бизнес', callback_data='startup')],
    [InlineKeyboardButton(text='Налоги', callback_data='nalogs')],
    [InlineKeyboardButton(text='Инвестиции', callback_data='invest')],
    [InlineKeyboardButton(text='Вклады', callback_data='vklads')],
    [InlineKeyboardButton(text='Инфляция', callback_data='infl')],
])

urls = {
    'credits': 'https://fincult.info/articles/credits/',
    'credit_story': 'https://fincult.info/articles/credit-history/',
    'plans': 'https://fincult.info/articles/planning/',
    'fishing': 'https://fincult.info/articles/fishing/',
    'hackers': 'https://fincult.info/articles/fraud/',
    'startup': 'https://fincult.info/articles/start-business/',
    'nalogs': 'https://fincult.info/articles/tax/',
    'ipoteka': 'https://fincult.info/articles/ipoteka/',
    'invest': 'https://fincult.info/articles/investitsii/',
    'vklads': 'https://fincult.info/articles/holdings/',
    'infl': 'https://fincult.info/articles/inflation/'

}

async def create_urls_builder(callback):
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.add(InlineKeyboardButton(text='Ссылка', url=urls[callback]))
    inline_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='comeback_to_materials'))
    return inline_keyboard.adjust(1).as_markup()