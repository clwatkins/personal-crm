import pynecone as pc
from ...base_state import AppState
from ...backend import crud
import pandas as pd


class RecentPlansState(AppState):
    """The state for the recent plans modal."""

    have_recent_plans: bool = False

    @pc.var
    def recent_plans(self) -> list[dict]:
        with pc.session() as session:
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
    return pc.tr(
        pc.td(meeting["plans.what"]),
        pc.td(meeting["plans.when"]),
        pc.td(meeting["people.name"]),
    )


def recent_plans_table() -> pc.Component:
    return pc.card(
        header=pc.heading("What have you got planned?", size="lg"),
        body=pc.cond(
            RecentPlansState.have_recent_plans == False,
            pc.text("No upcoming plans -- go make some!"),
            pc.table(
                pc.thead(
                    pc.tr(
                        pc.th("What"),
                        pc.th("When"),
                        pc.th("With"),
                    )
                ),
                pc.tbody(pc.foreach(RecentPlansState.recent_plans, show_plan)),
            ),
        ),
    )
