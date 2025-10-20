from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import app.finans_calculator_keyboard as calc_kb

storage = MemoryStorage()
infl_router = Router()

class InflStates(StatesGroup):
    waiting_principal = State()
    waiting_rate = State()
    waiting_years = State()

class SimpleInflCalculator:
    @staticmethod
    def calculate(principal: float, rate: float, years: int) -> dict:

        future_sum = principal * (1 + rate/100)**years
        miss_sum = future_sum - principal
        proc_miss = (miss_sum / principal) * 100
        return {
            'principal': principal,
            'rate': rate,
            'years': years,
            'future_sum': future_sum,
            'miss_sum': miss_sum,
            'proc_miss': proc_miss
        }
    
@infl_router.callback_query(F.data == 'infl_calc')
async def infl(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выбирите действие', reply_markup=calc_kb.infl)

@infl_router.callback_query(F.data == 'infl_info')
async def infl_info(callback: CallbackQuery):
    await callback.answer('')
    info_text = ("📉 Калькулятор инфляции\n\n"
        "📊 Что рассчитывает калькулятор:\n"
        "• Будущую стоимость денег\n"
        "• Потерю покупательной способности\n"
        "• Реальную доходность сбережений\n"
        "• Сравнение с инвестициями\n\n"
        "🔄 Как пользоваться:\n"
        "1. Введите сумму денег (например: 100000)\n"
        "2. Введите годовую инфляцию (например: 7)\n"
        "3. Введите период в годах (например: 5)\n\n"
        "📈 Пример расчета:\n"
        "Сумма: 100,000 ₽\n"
        "Инфляция: 7%\n"
        "Период: 5 лет\n"
        "Результат:\n"
        "• Будущая стоимость: ~140,255 ₽\n"
        "• Потеря стоимости: ~40,255 ₽\n"
        "• Обесценивание: 40%\n\n"
        "💡 Инфляция показывает, насколько дороже станет жизнь в будущем")
    await callback.message.edit_text(info_text, reply_markup=calc_kb.back_to_infl)

@infl_router.callback_query(F.data == 'infl_start')
async def infl_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_state(InflStates.waiting_principal)
    
    await state.update_data(user_id=callback.from_user.id)
    
    await callback.message.edit_text(
        "💵 Введите сумму ипотеки:\n\n"
        "Например: 1000000"
    )

@infl_router.message(InflStates.waiting_principal)
async def process_principal(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.infl)
            await state.clear()
            return
            
        principal = float(message.text.replace(',', '.'))
        if principal <= 0:
            await message.answer("❌ Сумма должна быть положительной. Введите сумму:")
            return
        
        await state.update_data(principal=principal)
        await state.set_state(InflStates.waiting_rate)
        await message.answer(
            f"💵 Сумма: {principal:,.0f} ₽\n\n"
            "📈 Введите % инфляции:\n\n"
            "Например: 8"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число. Введите сумму:")

@infl_router.message(InflStates.waiting_rate)
async def process_rate(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data or 'principal' not in data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.infl)
            await state.clear()
            return
            
        rate = float(message.text.replace(',', '.'))
        if rate <= 0:
            await message.answer("❌ Ставка должна быть положительной. Введите % инфляции:")
            return
        
        await state.update_data(rate=rate)
        await state.set_state(InflStates.waiting_years)
        
        principal = data['principal']
        
        await message.answer(
            f"💵 Сумма: {principal:,.0f} ₽\n"
            f"📈 % Инфляции: {rate}%\n\n"
            "⏱ Введите срок в годах:\n\n"
            "Например: 10"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число. Введите % инфляции:")

@infl_router.message(InflStates.waiting_years)
async def process_years(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data or 'principal' not in data or 'rate' not in data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.infl)
            await state.clear()
            return
            
        years = int(message.text)
        if years <= 0:
            await message.answer("❌ Срок должен быть положительным. Введите срок:")
            return
        
        principal = data['principal']
        rate = data['rate']
        
        result = SimpleInflCalculator.calculate(principal, rate, years)
        
        response = (
            f"📊 Результат расчета:\n\n"
            f"💵 Начальная сумма: {result['principal']:,.0f} ₽\n"
            f"📈 %: {result['rate']}%\n"
            f"⏱ Срок: {result['years']} лет\n\n"
            f"💰 Будущая стоимость: {result['future_sum']:,.0f} ₽\n"
            f"💸 Потеря стоимости: {result['miss_sum']:,.0f} ₽\n"
            f"Обесценивание {result['proc_miss']:,.0f} %"
        )
        
        await message.answer(response)
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите целое число. Введите срок:")


