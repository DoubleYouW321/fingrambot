from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

import app.database.requests as rq

from config import ADMIN_CHAT_ID


feedback_router = Router()

ADMIN = ADMIN_CHAT_ID

feedback_markups = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отменить', callback_data='stop')]
])

class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()


@feedback_router.message(Command("feedback"))
async def cmd_feedback_start(message: Message, state: FSMContext):
    await message.answer("📝 Раздел для отзывов. Напишите свой отзыв:", reply_markup=feedback_markups)
    await state.set_state(FeedbackStates.waiting_for_feedback)

@feedback_router.message(FeedbackStates.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext, bot: Bot):
    user_feedback = message.text
    user_id = message.from_user.id
    username = message.from_user.username or "Без username"
    first_name = message.from_user.first_name or "Не указано"
    
    admin_message = (
        "📨 Новый отзыв!\n"
        f"👤 Пользователь: {first_name} (@{username})\n"
        f"🆔 ID: {user_id}\n"
        f"💬 Отзыв: {user_feedback}"
    )

    try:
        await bot.send_message(ADMIN, admin_message)
        
        await message.answer("✅ Спасибо! Ваш отзыв отправлен администратору.")
        
    except Exception as e:
        await message.answer("❌ Произошла ошибка при отправке отзыва.")
    
    await rq.set_comment(message.from_user.id, message.text)
    await state.clear()

@feedback_router.callback_query(F.data == 'stop')
async def process_feedback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


 
