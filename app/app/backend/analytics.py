import pynecone as pc
from dateutil import relativedelta
from collections import Counter, defaultdict
import math
from . import crud
from datetime import datetime

DEFAULT_LIMIT = 1_000


def get_most_seen(db: pc.session, user_id: int, limit: int = 100):
    meetings = crud.get_meetings(
        db=db, user_id=user_id, limit=100_000
    )  # arbitrarily high limit
    most_common_count = Counter(
        [person.name for meeting, person in meetings]
    ).most_common(limit)
    return [
        {"id": i, "name": name, "count": count}
        for i, (name, count) in enumerate(most_common_count)
    ]


def get_to_see(db: pc.session, user_id: int, limit: int = 100):
    min_meetings = 3
    min_timedelta_days = 30

    meetings = crud.get_meetings(
        db=db, user_id=user_id, limit=100_000
    )  # arbitrarily high limit

    # Construct a record of how many times each person has been seen
    person_timeline = defaultdict(list)
    for meeting, person in meetings:
        person_timeline[person.name].append(meeting.when)

    to_see = []
    i = 0
    for person, meetings in person_timeline.items():
        # Skip anyone we haven't seen enough
        if len(meetings) < min_meetings:
            continue

        # Calculate time since we last saw person
        last_seen_gap = relativedelta.relativedelta(datetime.utcnow(), max(meetings))
        last_seen_gap_days = (
            last_seen_gap.years * 365 + last_seen_gap.months * 30 + last_seen_gap.days
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
        key=lambda d: math.log(d["days_since_last_seen"] + eps)
        * math.log(d["total_meetings"]),
    )
    # Truncate list to desired limit
    return to_see[:limit]
