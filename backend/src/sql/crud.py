from datetime import datetime
import hashlib
from typing import List, Optional

from sqlalchemy.orm import Session

from . import models


def _get_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# ============
# USERS
# ============
def get_user(*, db: Session, email: str, with_password: bool):
    if with_password:
        return db.query(models.User).filter(models.User.email == email).first()
    else:
        return db.query(*[c for c in models.User.__table__.c if c.name != 'hashed_password']
                        ).filter(models.User.email == email).first()


def create_user(*, db: Session, email: str, name: str, hashed_password: str):
    db.add(models.User(name=name, email=email, hashed_password=hashed_password))
    db.commit()


# ============
# PERSONS
# ============
def get_persons(*, db: Session, user_id: int, limit: int):
    return db.query(models.Person).filter(models.Person.user_id == user_id).order_by(models.Person.id.desc()).limit(
        limit).all()


def get_person(*, db: Session, user_id: int, person_id: int):
    return db.query(models.Person).filter(models.Person.user_id == user_id, models.Person.id == person_id).first()


def get_people_by_name(*, db: Session, user_id: int, person_names: List[str]):
    return db.query(models.Person).filter(models.Person.user_id == user_id, models.Person.name.in_(person_names)).all()


def update_person(*, db: Session, user_id: int, person_id: int, name: str, first_met_comment: str, priority: int):
    person = get_person(db=db, user_id=user_id, person_id=person_id)
    person.name = name
    person.first_met_comment = first_met_comment
    person.priority = priority
    db.commit()


def create_persons(*, db: Session, user_id: int, names: List[str], first_met_comment: Optional[str] = None):
    utc_now = datetime.utcnow()
    db.add_all(
        [
            models.Person(
                user_id=user_id, name=name, first_met=utc_now, first_met_comment=first_met_comment
            )
            for name in names
        ]
    )
    db.commit()


# ============
# MEETINGS
# ============
def get_meetings(*, db: Session, user_id: int, limit: int):
    return (
        db.query(models.Meeting).filter(models.Meeting.user_id == user_id).order_by(models.Meeting.when.desc()).limit(
            limit).all()
    )


def create_meeting(
        *, db: Session, user_id: int, person_ids: List[int], what: str, when: Optional[datetime] = None
):
    meeting_hash = _get_hash(datetime.utcnow().isoformat() + what)

    db.add_all(
        [
            models.Meeting(
                user_id=user_id, person_id=person_id, meeting_hash=meeting_hash, when=when, what=what
            )
            for person_id in person_ids
        ]
    )
    db.commit()


# ============
# PLANS
# ============
def get_plans(*, db: Session, user_id: int, limit: int):
    return db.query(models.Plan).filter(models.Plan.user_id == user_id).order_by(models.Plan.when.desc()).limit(
        limit).all()


def create_plan(
        *, db: Session, user_id: int, person_ids: List[int], what: str, when: Optional[datetime] = None
):
    plan_hash = _get_hash(datetime.utcnow().isoformat() + what)

    db.add_all(
        [
            models.Plan(user_id=user_id, person_id=person_id, plan_hash=plan_hash, when=when, what=what)
            for person_id in person_ids
        ]
    )
    db.commit()


# ============
# NOTES
# ============
def get_notes_for_person(*, db: Session, user_id: int, person_id: int):
    return (
        db.query(models.Note)
            .filter(models.Note.user_id == user_id, models.Note.person_id == person_id)
            .order_by(models.Note.when.desc())
            .all()
    )


def create_note_for_person(
        *, db: Session, user_id: int, person_id: int, what: str, when: Optional[datetime] = None
):
    db.add(models.Note(user_id=user_id, person_id=person_id, when=when, what=what))
    db.commit()
