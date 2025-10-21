from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import app.finans_calculator_keyboard as calc_kb

storage = MemoryStorage()
calculator_router = Router()

class HardProcentsStates(StatesGroup):
    waiting_principal = State()
    waiting_rate = State()
    waiting_years = State()

class SimpleCompoundCalculator:
    @staticmethod
    def calculate(principal: float, rate: float, years: int) -> dict:

        r = rate / 100
        
        final_amount = principal * (1 + r) ** years
        profit = final_amount - principal
        
        return {
            'principal': principal,
            'rate': rate,
            'years': years,
            'final_amount': final_amount,
            'profit': profit
        }

@calculator_router.message(Command('calculator'))
async def calculator(message: Message):
    with open('images\calculator.jpg', 'rb') as photo:
        await message.answer(photo, caption="Выбирите нужный калькулятор", reply_markup=calc_kb.calculators_keyboard)

@calculator_router.callback_query(F.data == 'hard_procents_calc')
async def hard_proc(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выбирите действие', reply_markup=calc_kb.hard_proc)

@calculator_router.callback_query(F.data == 'hard_proc_info')
async def hard_proc_info(callback: CallbackQuery):
     help_text = (
        "📚 Простой калькулятор сложных процентов\n\n"
        "Всего 3 шага:\n"
        "1. Введите сумму инвестиций\n"
        "2. Введите годовую процентную ставку\n"
        "3. Введите срок в годах\n\n"
        "Пример:\n"
        "Сумма: 100000\n"
        "Ставка: 10\n"
        "Срок: 5\n\n"
        "Результат:\n"
        "Через 5 лет: 161051 ₽\n"
        "Прибыль: 61051 ₽"
    )
     await callback.message.edit_text(help_text, reply_markup=calc_kb.back_to_hard_proc)

@calculator_router.callback_query(F.data == 'hard_proc_start')
async def hard_proc_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_state(HardProcentsStates.waiting_principal)
    
    await state.update_data(user_id=callback.from_user.id)
    
    await callback.message.edit_text(
        "💵 <b>Введите сумму инвестиций:</b>\n\n"
        "Например: 100000"
    )

@calculator_router.message(HardProcentsStates.waiting_principal)
async def process_principal(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.hard_proc)
            await state.clear()
            return
            
        principal = float(message.text.replace(',', '.'))
        if principal <= 0:
            await message.answer("❌ Сумма должна быть положительной. Введите сумму:")
            return
        
        await state.update_data(principal=principal)
        await state.set_state(HardProcentsStates.waiting_rate)
        await message.answer(
            f"💵 Сумма: {principal:,.0f} ₽\n\n"
            "📈 Введите годовую процентную ставку:\n\n"
            "Например: 10"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число. Введите сумму:")

@calculator_router.message(HardProcentsStates.waiting_rate)
async def process_rate(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data or 'principal' not in data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.hard_proc)
            await state.clear()
            return
            
        rate = float(message.text.replace(',', '.'))
        if rate <= 0:
            await message.answer("❌ Ставка должна быть положительной. Введите ставку:")
            return
        
        await state.update_data(rate=rate)
        await state.set_state(HardProcentsStates.waiting_years)
        
        principal = data['principal']
        
        await message.answer(
            f"💵 Сумма: {principal:,.0f} ₽\n"
            f"📈 Ставка: {rate}%\n\n"
            "⏱ Введите срок в годах:\n\n"
            "Например: 5"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число. Введите ставку:")

@calculator_router.message(HardProcentsStates.waiting_years)
async def process_years(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data or 'principal' not in data or 'rate' not in data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.hard_proc)
            await state.clear()
            return
            
        years = int(message.text)
        if years <= 0:
            await message.answer("❌ Срок должен быть положительным. Введите срок:")
            return
        if years > 100:
            await message.answer("❌ Срок не может превышать 100 лет. Введите срок:")
            return
        
        principal = data['principal']
        rate = data['rate']
        
        result = SimpleCompoundCalculator.calculate(principal, rate, years)
        
        response = (
            f"📊 <b>Результат расчета:</b>\n\n"
            f"💵 Начальная сумма: {result['principal']:,.0f} ₽\n"
            f"📈 Годовая ставка: {result['rate']}%\n"
            f"⏱ Срок: {result['years']} лет\n\n"
            f"💰 Итоговая сумма: {result['final_amount']:,.0f} ₽\n"
            f"💸 Прибыль: {result['profit']:,.0f} ₽\n\n"
            f"💡 Ваши деньги выросли в {result['final_amount']/result['principal']:.1f} раз"
        )
        
        await message.answer(response)
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите целое число. Введите срок:")


@calculator_router.message(Command('cancel'))
@calculator_router.message(F.text.casefold() == 'отмена')
async def cancel_calculation(message: Message, state: FSMContext):
    """Отмена расчета для текущего пользователя"""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активного расчета.", reply_markup=calc_kb.hard_proc)
        return
    
    await state.clear()
    await message.answer("Расчет отменен.", reply_markup=calc_kb.hard_proc)

