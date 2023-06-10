import pynecone as pc
from ...base_state import AppState
from ...backend import crud
import pandas as pd


class RecentHistoryState(AppState):
    """The state for the recent history modal."""

    have_recent_meetings: bool = False

    @pc.var
    def recent_meetings(self) -> list[dict]:
        with pc.session() as session:
            meetings = crud.get_meetings(
                db=session, user_id=self.authorised_user_id, limit=10
            )
        if not meetings:
            self.have_recent_meetings = False
            return []

        df = pd.DataFrame.from_records(crud.make_json_safe(meetings))
        grouped = (
            df.groupby(["meetings.what", "meetings.when"])
            .agg({"people.name": ", ".join})
            .reset_index()
        )
        self.have_recent_meetings = True
        return grouped.to_dict(orient="records")


def show_meeting(meeting):
    return pc.tr(
        pc.td(meeting["meetings.what"]),
        pc.td(meeting["meetings.when"]),
        pc.td(meeting["people.name"]),
    )


def recent_history_table() -> pc.Component:
    return pc.card(
        header=pc.heading("What have you done recently?", size="lg"),
        body=pc.cond(
            RecentHistoryState.have_recent_meetings == False,
            pc.text("No recent meetings -- go have some fun!"),
            pc.table(
                pc.thead(
                    pc.tr(
                        pc.th("What"),
                        pc.th("When"),
                        pc.th("With"),
                    )
                ),
                pc.tbody(pc.foreach(RecentHistoryState.recent_meetings, show_meeting)),
            ),
        ),
    )
