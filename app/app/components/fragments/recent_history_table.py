import reflex as rx
from ...base_state import AppState
from ...backend import crud
import pandas as pd


class RecentHistoryState(AppState):
    """The state for the recent history modal."""

    have_recent_meetings: bool = False

    @rx.var
    def recent_meetings(self) -> list[dict]:
        with rx.session() as session:
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
    return rx.tr(
        rx.td(meeting["meetings.what"]),
        rx.td(meeting["meetings.when"]),
        rx.td(meeting["people.name"]),
    )


def recent_history_table() -> rx.Component:
    return rx.card(
        header=rx.heading("What have you done recently?", size="lg"),
        body=rx.cond(
            RecentHistoryState.have_recent_meetings == False,
            rx.text("No recent meetings -- go have some fun!"),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("What"),
                        rx.th("When"),
                        rx.th("With"),
                    )
                ),
                rx.tbody(rx.foreach(RecentHistoryState.recent_meetings, show_meeting)),
            ),
        ),
    )
