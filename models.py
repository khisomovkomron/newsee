from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    phone_number = Column(String)
    is_active = Column(Boolean, default=True)
    
    todo = relationship('Todo', back_populates='owner')
    
class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship('Users', back_populates='todo')
