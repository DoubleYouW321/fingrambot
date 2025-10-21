from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.gameskeyboard as gamekb

games_router = Router()

@games_router.message(Command('games'))
async def games(message: Message):
    photo_url = 'https://web.telegram.org/eede7508-f185-4c1a-be00-087bc5558c05'
    await message.answer_photo(photo=photo_url)
    await message.answer('Выберите игру', reply_markup=gamekb.games)

@games_router.callback_query(F.data == 'finans_fight')
async def fight(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Ваша цель - победить злоумышленника! Атакуйте или защищайтесь от его атак. Для этого используйте 10 "финансовых карт", каждая из которых является финансовым термином и имеет свой эффект. Не дайте злоумышленнику обмануть себя!',
                                     reply_markup=await gamekb.create_games(callback.data))

@games_router.callback_query(F.data == 'haos')
async def haos(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Увлекательная игра, которая быстро погрузит вас в мир инвестиций, доходов и высоких рисков!', reply_markup=await gamekb.create_games(callback.data))

@games_router.callback_query(F.data == 'comeback_to_games')
async def haos(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите игру', reply_markup=gamekb.games)