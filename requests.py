from sqlalchemy import select
from models import async_session

from models import User, Direction

async def is_user_registered_db(telegram_id):
    async with async_session as session:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar() is not None
    
async def save_user_to_db(telegram_id, data):
    async with async_session as session:
        User_instance = await session.merge(User(telegram_id=telegram_id))
        User_instance.kurs = data['kurs']
        User_instance.direction = data['direction']
        User_instance.group = data['group']

        await session.commit()
        
async def get_user_data(telegram_id):
    async with async_session as session:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalar()
        return user

async def get_direction():
    async with async_session as session:
        result = await session.execute(select(Direction))
        return result.scalars().all()