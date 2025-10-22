from openai import AsyncOpenAI
from config import AI_TOKEN
import asyncio
import random

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_TOKEN,
)

FINANCE_MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "google/gemini-2.0-flash-thinking-exp:free",
    "google/gemini-flash-1.5-8b:free",
    
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-3.1-8b-instruct:free", 
    "meta-llama/llama-3.2-3b-instruct:free",
    "meta-llama/llama-3-70b-instruct:free",
    
    "qwen/qwen-2.5-72b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
    "qwen/qwen-2-72b-instruct:free",
]

async def ai_generate(text: str):
    random.shuffle(FINANCE_MODELS)
    
    for model in FINANCE_MODELS:
        try:
            completion = await client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": """Ты финансовый консультант. Отвечай ТОЛЬКО на финансовые вопросы.
                        
ВАЖНЫЕ ПРАВИЛА:
1. Отвечай ТОЛЬКО на русском языке
2. Отвечай только на финансы, инвестиции, кредиты, бюджет
3. Будь лаконичным (3-5 предложений)
4. Давай практические советы
5. Если вопрос не о финансах - вежливо откажись
6. Не предсказывай будущее (курсы, цены)
7. Форматируй кратко и по делу
8. Используй только русский язык в ответах

Пример хорошего ответа:
"Для накопления на квартиру рекомендую открыть вклад под 8% годовых. Откладывайте 20% от дохода ежемесячно. Рассмотрите ИИС для налоговых вычетов."

НЕ используй английские слова, только русский язык!"""
                    },
                    {
                        "role": "user", 
                        "content": text
                    }
                ],
                timeout=20,
                max_tokens=400
            )
            
            response = completion.choices[0].message.content
            
            if response and is_response_russian(response):
                return response
            else:
                print(f"Модель {model} вернула не русский ответ, пробуем следующую...")
                continue
                
        except Exception as e:
            print(f"Модель {model} недоступна: {e}")
            continue 
    
    return "⚠️ Все финансовые модели временно перегружены. Попробуйте позже."

def is_response_russian(text: str) -> bool:
    """Проверяет, что ответ на русском языке"""
    if not text:
        return False
    
    # Считаем русские и английские буквы
    russian_chars = sum(1 for char in text if 'а' <= char.lower() <= 'я' or char in 'ёЁ')
    english_chars = sum(1 for char in text if 'a' <= char.lower() <= 'z')
    
    total_letters = russian_chars + english_chars
    if total_letters == 0:
        return True  # Если нет букв, считаем допустимым
    
    russian_ratio = russian_chars / total_letters
    return russian_ratio >= 0.8  # 80% текста должно быть на русском