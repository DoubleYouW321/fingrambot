from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import String, BigInteger, Text
import os

# Автоматическое определение URL для любой БД
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///db.sqlite')

# Конвертируем для async PostgreSQL
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+asyncpg://', 1)

# Создаем engine
engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    user_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

class Comment(Base):
    __tablename__ = 'feedback'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    comment_text: Mapped[str] = mapped_column(Text())  # Text для PostgreSQL

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)