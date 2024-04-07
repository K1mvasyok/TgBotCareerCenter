from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)
async_session = AsyncSession(engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    kurs = Column(Integer)
    direction = Column(String) # Направление
    group = Column(String) 


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
