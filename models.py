from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)
async_session = AsyncSession(engine)
Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    groups = relationship("Group", back_populates="course")

class Direction(Base):
    __tablename__ = 'directions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    groups = relationship("Group", back_populates="direction")

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    direction_id = Column(Integer, ForeignKey('directions.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    direction = relationship("Direction", back_populates="groups")    
    course = relationship("Course", back_populates="groups")
    users = relationship("User", back_populates="group")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    group_id = Column(Integer, ForeignKey('groups.id'))
    
    group = relationship("Group", back_populates="users")

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)