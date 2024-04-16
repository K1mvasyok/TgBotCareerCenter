from sqlalchemy import select, distinct, join
from sqlalchemy.exc import IntegrityError
from models import async_session

from models import User, Direction, Group, Course, Admin

async def is_user_registered_db(telegram_id):
    async with async_session as session:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar() is not None
    
async def save_new_user(telegram_id, course_id, direction_id, group_id):
    async with async_session as session:
        try:
            # Проверяем, существует ли пользователь с таким telegram_id
            existing_user = await session.execute(select(User).filter(User.telegram_id == telegram_id))
            existing_user = existing_user.scalar_one_or_none()

            # Если пользователь существует, обновляем его данные
            if existing_user:
                existing_user.group_id = group_id
                await session.commit()
                return True

            # Проверяем существование курса, направления и группы
            course = await session.get(Course, course_id)
            direction = await session.get(Direction, direction_id)
            group = await session.get(Group, group_id)

            # Если курс, направление и группа существуют, сохраняем нового пользователя
            if course and direction and group:
                new_user = User(telegram_id=telegram_id, group_id=group_id)
                session.add(new_user)
                await session.commit()
                return True
            else:
                return False
        except IntegrityError:
            await session.rollback()
            return False
        
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

async def get_direction_by_course_id(course_id):
    async with async_session as session:
        # Выбираем уникальные направления для указанного курса
        stmt = (
            select(distinct(Group.direction_id))
            .select_from(join(Group, Course).join(Direction))
            .where(Course.id == course_id)
        )
        result = await session.execute(stmt)
        direction_ids = [row[0] for row in result]
        
        # Затем получаем сами объекты направлений по их идентификаторам
        streams = await session.execute(select(Direction).where(Direction.id.in_(direction_ids)))
        return streams.scalars().all()
    
async def get_students_by_course_and_direction(course_id, direction_id):
    async with async_session as session:
        # Получаем идентификаторы групп для указанного курса и направления
        group_ids = await session.execute(
            select(Group.id)
            .join(Course)
            .join(Direction)
            .filter(Course.id == course_id, Direction.id == direction_id)
        )
        group_ids = [row[0] for row in group_ids.fetchall()]

        # Получаем студентов из этих групп
        students = await session.execute(
            select(User)
            .join(Group)
            .filter(Group.id.in_(group_ids))
        )
        return students.scalars().all()
    
async def get_group_by_course_and_direction(course_id, direction_id):
    async with async_session as session:
        groups = await session.execute(
            select(Group)
            .join(Course)
            .join(Direction)
            .filter(Course.id == course_id, Direction.id == direction_id)
        )
        return groups.scalars().all()
    
async def get_users_by_group_id(group_id):
    async with async_session as session:
        users = await session.execute(
            select(User)
            .filter(User.group_id == group_id)
        )
        return users.scalars().all()    
    
# Проверка на администратора 
async def is_admin(user_id):
    async with async_session as session:
        # Получаем список всех идентификаторов администраторов из базы данных
        query = select(Admin.telegram_id)
        result = await session.execute(query)
        admin_ids = [row[0] for row in result.all()]
        # Проверяем, является ли идентификатор пользователя администратором
        return user_id in admin_ids

# Сохранение администратора
async def add_admin(telegram_id):
    async with async_session as session:
        try:
            # Создаем новую запись администратора
            new_admin = Admin(telegram_id=telegram_id)
            session.add(new_admin)
            # Применяем изменения к базе данных
            await session.commit()
            return True  # Успешно добавлен администратор
        except IntegrityError:
            # Обработка случая, когда администратор с таким telegram_id уже существует
            await session.rollback()
            return False  # Администратор с таким telegram_id уже существу
    