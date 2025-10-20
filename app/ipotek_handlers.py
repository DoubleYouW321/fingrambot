from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import app.finans_calculator_keyboard as calc_kb

storage = MemoryStorage()
ipotek_router = Router()

class IpotekStates(StatesGroup):
    waiting_principal = State()
    waiting_rate = State()
    waiting_years = State()

class SimpleIpotekCalculator:
    @staticmethod
    def calculate(principal: float, rate: float, years: int) -> dict:

        months = years * 12
        months_rate = rate / 12 /100
        months_pay = principal * (months_rate * (1 + months_rate)**months) / ((1 + months_rate)**months - 1) 
        full_sum = months_pay * months
        overpayment = full_sum - principal
        return {
            'principal': principal,
            'rate': rate,
            'years': years,
            'months_pay': months_pay,
            'overpayment': overpayment,
            'full_sum': full_sum
        }


@ipotek_router.callback_query(F.data == 'ipotek_calc')
async def ipotek(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выбирите действие', reply_markup=calc_kb.ipotek)

@ipotek_router.callback_query(F.data == 'ipotek_info')
async def ipotek_info(callback: CallbackQuery):
    await callback.answer('')
    info_text = ("🏠 Ипотечный калькулятор\n\n"
        "📊 Что рассчитывает калькулятор:\n"
        "• Ежемесячный платеж\n"
        "• Общую переплату по кредиту\n"
        "• Общую сумму выплат\n"
        "• Эффективную процентную ставку\n\n"
        "🔄 Как пользоваться:\n"
        "1. Введите сумму кредита (например: 5000000)\n"
        "2. Введите годовую процентную ставку (например: 7.5)\n"
        "3. Введите срок кредита в годах (например: 20)\n\n"
        "📈 Пример расчета:\n"
        "Сумма: 5,000,000 ₽\n"
        "Ставка: 7.5%\n"
        "Срок: 20 лет\n"
        "Результат:\n"
        "• Платеж: ~40,742 ₽/мес\n"
        "• Переплата: ~4,778,080 ₽\n"
        "• Общая сумма: ~9,778,080 ₽\n\n")
    await callback.message.edit_text(info_text, reply_markup=calc_kb.back_to_ipotek)

@ipotek_router.callback_query(F.data == 'ipotek_start')
async def infl_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_state(IpotekStates.waiting_principal)
    
    await state.update_data(user_id=callback.from_user.id)
    
    await callback.message.edit_text(
        "💵 Введите сумму ипотеки:\n\n"
        "Например: 1000000"
    )

@ipotek_router.message(IpotekStates.waiting_principal)
async def process_principal(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.ipotek)
            await state.clear()
            return
            
        principal = float(message.text.replace(',', '.'))
        if principal <= 0:
            await message.answer("❌ Сумма должна быть положительной. Введите сумму:")
            return
        
        await state.update_data(principal=principal)
        await state.set_state(IpotekStates.waiting_rate)
        await message.answer(
            f"💵 Сумма: {principal:,.0f} ₽\n\n"
            "📈 Введите годовую процентную ставку:\n\n"
            "Например: 10"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число. Введите сумму:")

@ipotek_router.message(IpotekStates.waiting_rate)
async def process_rate(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data or 'principal' not in data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.ipotek)
            await state.clear()
            return
            
        rate = float(message.text.replace(',', '.'))
        if rate <= 0:
            await message.answer("❌ Ставка должна быть положительной. Введите ставку:")
            return
        
        await state.update_data(rate=rate)
        await state.set_state(IpotekStates.waiting_years)
        
        principal = data['principal']
        
        await message.answer(
            f"💵 Сумма: {principal:,.0f} ₽\n"
            f"📈 Ставка: {rate}%\n\n"
            "⏱ Введите срок ипотеки в годах:\n\n"
            "Например: 10"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число. Введите ставку:")

@ipotek_router.message(IpotekStates.waiting_years)
async def process_years(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if not data or 'principal' not in data or 'rate' not in data:
            await message.answer("❌ Сессия устарела. Начните расчет заново.", reply_markup=calc_kb.ipotek)
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
        
        result = SimpleIpotekCalculator.calculate(principal, rate, years)
        
        response = (
            f"📊 Результат расчета:\n\n"
            f"💵 Начальная сумма: {result['principal']:,.0f} ₽\n"
            f"📈 Годовая ставка: {result['rate']}%\n"
            f"⏱ Срок: {result['years']} лет\n\n"
            f"💰 Ежемесяный платеж: {result['months_pay']:,.0f} ₽\n"
            f"💸 Общая переплата: {result['overpayment']:,.0f} ₽\n\n"
            f"💰 Общая сумма {result['full_sum']:,.0f} ₽"
        )
        
        await message.answer(response)
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите целое число. Введите срок:")

@ipotek_router.message(Command('cancel'))
@ipotek_router.message(F.text.casefold() == 'отмена')
async def cancel_calculation(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активного расчета.", reply_markup=calc_kb.ipotek)
        return
    
    await state.clear()
    await message.answer("Расчет отменен.", reply_markup=calc_kb.ipotek)

