import reflex as rx
from ...base_state import AppState
from ...backend import analytics
import pandas as pd


class ToSeeState(AppState):
    """The state for the recent history modal."""

    have_to_see: bool = False

    @rx.var
    def to_see(self) -> list[dict]:
        with rx.session() as session:
            to_see = analytics.get_to_see(
                db=session, user_id=self.authorised_user_id, limit=10
            )
        if not to_see:
            self.have_to_see = False
            return []

        self.have_to_see = True
        return to_see


def show_to_see(person):
    return rx.tr(
        rx.td(person["name"]),
        rx.td(person["total_meetings"]),
        rx.td(person["days_since_last_seen"]),
    )


def to_see_table() -> rx.Component:
    return rx.card(
        header=rx.heading("Who should you see next?", size="lg"),
        body=rx.cond(
            ToSeeState.have_to_see == False,
            rx.text("No recommendations -- go have some fun!"),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("Who"),
                        rx.th("Total Meetings"),
                        rx.th("Days since last Seen"),
                    )
                ),
                rx.tbody(rx.foreach(ToSeeState.to_see, show_to_see)),
            ),
        ),
    )
