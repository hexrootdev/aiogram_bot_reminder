from os import getenv
from dotenv import load_dotenv
from functools import wraps

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()
db_password = getenv("DB_PASSWORD")

engine = create_async_engine(f"postgresql+asyncpg://postgres:{db_password}@localhost:5432/postgres")


class Base(DeclarativeBase): pass

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True)
    email = Column(String, nullable=True)
    additional_remind_status = Column(Boolean)

    reminds = relationship("Reminds", back_populates="user", cascade="all, delete-orphan")

class Reminds(Base):
    __tablename__ = "reminds"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    date = Column(DateTime)
    text = Column(Text)

    user = relationship("Users", back_populates="reminds")


session_create = sessionmaker(
    autoflush=True, bind=engine, expire_on_commit=False, class_=AsyncSession
)


def connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_create() as session:     
            try:
                kwargs["session"] = session   
                result = await func(*args, **kwargs)
                await session.commit() 
                return result
            except:
                await session.rollback()
                raise
    return wrapper


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
