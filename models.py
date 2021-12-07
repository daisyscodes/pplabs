from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, Text, PrimaryKeyConstraint, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    firstName = Column(String(32), nullable=False)
    lastName = Column(String(32), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(32), nullable=False, unique=True)
    phone = Column(String(32), nullable=False, unique=True)

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    date = Column(Date, nullable=False)


class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    eventId = Column(Integer, ForeignKey('event.id'))
    isBooked = Column(Boolean, default=False)
    isBought = Column(Boolean, default=False)
    users = relationship('User')
    events = relationship('Event')
   