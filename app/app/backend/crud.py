import pynecone as pc
from datetime import datetime
from typing import Optional
from .models import Person

from ..base_state import State


# ============
# PERSONS
# ============
def get_persons(*, db: pc.session, user_id: int, limit: int):
    return (
        db.query(Person)
        .filter(Person.user_id == user_id)
        .order_by(Person.id.desc())
        .limit(limit)
        .all()
    )


def get_person(*, db: pc.session, user_id: int, person_id: int):
    return (
        db.query(Person)
        .filter(Person.user_id == user_id, Person.id == person_id)
        .first()
    )


def get_people_by_name(*, db: pc.session, user_id: int, person_names: list[str]):
    return (
        db.query(Person)
        .filter(Person.user_id == user_id, Person.name.in_(person_names))
        .all()
    )


def update_person(
    *,
    db: pc.session,
    user_id: int,
    person_id: int,
    name: str,
    first_met_comment: str,
    priority: int
):
    person = get_person(db=db, user_id=user_id, person_id=person_id)
    person.name = name
    person.first_met_comment = first_met_comment
    person.priority = priority
    db.commit()


def create_persons(
    *,
    db: pc.session,
    user_id: int,
    names: list[str],
    first_met_comment: Optional[str] = None
):
    utc_now = datetime.utcnow()
    db.add_all(
        [
            Person(
                user_id=user_id,
                name=name,
                first_met=utc_now,
                first_met_comment=first_met_comment,
            )
            for name in names
        ]
    )
    db.commit()
