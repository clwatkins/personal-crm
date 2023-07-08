import reflex as rx
from ..base_state import AppState
from .. import base_style

from ..components.navbar import navbar
from ..components.fragments.login_requirement import need_login
from ..components.fragments import most_seen_chart
from ..components.fragments import to_see_table


def analytics_page_content() -> rx.Component:
    return rx.vstack(most_seen_chart.most_seen_chart(), to_see_table.to_see_table())


def analytics() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.heading(
            "Let's get into the numbers 📊",
            font_size="2em",
            weight=base_style.BOLD_WEIGHT,
            color=base_style.ACCENT_COLOR_DARK,
        ),
        rx.cond(
            AppState.is_authorised == False,
            need_login(),
            analytics_page_content(),
        ),
        padding_top="5em",
    )
