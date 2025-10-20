from app.database.models import async_session
from app.database.models import User, Comment
from sqlalchemy import select

async def set_user(tg_id, user_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            username_to_save = user_name if user_name else "Пользователь"
            session.add(User(tg_id=tg_id, user_name=username_to_save))
            await session.commit()

async def set_comment(tg_id, comment_text):
    try:
        async with async_session() as session:
            session.add(Comment(tg_id=tg_id, comment_text=comment_text))
            await session.commit()
    except Exception as e:
        print(f"Ошибка при сохранении комментария: {e}")
