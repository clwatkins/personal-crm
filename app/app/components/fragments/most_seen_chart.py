import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import reflex as rx

from ...base_state import AppState
from ...backend import analytics
from ..fragments import card_page


class MostSeenChartState(AppState):
    @rx.var
    def chart_data(self) -> pd.DataFrame:
        with rx.session() as session:
            most_seen = analytics.get_most_seen(
                db=session, user_id=self.authorised_user_id, limit=10
            )
        return pd.DataFrame(most_seen)

    @rx.var
    def chart_fig(self) -> go.Figure:
        return (
            go.Figure()
            if len(self.chart_data) == 0
            else px.bar(
                self.chart_data,
                x="name",
                y="count",
            )
        )


def most_seen_chart() -> rx.Component:
    return card_page.card_page(
        header_text="Who have you seen the most?",
        body_component=rx.plotly(
            data=MostSeenChartState.chart_fig, layout={"width": "100%", "height": "350"}
        ),
    )
