from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

routertest = Router()

questions = [
    {
        "question": "Что такое «финансовая подушка безопасности»?",
        "options": ["Деньги на подушки", "Запас на черный день", "Инвестиции в подушки", "Кредитная карта"],
        "correct": "Запас на черный день"
    },
    {
        "question": "Что показывает кредитная история?",
        "options": ["История покупок", "Дисциплина платежей", "Количество карт", "Посещения банков"],
        "correct": "Дисциплина платежей"
    },
    {
        "question": "Что такое инфляция?",
        "options": [" Рост доллара", "Рост цен", "Рост зарплат", "Снижение ставок"],
        "correct": "Рост цен"
    },
    {
        "question": "Что такое ИИС?",
        "options": ["Социальный счет", "Налоговые льготы", "Иностранный счет", "Наличный счет"],
        "correct": "Налоговые льготы"
    },
    {
        "question": "Что такое диверсификация?",
        "options": ["Один актив", "Разные активы", "Только недвижимость", "Иностранные акции"],
        "correct": "Разные активы"
    },
    {
        "question": "Что такое капитализация процентов?",
        "options": ["Проценты на вклад", "Проценты на проценты", "Снятие процентов", "Закрытие вклада"],
        "correct": "Проценты на проценты"
    },
    {
        "question": "Что такое ПСК?",
        "options": ["Процентная ставка", "Все расходы", "Первый взнос", "Стоимость страховки"],
        "correct": "Все расходы"
    },
    {
        "question": "Что такое бюджет?",
        "options": ["План доходов/расходов", "Список покупок", "Деньги в кошельке", "Сумма кредитов"],
        "correct": "План доходов/расходов"
    },
    {
        "question": "Что такое дебетовая карта?",
        "options": ["Кредитный лимит", "Собственные деньги", "Только онлайн", "Бонусная карта"],
        "correct": "Собственные деньги"
    },
    {
        "question": "Что такое пассивный доход?",
        "options": ["Работа по найму", "Доход без действий", "Разовые подработки", "Продажа вещей"],
        "correct": "Доход без действий"
    }
]

user_scores = {}
user_questions_index = {}

@routertest.message(Command('starttest'))
async def start_test(message: Message):
    chat_id = message.from_user.id
    user_scores[chat_id] = 0
    user_questions_index[chat_id] = 0
    await message.answer('Приветствуем вас в викторине! 🧠\nОтвечайте на вопросы, выбирая один из вариантов ответа.')
    await send_question(message, chat_id)

async def send_question(message: Message, chat_id):
    current_index = user_questions_index[chat_id]
    
    if current_index >= len(questions):
        score = user_scores[chat_id]
        total = len(questions)
        # Явно удаляем клавиатуру
        await message.answer(
            f'🏆 Викторина завершена!\nВаш результат: {score} из {total}', 
            reply_markup=ReplyKeyboardRemove()
        )
        del user_questions_index[chat_id]
        del user_scores[chat_id]
        return
    
    question = questions[current_index]
    markup = ReplyKeyboardBuilder()
    for option in question['options']:
        markup.add(KeyboardButton(text=option))
    markup.add(KeyboardButton(text='❌ Завершить викторину'))
    markup.adjust(1)

    await message.answer(
        f"Вопрос {current_index + 1}/{len(questions)}:\n{question['question']}", 
        reply_markup=markup.as_markup(resize_keyboard=True)
    )

@routertest.message(F.text == '❌ Завершить викторину')
async def cancel_quiz(message: Message):
    chat_id = message.from_user.id
    if chat_id in user_scores:
        score = user_scores[chat_id]
        total = len(questions)
        # Явно удаляем клавиатуру
        await message.answer(
            f"Викторина прервана.\nВаш результат: {score} из {total}",
            reply_markup=ReplyKeyboardRemove()
        )
        if chat_id in user_questions_index:
            del user_questions_index[chat_id]
        if chat_id in user_scores:
            del user_scores[chat_id]

@routertest.message(F.text.in_([option for question in questions for option in question['options']]))
async def check_answer(message: Message):
    chat_id = message.from_user.id
    
    if chat_id not in user_questions_index or chat_id not in user_scores:
        await message.answer("Начните викторину командой /starttest")
        return
    
    current_index = user_questions_index[chat_id]

    if current_index >= len(questions):
        return
    
    question = questions[current_index]
    
    if message.text == question['correct']:
        user_scores[chat_id] += 1
        await message.answer("✅ Правильно!", reply_markup=ReplyKeyboardRemove())
    else:
        correct_answer = question['correct']
        await message.answer(f"❌ Неправильно! Правильный ответ: {correct_answer}", reply_markup=ReplyKeyboardRemove())
    
    import asyncio
    await asyncio.sleep(1)
    
    user_questions_index[chat_id] += 1
    await send_question(message, chat_id)