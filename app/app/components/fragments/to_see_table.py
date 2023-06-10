import pynecone as pc
from ...base_state import AppState
from ...backend import analytics
import pandas as pd


class ToSeeState(AppState):
    """The state for the recent history modal."""

    have_to_see: bool = False

    @pc.var
    def to_see(self) -> list[dict]:
        with pc.session() as session:
            to_see = analytics.get_to_see(
                db=session, user_id=self.authorised_user_id, limit=10
            )
        if not to_see:
            self.have_to_see = False
            return []

        self.have_to_see = True
        return to_see


def show_to_see(person):
    return pc.tr(
        pc.td(person["name"]),
        pc.td(person["total_meetings"]),
        pc.td(person["days_since_last_seen"]),
    )


def to_see_table() -> pc.Component:
    return pc.card(
        header=pc.heading("Who should you see next?", size="lg"),
        body=pc.cond(
            ToSeeState.have_to_see == False,
            pc.text("No recommendations -- go have some fun!"),
            pc.table(
                pc.thead(
                    pc.tr(
                        pc.th("Who"),
                        pc.th("Total Meetings"),
                        pc.th("Days since last Seen"),
                    )
                ),
                pc.tbody(pc.foreach(ToSeeState.to_see, show_to_see)),
            ),
        ),
    )
