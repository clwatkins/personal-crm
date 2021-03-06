from collections import Counter, defaultdict
from datetime import datetime
from dateutil import relativedelta
import logging
import math
from typing import List, Optional

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .sql import crud, models, schemas
from .sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = logging.getLogger("api")

origins = [
    "http://67.207.69.150",
    "http://localhost",  # PROD
    "http://localhost:4000",  # PROD
    "http://localhost:3000",  # DEV (default)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULT_LIMIT = 1_000


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============
# PERSONS
# ============
@app.get("/persons/", response_model=List[schemas.Person])
def get_persons(limit: Optional[int] = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, limit=limit)
    return persons


@app.post("/persons/", response_model=List[schemas.Person])
def create_persons(
    request: schemas.PersonsCreateRequest, db: Session = Depends(get_db)
):
    crud.create_persons(
        db, names=request.persons, first_met_comment=request.what
    )
    new_persons = crud.get_people_by_name(db=db, person_names=request.persons)

    return new_persons


@app.get("/person/{person_id}", response_model=schemas.Person)
def get_person(person_id: int, db: Session = Depends(get_db)):
    details = crud.get_person(db, person_id=person_id)
    return details


@app.patch("/person/{person_id}", status_code=status.HTTP_200_OK)
def update_person(
    person_id: int, request: schemas.PersonUpdateRequest, db: Session = Depends(get_db)
):
    crud.update_person(
        db,
        person_id=person_id,
        name=request.name,
        first_met_comment=request.first_met_comment,
        priority=request.priority
    )


# ============
# MEETINGS
# ============
@app.get("/meetings/", response_model=List[schemas.Meeting])
def get_meetings(limit: Optional[int] = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    meetings = crud.get_meetings(db, limit=limit)
    return meetings


@app.post("/meetings/", status_code=status.HTTP_201_CREATED)
def create_meeting(
    request: schemas.MeetingCreateRequest, db: Session = Depends(get_db)
):
    crud.create_meeting(
        db, person_ids=request.persons, when=request.when, what=request.what
    )


# ============
# PLANS
# ============
@app.get("/plans/", response_model=List[schemas.Plan])
def get_plans(limit: Optional[int] = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    plans = crud.get_plans(db, limit=limit)
    return plans


@app.post("/plans/", status_code=status.HTTP_201_CREATED)
def create_plan(request: schemas.PlanCreateRequest, db: Session = Depends(get_db)):
    crud.create_plan(
        db, person_ids=request.persons, when=request.when, what=request.what
    )


# ============
# NOTES
# ============
@app.get("/notes/{person_id}", response_model=List[schemas.Note])
def get_notes_for_person(person_id: int, db: Session = Depends(get_db)):
    notes = crud.get_notes_for_person(db, person_id)
    logging.info(notes)
    return notes


@app.post("/notes/{person_id}", status_code=status.HTTP_201_CREATED)
def create_note_for_person(
    person_id: int, request: schemas.NoteCreateRequest, db: Session = Depends(get_db)
):
    crud.create_note_for_person(
        db, person_id=person_id, when=request.when, what=request.what
    )


@app.get("/analytics/most-seen/", response_model=List[schemas.MostSeenResponse])
def get_analytics_most_seen(limit: Optional[int] = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    meetings = crud.get_meetings(db, limit=100_000)  # arbitrarily high limit
    most_common_count = Counter([meeting.person.name for meeting in meetings]).most_common(limit)
    return [{"id": i, "name": name, "count": count} for i, (name, count) in enumerate(most_common_count)]


@app.get("/analytics/persons-summary/", response_model=List[schemas.PersonsSummaryResponse])
def get_analytics_persons_summary(limit: Optional[int] = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, limit=100_000)

    persons_summary = []
    for person in persons:
        last_meeting = None
        if person.meetings:
            last_meeting = sorted(person.meetings, key=lambda m: m.id, reverse=True)[0]

        persons_summary.append(
            {
                'id': person.id,
                'name': person.name,
                'first_met_at': person.first_met,
                'first_met_comment': person.first_met_comment,
                'num_meetings': len(person.meetings),
                'last_seen_at': last_meeting.when if last_meeting else None,
                'last_seen': last_meeting.what if last_meeting else None
            }
        )

    return sorted(persons_summary, key=lambda p: p['last_seen_at'] or p['first_met_at'], reverse=True)[:limit]


@app.get("/analytics/events-summary/", response_model=List[schemas.EventsSummaryResponse])
def get_analytics_events_summary(limit: Optional[int] = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    meetings = crud.get_meetings(db, limit=100_000)

    # Reduce from people-event cardinality to event cardinality
    meetings_summary = {}
    for meeting in meetings:
        if meeting.meeting_hash in meetings_summary:
            meetings_summary[meeting.meeting_hash]['who'].append(meeting.person.name)
        else:
            meetings_summary[meeting.meeting_hash] = {
                'hash_id': meeting.meeting_hash,
                'what': meeting.what,
                'when': meeting.when,
                'who': [meeting.person.name]
            }

    return sorted(list(meetings_summary.values()), key=lambda m: m['when'], reverse=True)[:limit]


@app.get("/analytics/to-see/", response_model=List[schemas.ToSeeResponse])
def get_analytics_to_see(limit: Optional[int] = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    min_meetings = 3
    min_timedelta_days = 30

    meetings = crud.get_meetings(db, limit=100_000)  # arbitrarily high limit

    # Construct a record of how many times each person has been seen
    person_timeline = defaultdict(list)
    for meeting in meetings:
        person_timeline[meeting.person.name].append(meeting.when)

    to_see = []
    i = 0
    for person, meetings in person_timeline.items():
        # Skip anyone we haven't seen enough
        if len(meetings) < min_meetings:
            continue

        # Calculate time since we last saw person
        last_seen_gap = relativedelta.relativedelta(
            datetime.utcnow(), max(meetings)
        )
        last_seen_gap_days = (
                last_seen_gap.years * 365
                + last_seen_gap.months * 30
                + last_seen_gap.days
        )

        if last_seen_gap_days > min_timedelta_days:
            to_see.append(
                {
                    "id": i,
                    "name": person,
                    "total_meetings": len(meetings),
                    "days_since_last_seen": last_seen_gap_days,
                }
            )
            i += 1

    eps = 1e-6
    to_see.sort(
        reverse=True,
        # Sort list based on normalised length of time since last seen + number of meetings
        key=lambda d: math.log(d["days_since_last_seen"] + eps) * math.log(d["total_meetings"]),
    )
    # Truncate list to desired limit
    return to_see[:limit]
