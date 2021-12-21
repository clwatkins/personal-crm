from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    first_met = Column(DateTime, unique=False, nullable=False, default=datetime.utcnow)
    first_met_comment = Column(Text, unique=False, nullable=True)
    priority = Column(Integer, unique=False, nullable=False, default=2)

    meetings = relationship("Meeting", backref="person")
    plans = relationship("Plan", backref="person")
    notes = relationship("Note", backref="person")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)
    meeting_hash = Column(String(40), unique=False, nullable=False)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    when = Column(DateTime, unique=False, nullable=False, default=datetime.utcnow)
    what = Column(Text, unique=False, nullable=True)


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    plan_hash = Column(String(40), unique=False, nullable=False)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    when = Column(DateTime, unique=False, nullable=False, default=datetime.utcnow)
    what = Column(Text, unique=False, nullable=True)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    when = Column(DateTime, unique=False, nullable=False, default=datetime.utcnow)
    what = Column(Text, unique=False, nullable=True)
