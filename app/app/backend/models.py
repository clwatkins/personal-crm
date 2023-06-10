import pynecone as pc
from sqlmodel import Field
from datetime import datetime
from typing import Optional


class User(pc.Model, table=True):
    __tablename__ = "users"
    email: str = Field(unique=True, nullable=False)
    name: str = Field(unique=False, nullable=False)
    hashed_password: str = Field(unique=False, nullable=False)
    disabled: bool = Field(nullable=False, default=False)
    created_at: datetime = Field(
        unique=False, nullable=False, default_factory=datetime.utcnow
    )


class Person(pc.Model, table=True):
    __tablename__ = "people"

    user_id: int = Field(
        nullable=False,
        foreign_key="users.id",
    )
    name: str = Field(unique=True, nullable=False)
    first_met: datetime = Field(
        default_factory=datetime.utcnow, unique=False, nullable=False
    )
    first_met_comment: Optional[str] = Field(None, unique=False, nullable=True)
    priority: int = Field(2, unique=False, nullable=True)


class Meeting(pc.Model, table=True):
    __tablename__ = "meetings"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id", nullable=False)
    meeting_hash: str = Field(default=None, max_length=40, unique=False, nullable=False)
    person_id: int = Field(default=None, foreign_key="people.id", nullable=False)
    when: datetime = Field(
        default_factory=datetime.utcnow, unique=False, nullable=False
    )
    what: Optional[str] = Field(None, unique=False, nullable=True)


class Plan(pc.Model, table=True):
    __tablename__ = "plans"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id", nullable=False)
    plan_hash: str = Field(default=None, max_length=40, unique=False, nullable=False)
    person_id: int = Field(default=None, foreign_key="people.id", nullable=False)
    when: datetime = Field(
        default_factory=datetime.utcnow, unique=False, nullable=False
    )
    what: Optional[str] = Field(None, unique=False, nullable=True)


class Note(pc.Model, table=True):
    __tablename__ = "notes"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id", nullable=False)
    person_id: int = Field(default=None, foreign_key="people.id", nullable=False)
    when: datetime = Field(
        default_factory=datetime.utcnow, unique=False, nullable=False
    )
    what: Optional[str] = Field(None, unique=False, nullable=True)
