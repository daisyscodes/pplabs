from logging.config import fileConfig
from datetime import datetime
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Event, Ticket

some_engine = create_engine('mysql+pymysql://root:the-god-delusion@127.0.0.1:3306/srenshin')

Session = sessionmaker(bind=some_engine)

session = Session()
user1 = User(username="mom", firstName="Mama", lastName="Tvoya", password="Dub3", email="mama@gmail.com", phone="+380955953555")
event1 = Event(name="Baking Day", date = datetime.now())
ticket1 = Ticket(userId = 1, eventId = 1)
session.add(user1)
session.add(event1)
session.add(ticket1)
session.commit()