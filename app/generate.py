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
                        
ПРАВИЛА:
1. Отвечай только на финансы, инвестиции, кредиты, бюджет
2. Будь лаконичным (3-5 предложений)
3. Давай практические советы
4. Если вопрос не о финансах - вежливо откажись
5. Не предсказывай будущее (курсы, цены)
6. Форматируй кратко и по делу"""
                    },
                    {
                        "role": "user", 
                        "content": text
                    }
                ],
                timeout=20,
                max_tokens=400
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Модель {model} недоступна: {e}")
            continue 
    
    return "⚠️ Все финансовые модели временно перегружены. Попробуйте позже."
