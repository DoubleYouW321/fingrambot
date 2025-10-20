import asyncio
import logging as log
import os
from aiogram import Bot, Dispatcher

# Безопасный импорт config
try:
    from config import TOKEN, ADMIN_CHAT_ID, AI_TOKEN, DATABASE_URL
except ImportError:
    # Если config.py не доступен, берем из переменных окружения
    TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '5719962912')
    AI_TOKEN = os.getenv('AI_TOKEN')

from app.handlers import router
from app.victorinhandlers import routertest
from app.gameshandlers import games_router
from app.feedbackhandlers import feedback_router
from app.hard_proc_handlers import calculator_router
from app.ipotek_handlers import ipotek_router
from app.database.models import async_main
from app.infl_handlers import infl_router
from app.credit_calc import credit_router
from app.ai_handlers import ai_router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    try:
        await async_main()
        print("✅ Таблицы созданы успешно")
    except Exception as e:
        print(f"❌ Ошибка создания таблиц: {e}")
        return
    dp.include_router(router)
    dp.include_router(routertest)
    dp.include_router(games_router)
    dp.include_router(feedback_router)
    dp.include_router(calculator_router)
    dp.include_router(ipotek_router)
    dp.include_router(infl_router)
    dp.include_router(credit_router)
    dp.include_router(ai_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')