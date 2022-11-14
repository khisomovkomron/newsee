from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


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
    address_id = Column(Integer, ForeignKey('address.id'), nullable=True)
    
    todo = relationship('Todo', back_populates='owner')
    address = relationship('Address', back_populates='user_address')
    
class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship('Users', back_populates='todo')
    

class Address(Base):
    __tablename__ = 'address'
    
    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postalcode = Column(String)
    apt_num = Column(Integer)

    user_address = relationship('Users', back_populates='address')
    
    
class Archive(Base):
    __tablename__ = 'archive'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(Boolean)
