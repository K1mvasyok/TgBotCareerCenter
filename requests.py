from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models import async_session

from models import User, Direction, Group, Course

async def is_user_registered_db(telegram_id):
    async with async_session as session:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar() is not None
    
async def save_new_user(telegram_id, course_id, direction_id, group_id):
    async with async_session as session:
        try:
            # Проверяем существование курса, направления и группы
            course = await session.get(Course, course_id)
            direction = await session.get(Direction, direction_id)
            group = await session.get(Group, group_id)

            # Если курс, направление и группа существуют, сохраняем нового пользователя
            if course and direction and group:
                new_user = User(telegram_id=telegram_id, group_id=group_id)
                session.add(new_user)
                await session.commit()
                return True, "Пользователь успешно сохранен"
            else:
                return False, "Курс, направление или группа не найдены"
        except IntegrityError:
            await session.rollback()
            return False, "Пользователь с таким телеграм ID уже существует"
        
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
    
async def get_groups_by_course_and_direction(course_id, direction_id):
    async with async_session as session:
        groups = await session.execute(
            select(Group).filter(
                Group.course_id == course_id,
                Group.direction_id == direction_id
            )
        )
        group_records = groups.scalars().all()
        return group_records
    
async def get_group_info_by_id(group_id):
    async with async_session as session:
        result = await session.execute(
            select(Group.name, Direction.name, Course.name)
            .join(Direction)
            .join(Course)
            .filter(Group.id == group_id)
        )
        group_name, direction_name, course_name = result.first()
        return group_name, direction_name, course_name
    
async def get_user_info_by_telegram_id(telegram_id):
    async with async_session as session:
        result = await session.execute(
            select(Group.name, Direction.name, Course.name)
            .join(User.group)
            .join(Direction)
            .join(Course)
            .filter(User.telegram_id == telegram_id)
        )
        user_info = result.first()
        if user_info:
            return user_info
        else:
            return None
        
async def get_users_by_course(course_id):
    async with async_session as session:
        users = await session.execute(
            select(User).join(Group).filter(Group.course_id == course_id)
        )
        return users.scalars().all()