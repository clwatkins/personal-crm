from datetime import datetime
import hashlib
from typing import List, Optional

from sqlalchemy.orm import Session

from . import models


def _get_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# ============
# PERSONS
# ============
def get_persons(db: Session, limit: int):
    return db.query(models.Person).limit(limit).all()


def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()


def update_person(db: Session, person_id: int, name: str, first_met_comment: str):
    person = get_person(db, person_id)
    person.name = name
    person.first_met_comment = first_met_comment
    db.commit()


def create_persons(db: Session, names: List[str], first_met_comment: Optional[str] = None):
    utc_now = datetime.utcnow()
    db.add_all(
        [
            models.Person(
                name=name, first_met=utc_now, first_met_comment=first_met_comment
            )
            for name in names
        ]
    )

    db.commit()


# ============
# MEETINGS
# ============
def get_meetings(db: Session, limit: int):
    return (
        db.query(models.Meeting).order_by(models.Meeting.when.desc()).limit(limit).all()
    )


def create_meeting(
    db: Session, person_ids: List[int], what: str, when: Optional[datetime] = None
):
    meeting_hash = _get_hash(datetime.utcnow().isoformat() + what)

    db.add_all(
        [
            models.Meeting(
                person_id=person_id, meeting_hash=meeting_hash, when=when, what=what
            )
            for person_id in person_ids
        ]
    )
    db.commit()


# ============
# PLANS
# ============
def get_plans(db: Session, limit: int):
    return db.query(models.Plan).order_by(models.Plan.when.desc()).limit(limit).all()


def create_plan(
    db: Session, person_ids: List[int], what: str, when: Optional[datetime] = None
):
    plan_hash = _get_hash(datetime.utcnow().isoformat() + what)

    db.add_all(
        [
            models.Plan(person_id=person_id, plan_hash=plan_hash, when=when, what=what)
            for person_id in person_ids
        ]
    )
    db.commit()


# ============
# NOTES
# ============
def get_notes_for_person(db: Session, person_id: int):
    return (
        db.query(models.Note)
        .filter(models.Note.person_id == person_id)
        .order_by(models.Note.when.desc())
        .all()
    )


def create_note_for_person(
    db: Session, person_id: int, what: str, when: Optional[datetime] = None
):
    db.add(models.Note(person_id=person_id, when=when, what=what))
    db.commit()
