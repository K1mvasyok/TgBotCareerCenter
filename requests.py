from sqlalchemy import select, distinct, join
from sqlalchemy.exc import IntegrityError
from models import async_session

from models import User, Speciality, Group, Course, Admin

async def is_user_registered_db(telegram_id):
    async with async_session as session:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar() is not None

async def save_new_user(telegram_id, course_id, speciality_id, group_id):
    async with async_session as session:
        try:
            existing_user = await session.execute(select(User).filter(User.telegram_id == telegram_id))
            existing_user = existing_user.scalar_one_or_none()

            if existing_user:
                existing_user.group_id = group_id
                await session.commit()
                return True

            course = await session.get(Course, course_id)
            speciality = await session.get(Speciality, speciality_id)
            group = await session.get(Group, group_id)

            if course and speciality and group:
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

async def get_specialities():
    async with async_session as session:
        result = await session.execute(select(Speciality))
        return result.scalars().all()

async def get_groups_by_course_and_speciality(course_id, speciality_id):
    async with async_session as session:
        groups = await session.execute(
            select(Group).filter(
                Group.course_id == course_id,
                Group.speciality_id == speciality_id
            )
        )
        group_records = groups.scalars().all()
        return group_records

async def get_group_info_by_id(group_id):
    async with async_session as session:
        result = await session.execute(
            select(Group.name, Speciality.name, Course.name)
            .join(Speciality)
            .join(Course)
            .filter(Group.id == group_id)
        )
        group_name, speciality_name, course_name = result.first()
        return group_name, speciality_name, course_name

async def get_user_info_by_telegram_id(telegram_id):
    async with async_session as session:
        result = await session.execute(
            select(Group.name, Speciality.name, Course.name)
            .join(User.group)
            .join(Speciality)
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

async def get_specialities_by_course_id(course_id):
    async with async_session as session:
        stmt = (
            select(distinct(Group.speciality_id))
            .select_from(join(Group, Course).join(Speciality))
            .where(Course.id == course_id)
        )
        result = await session.execute(stmt)
        speciality_ids = [row[0] for row in result]

        specialities = await session.execute(select(Speciality).where(Speciality.id.in_(speciality_ids)))
        return specialities.scalars().all()

async def get_students_by_course_and_speciality(course_id, speciality_id):
    async with async_session as session:
        group_ids = await session.execute(
            select(Group.id)
            .join(Course)
            .join(Speciality)
            .filter(Course.id == course_id, Speciality.id == speciality_id)
        )
        group_ids = [row[0] for row in group_ids.fetchall()]

        students = await session.execute(
            select(User)
            .join(Group)
            .filter(Group.id.in_(group_ids))
        )
        return students.scalars().all()

async def get_groups_by_course_and_speciality(course_id, speciality_id):
    async with async_session as session:
        groups = await session.execute(
            select(Group)
            .join(Course)
            .join(Speciality)
            .filter(Course.id == course_id, Speciality.id == speciality_id)
        )
        return groups.scalars().all()

async def get_users_by_group_id(group_id):
    async with async_session as session:
        users = await session.execute(
            select(User)
            .filter(User.group_id == group_id)
        )
        return users.scalars().all()

async def is_admin(user_id):
    async with async_session as session:
        query = select(Admin.telegram_id)
        result = await session.execute(query)
        admin_ids = [row[0] for row in result.all()]
        return user_id in admin_ids

async def add_admin(telegram_id):
    async with async_session as session:
        try:
            new_admin = Admin(telegram_id=telegram_id)
            session.add(new_admin)
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False