from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.generate import ai_generate
import asyncio
import html
import app.ai_keyboard as ai_kb

ai_router = Router()

class Gen(StatesGroup):
    wait = State()


FINANCE_KEYWORDS = [
    'финанс', 'деньг', 'бюджет', 'инвест', 'кредит', 'вклад', 'сбережени', 
    'налог', 'ипотек', 'страхован', 'акци', 'облигац', 'фонд', 'крипто',
    'биткоин', 'эфир', 'депозит', 'заем', 'долг', 'доход', 'расход', 'экономи',
    'пенси', 'накоплен', 'трат', 'покупк', 'цена', 'стоимост', 'рубл', 'доллар',
    'евро', 'курс', 'валют', 'банк', 'карт', 'перевод', 'платеж', 'доллар', 'цен'
]

def is_finance_related(text: str) -> bool:
    """Проверяет, относится ли вопрос к финансам"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in FINANCE_KEYWORDS)

@ai_router.message(Command('ai_consultation'))
async def cmd_start_consultation(message: Message):
    await message.answer('🤖 Финансовый AI-консультант', reply_markup=ai_kb.consult_choose)

@ai_router.callback_query(F.data == 'start_consult')
async def cmd_start_consult(callback: CallbackQuery):
    await callback.answer('')
    with open('images\hello_ai.jpg', 'rb') as photo:
        await callback.message.answer(photo, caption='💰 Финансовый AI-консультант\n\n'
        'Задавайте вопросы по темам:\n'
        '• Инвестиции и сбережения\n'
        '• Кредиты и ипотека\n' 
        '• Бюджет и учет финансов\n'
        '• Налоги и отчетность\n'
        '• Страхование\n'
        '• Криптовалюты и акции\n\n'
        'Отвечаю только на финансовые вопросы')


@ai_router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer('⏳ Анализирую ваш финансовый вопрос...')

def split_message(text: str, max_length: int = 4096) -> list:
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        if len(paragraph) > max_length:
            sentences = paragraph.split('. ')
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 2 <= max_length:
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + ". "
        else:
            if len(current_chunk) + len(paragraph) + 2 <= max_length:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def clean_text(text: str) -> str:
    if not text:
        return ""
    
    text = text.replace('**', '').replace('__', '').replace('```', '')
    text = html.escape(text)
    
    return text

async def send_long_message(message: Message, text: str, delay: float = 0.5):
    clean_text_content = clean_text(text)
    chunks = split_message(clean_text_content)
    
    if len(chunks) == 1:
        await message.answer(chunks[0])
        return
    
    first_chunk = chunks[0] + f"\n\n📄 Сообщение 1/{len(chunks)}"
    await message.answer(first_chunk)
    
    for i, chunk in enumerate(chunks[1:], 2):
        chunk_with_counter = f"📄 Продолжение {i}/{len(chunks)}:\n\n{chunk}"
        await asyncio.sleep(delay)
        await message.answer(chunk_with_counter)

@ai_router.message()
async def generating(message: Message, state: FSMContext):
    if len(message.text) > 4000:
        await message.answer("❌ Запрос слишком длинный. Сократите до 4000 символов.")
        return
    
    if not is_finance_related(message.text):
        await message.answer(
            "❌ Я отвечаю только на финансовые вопросы.\n\n"
            "Задайте вопрос по темам:\n"
            "• Инвестиции и сбережения\n"
            "• Кредиты и бюджет\n" 
            "• Налоги и финансовое планирование"
        )
        return
    
    await state.set_state(Gen.wait)
    
    processing_msg = await message.answer("💼 Анализирую финансовый вопрос...")
    
    try:
        response = await asyncio.wait_for(
            ai_generate(message.text), 
            timeout=60
        )
        
        await processing_msg.delete()
        
        if not response or response.strip() == "":
            await message.answer("❌ Не удалось сгенерировать ответ. Попробуйте переформулировать вопрос.")
            return
        
        await send_long_message(message, response)
            
    except asyncio.TimeoutError:
        await processing_msg.delete()
        await message.answer("⏰ Превышено время ожидания. Попробуйте позже.")
    
    except Exception as e:
        await processing_msg.delete()
        error_message = str(e)
        
        if "rate limit" in error_message.lower() or "429" in error_message:
            await message.answer("🚫 Слишком много запросов. Подождите немного.")
        elif "timeout" in error_message.lower():
            await message.answer("⏰ Сервис временно недоступен. Попробуйте позже.")
        else:
            await message.answer("❌ Произошла ошибка. Попробуйте еще раз.")
    
    finally:
        await state.clear()

@ai_router.callback_query(F.data == 'consult_info')
async def cmd_help_ai(callback: CallbackQuery):
    help_text = (
        "💰 Финансовый AI-консультант\n\n"
        "Я помогу с:\n"
        "• Инвестициями и сбережениями\n"
        "• Кредитами и ипотекой\n"
        "• Составлением бюджета\n"
        "• Налоговыми вопросами\n"
        "• Финансовым планированием\n\n"
        "Как пользоваться:\n"
        "1. Задайте вопрос по финансам\n"
        "2. Получите лаконичный ответ\n"
        "3. Используйте практические советы\n\n"
        "Отвечаю только на финансовые темы"
    )
    await callback.answer('')
    await callback.message.answer(help_text, reply_markup=ai_kb.back_to_consult)