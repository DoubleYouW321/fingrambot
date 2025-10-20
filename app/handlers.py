from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
import app.database.requests as rq

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.username)  
    await message.answer('Приветствуем вас в чат боте по фин грамотности')

@router.message(Command('learnmaterials'))
async def learning(message: Message):
    await message.answer('В этом разделе вы можете найти важные обучающме статьи по фин-гармотности', reply_markup=kb.learning_materials)


@router.callback_query(F.data == 'credits')
async def credits(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Кредиты"')
    await callback.message.edit_text('Выберите статью:', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'credit_story')
async def story(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Кредиты"')
    await callback.message.edit_text('Выберите статью:', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'ipoteka')
async def ipoteka(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Ипотека"')
    await callback.message.edit_text('Выберите статью:', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'plans')
async def plans(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Планирование"')
    await callback.message.edit_text('Ссылка на статьи по теме Планирование', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'fishing')
async def fishing(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Фишинг"')
    await callback.message.edit_text('Ссылка на статьи по теме Фишинг', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'hackers')
async def hackers(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Мошенничество"')
    await callback.message.edit_text('Ссылка на статьи по теме Мошенничество', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'startup')
async def startup(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Начать бизнес"')
    await callback.message.edit_text('Ссылка на статьи по теме Начать бизнес', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'nalogs')
async def nalogs(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Налоги"')
    await callback.message.edit_text('Ссылка на статьи по теме Налоги', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'invest')
async def invest(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Инвестиции"')
    await callback.message.edit_text('Ссылка на статьи по теме Инвестиции', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'vklads')
async def vklads(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Вклады"')
    await callback.message.edit_text('Ссылка на статьи по теме Вклады', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'infl')
async def infl(callback: CallbackQuery):
    await callback.answer('Вы открыли раздел "Инфляция"')
    await callback.message.edit_text('Ссылка на статьи по теме Инфляция', reply_markup=await kb.create_urls_builder(callback.data))

@router.callback_query(F.data == 'comeback_to_materials')
async def comeback_mat(callback: CallbackQuery):
    await callback.answer('Назад"')
    await callback.message.edit_text('В этом разделе вы можете найти важные обучающме статьи по фин-гармотности', reply_markup=kb.learning_materials)