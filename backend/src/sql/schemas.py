from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


# ============
# MEETINGS
# ============
class MeetingCreate(BaseModel):
    person_id: int
    when: Optional[datetime]
    what: Optional[str]

    class Config:
        orm_mode = True


class MeetingBase(MeetingCreate):
    id: int
    meeting_hash: str


class MeetingCreateRequest(BaseModel):
    persons: List[int]
    when: Optional[datetime]
    what: Optional[str]


# ============
# PLANS
# ============
class PlanCreateRequest(BaseModel):
    persons: List[int]
    when: Optional[datetime]
    what: Optional[str]


class PlanBase(BaseModel):
    person_id: int
    when: Optional[datetime]
    what: Optional[str]
    id: int
    plan_hash: str

    class Config:
        orm_mode = True


# ============
# NOTES
# ============
class NoteCreateRequest(BaseModel):
    when: Optional[datetime] = None
    what: Optional[str]


class NoteCreate(NoteCreateRequest):
    person_id: int

    class Config:
        orm_mode = True


class NoteBase(NoteCreate):
    id: int


# ============
# PERSONS
# ============
class PersonsCreateRequest(BaseModel):
    persons: List[str]
    what: Optional[str] = None


class PersonUpdateRequest(BaseModel):
    name: str
    first_met_comment: Optional[str] = None
    priority: Optional[int] = None


class PersonCreate(BaseModel):
    name: str
    first_met: Optional[datetime]
    first_met_comment: Optional[str] = None
    priority: Optional[int] = None

    class Config:
        orm_mode = True


class PersonBase(PersonCreate):
    id: int
    first_met: datetime


# ============
# FINAL SCHEMAS
# ============
class Person(PersonBase):
    meetings: Optional[List[MeetingBase]] = []
    plans: Optional[List[PlanBase]] = []
    notes: Optional[List[NoteBase]] = []


class Plan(PlanBase):
    person: Person


class Note(NoteBase):
    person: Person


class Meeting(MeetingBase):
    person: Person


# ============
# ANALYTICS
# ============
class MostSeenResponse(BaseModel):
    id: int
    name: str
    count: int


class ToSeeResponse(BaseModel):
    id: int
    name: str
    total_meetings: int
    days_since_last_seen: int


class PersonsSummaryResponse(BaseModel):
    id: int
    name: str
    first_met_at: datetime
    first_met_comment: str
    num_meetings: int
    last_seen_at: Optional[datetime]
    last_seen: Optional[str]


class EventsSummaryResponse(BaseModel):
    hash_id: str
    what: str
    when: datetime
    who: List[str]
