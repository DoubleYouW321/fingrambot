from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

games = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Финансовый поединок', callback_data='finans_fight')],
    [InlineKeyboardButton(text='Бизнес-хаос', callback_data='haos')]
])

urls_games = {
    'finans_fight': 'https://DoubleYouW321.github.io/cards.html',
    'haos': 'https://DoubleYouW321.github.io/haos.html'
}

async def create_games(callback):
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.add(InlineKeyboardButton(text='Ссылка на игру', url=urls_games[callback]))
    inline_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='comeback_to_games'))
    return inline_keyboard.adjust(1).as_markup()