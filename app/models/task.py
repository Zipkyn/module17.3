from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)  # Ссылаемся на таблицу 'user'
    slug = Column(String, unique=True, index=True)

    user = relationship('User', back_populates='tasks')
    __table_args__ = {'extend_existing': True}

from app.backend.db import Base, engine
from app.models.user import User
from app.models.task import Task

from sqlalchemy.schema import CreateTable

print(CreateTable(User.__table__))
print(CreateTable(Task.__table__))




