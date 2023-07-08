import reflex as rx
from ...base_state import AppState
from ...backend import crud
import pandas as pd


class RecentPlansState(AppState):
    """The state for the recent plans modal."""

    have_recent_plans: bool = False

    @rx.var
    def recent_plans(self) -> list[dict]:
        with rx.session() as session:
            plans = crud.get_plans(
                db=session, user_id=self.authorised_user_id, limit=10
            )
        if not plans:
            self.have_recent_plans = False
            return []

        df = pd.DataFrame.from_records(crud.make_json_safe(plans))
        grouped = (
            df.groupby(["plans.what", "plans.when"])
            .agg({"people.name": ", ".join})
            .reset_index()
        )
        self.have_recent_plans = True
        return grouped.to_dict(orient="records")


def show_plan(meeting):
    return rx.tr(
        rx.td(meeting["plans.what"]),
        rx.td(meeting["plans.when"]),
        rx.td(meeting["people.name"]),
    )


def recent_plans_table() -> rx.Component:
    return rx.card(
        header=rx.heading("What have you got planned?", size="lg"),
        body=rx.cond(
            RecentPlansState.have_recent_plans == False,
            rx.text("No upcoming plans -- go make some!"),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("What"),
                        rx.th("When"),
                        rx.th("With"),
                    )
                ),
                rx.tbody(rx.foreach(RecentPlansState.recent_plans, show_plan)),
            ),
        ),
    )
