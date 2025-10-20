from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.gameskeyboard as gamekb

games_router = Router()

@games_router.message(Command('desktopgames'))
async def games(message: Message):
    await message.answer('Выберите игру', reply_markup=gamekb.games)

@games_router.callback_query(F.data == 'finans_fight')
async def fight(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Ваша цель - победить злоумышленника! Атакуйте или защищайтесь от его атак. Для этого используйте 10 "финансовых карт", каждая из которых является финансовым термином и имеет свой эффект. Не дайте злоумышленнику обмануть себя!',
                                     reply_markup=await gamekb.create_games(callback.data))

@games_router.callback_query(F.data == 'haos')
async def haos(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите', reply_markup=await gamekb.create_games(callback.data))