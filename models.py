from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)
async_session = AsyncSession(engine)
Base = declarative_base()

# Ассоциативная таблица для связи курсов и направлений (специальностей)
course_speciality_association = Table(
    'course_speciality_association',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('speciality_id', Integer, ForeignKey('specialities.id'), primary_key=True)
)

# Таблица для Курсов
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    groups = relationship("Group", back_populates="course")
    specialities = relationship("Speciality", secondary=course_speciality_association, back_populates="courses")

# Таблица для Специальностей
class Speciality(Base):
    __tablename__ = 'specialities'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    groups = relationship("Group", back_populates="speciality")
    courses = relationship("Course", secondary=course_speciality_association, back_populates="specialities")

# Таблица для Групп
class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    speciality_id = Column(Integer, ForeignKey('specialities.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    speciality = relationship("Speciality", back_populates="groups")
    course = relationship("Course", back_populates="groups")
    users = relationship("User", back_populates="group")

# Таблица для Пользователей
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship("Group", back_populates="users")

# Таблица для Администраторов
class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)