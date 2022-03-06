from collections import Counter, defaultdict
from datetime import datetime, timedelta
from dateutil import relativedelta
import logging
import math
import os
import sys
from typing import Dict, List, Optional, Union

from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .sql import crud, models, schemas
from .sql.database import SessionLocal, engine

DEFAULT_LIMIT = 1_000

try:
    SECRET_KEY = os.environ['BACKEND_SECRET_KEY']
except KeyError:
    raise KeyError('Could not find BACKEND_SECRET_KEY env variable. This is needed to sign JWT tokens.')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("api")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://67.207.69.150",
        "http://localhost",  # PROD
        "http://localhost:4000",  # PROD
        "http://localhost:3000",  # DEV (default)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============
# USERS
# ============
# From FastAPI's OAuth2 example: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)) -> Union[bool, schemas.UserInDB]:
    user = crud.get_user(db, email, with_password=True)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
                           ) -> Union[HTTPException, schemas.User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, email=token_data.email, with_password=False)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)
                                  ) -> Union[HTTPException, schemas.User]:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
                                 ) -> Union[HTTPException, Dict[str, str]]:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/user/", status_code=201)
def create_user(request: schemas.UserCreateRequest, db: Session = Depends(get_db)):
    crud.create_user(
        db, email=request.email, hashed_password=get_password_hash(request.raw_password), name=request.name)


# ============
# PERSONS
# ============
@app.get("/persons/", response_model=List[schemas.Person])
def get_persons(limit: Optional[int] = DEFAULT_LIMIT, db: Session = Depends(get_db),
                active_user: models.User = Depends(get_current_active_user)):
    logger.info('With active user %s', active_user.email)
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
