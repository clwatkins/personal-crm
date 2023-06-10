import pynecone as pc
from datetime import datetime
from typing import Optional
from .models import Person, User, Plan, Meeting, Note
import hashlib
from sqlalchemy.engine import Row
from ..utils import iso_dt_to_display


def _get_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _flatten_row(row: Row) -> dict:
    row_output = {}
    for col in row:
        if isinstance(col, pc.Model):
            row_output.update(
                {
                    f"{col.__tablename__.lower()}.{k.lower()}": v
                    for k, v in col.dict().items()
                }
            )
        else:
            row_output.update(dict(col))
    return row_output


def make_json_safe(objs):
    def _convert(val):
        if isinstance(val, datetime):
            return iso_dt_to_display(val.isoformat())
        else:
            return val

    def _keep(key):
        return key != "_sa_instance_state"

    dicts = [_flatten_row(obj) for obj in objs]
    filtered_dicts = [{k: _convert(v) for k, v in d.items() if _keep(k)} for d in dicts]

    return filtered_dicts


# ============
# USERS
# ============
def get_user(*, db: pc.session, email: str, with_password: bool):
    if with_password:
        return db.query(User).filter(User.email == email).first()
    else:
        return (
            db.query(*[c for c in User.__fields__ if c.name != "hashed_password"])
            .filter(User.email == email)
            .first()
        )


def create_user(*, db: pc.session, email: str, name: str, hashed_password: str):
    db.add(User(name=name, email=email, hashed_password=hashed_password))
    db.commit()


# ============
# PERSONS
# ============
def get_persons(*, db: pc.session, user_id: int, limit: int):
    return (
        db.query(Person)
        .filter(Person.user_id == user_id)
        .order_by(Person.id)
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
    priority: int,
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
    first_met_comment: Optional[str] = None,
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


# ============
# MEETINGS
# ============
def get_meetings(*, db: pc.session, user_id: int, limit: int):
    return (
        db.query(Meeting, Person)
        .join(Person)
        .filter(Meeting.user_id == user_id)
        .order_by(Meeting.when.desc())
        .limit(limit)
        .all()
    )


def create_meeting(
    *,
    db: pc.session,
    user_id: int,
    person_ids: list[int],
    what: str,
    when: Optional[datetime] = None,
):
    meeting_hash = _get_hash(datetime.utcnow().isoformat() + what)

    db.add_all(
        [
            Meeting(
                user_id=user_id,
                person_id=person_id,
                meeting_hash=meeting_hash,
                when=when,
                what=what,
            )
            for person_id in person_ids
        ]
    )
    db.commit()


# ============
# PLANS
# ============
def get_plans(*, db: pc.session, user_id: int, limit: int):
    return (
        db.query(Plan, Person)
        .join(Person)
        .filter(Plan.user_id == user_id)
        .order_by(Plan.when.desc())
        .limit(limit)
        .all()
    )


def create_plan(
    *,
    db: pc.session,
    user_id: int,
    person_ids: list[int],
    what: str,
    when: Optional[datetime] = None,
):
    plan_hash = _get_hash(datetime.utcnow().isoformat() + what)

    db.add_all(
        [
            Plan(
                user_id=user_id,
                person_id=person_id,
                plan_hash=plan_hash,
                when=when,
                what=what,
            )
            for person_id in person_ids
        ]
    )
    db.commit()


# ============
# NOTES
# ============
def get_notes_for_person(*, db: pc.session, user_id: int, person_id: int):
    return (
        db.query(Note)
        .filter(Note.user_id == user_id, Note.person_id == person_id)
        .order_by(Note.when.desc())
        .all()
    )


def create_note_for_person(
    *,
    db: pc.session,
    user_id: int,
    person_id: int,
    what: str,
    when: Optional[datetime] = None,
):
    db.add(Note(user_id=user_id, person_id=person_id, when=when, what=what))
    db.commit()
