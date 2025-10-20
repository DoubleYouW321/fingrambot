from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import app.finans_calculator_keyboard as calc_kb

storage = MemoryStorage()
credit_router = Router()

class CreditStates(StatesGroup):
    waiting_principal = State()
    waiting_rate = State()
    waiting_years = State()

class SimpleInflCalculator:
    @staticmethod
    def calculate(principal: float, rate: float, years: int) -> dict:
        monthly_rate = rate / 12 / 100
        months = years * 12
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
        total_payment = monthly_payment * months
        overpayment = total_payment - principal
        return {
            'principal': principal,
            'rate': rate,
            'years': years,
            'monthly_payment': monthly_payment,
            'total_payment': total_payment,
            'overpayment': overpayment
        }
    
@credit_router.callback_query(F.data == 'credit_calc')
async def infl(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выбирите действие', reply_markup=calc_kb.credit)

@credit_router.callback_query(F.data == 'credit_info')
async def infl_info(callback: CallbackQuery):
    await callback.answer('')
    info_text = ("🏦 Кредитный калькулятор (аннуитетные платежи)\n\n"
        "📊 Что рассчитывает калькулятор:\n"
        "• Ежемесячный платеж\n"
        "• Общую переплату по кредиту\n"
        "• Общую сумму выплат\n"
        "• Состав платежей (проценты и основной долг)\n\n"
        "🔄 Как пользоваться:\n"
        "1. Введите сумму кредита (например: 500000)\n"
        "2. Введите годовую процентную ставку (например: 15)\n"
        "3. Введите срок кредита в годах (например: 3)\n\n"
        "📈 Пример расчета:\n"
        "Сумма: 500,000 ₽\n"
        "Ставка: 15%\n"
        "Срок: 3 года\n"
        "Результат:\n"
        "• Ежемесячный платеж: ~17,333 ₽\n"
        "• Общая переплата: ~123,988 ₽\n"
        "• Общая сумма: ~623,988 ₽\n\n"
        "💡 Аннуитетные платежи - одинаковые выплаты каждый месяц, удобно для планирования бюджета")
    await callback.message.edit_text(info_text, reply_markup=calc_kb.back_to_credit)

@credit_router.callback_query(F.data == 'credit_start')
async def credit_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_state(CreditStates.waiting_principal)
    
    await state.update_data(user_id=callback.from_user.id)
    
    await callback.message.edit_text(
        "💵 Введите сумму кредита:\n\n"
        "Например: 1000000"
    )

@credit_router.message(CreditStates.waiting_principal)
async def process_principal(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.credit)
            await state.clear()
            return
            
        principal = float(message.text.replace(',', '.'))
        if principal <= 0:
            await message.answer("❌ Сумма должна быть положительной. Введите сумму:")
            return
        
        await state.update_data(principal=principal)
        await state.set_state(CreditStates.waiting_rate)
        await message.answer(
            f"💵 Сумма: {principal:,.0f} ₽\n\n"
            "📈 Введите % ставку:\n\n"
            "Например: 10"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число. Введите сумму:")

@credit_router.message(CreditStates.waiting_rate)
async def process_rate(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data or 'principal' not in data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.credit)
            await state.clear()
            return
            
        rate = float(message.text.replace(',', '.'))
        if rate <= 0:
            await message.answer("❌ Ставка должна быть положительной. Введите ставку:")
            return
        
        await state.update_data(rate=rate)
        await state.set_state(CreditStates.waiting_years)
        
        principal = data['principal']
        
        await message.answer(
            f"💵 Сумма: {principal:,.0f} ₽\n"
            f"📈 % ставка: {rate}%\n\n"
            "⏱ Введите срок в годах:\n\n"
            "Например: 10"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число. Введите :ставку")

@credit_router.message(CreditStates.waiting_years)
async def process_years(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data or 'principal' not in data or 'rate' not in data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.credit)
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
        
        result = SimpleInflCalculator.calculate(principal, rate, years)
        
        response = (
            f"📊 Результат расчета:\n\n"
            f"💵 Начальная сумма: {result['principal']:,.0f} ₽\n"
            f"📈 Ставка %: {result['rate']}%\n"
            f"⏱ Срок: {result['years']} лет\n\n"
            f"💰 Ежемесячный платеж: {result['monthly_payment']:,.0f} ₽\n"
            f"💸 Общая сумма: {result['total_payment']:,.0f} ₽\n"
            f"Переплата: {result['overpayment']:,.0f}"
        )
        
        await message.answer(response)
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите целое число. Введите срок:")