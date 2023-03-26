import pynecone as pc
from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime


class Person(pc.Model, table=True):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(Text, unique=True, nullable=False)
    first_met = Column(DateTime, unique=False, nullable=False, default=datetime.utcnow)
    first_met_comment = Column(Text, unique=False, nullable=True)
    priority = Column(Integer, unique=False, nullable=True, default=2)
