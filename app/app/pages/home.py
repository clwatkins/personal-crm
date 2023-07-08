import reflex as rx
from ..base_state import AppState
from .. import base_style
from ..components.action_form import action_form
from ..components.fragments.recent_history_table import recent_history_table
from ..components.fragments.recent_plans_table import recent_plans_table
from ..components.navbar import navbar
from ..components.fragments.login_requirement import need_login


def homepage_content() -> rx.Component:
    return rx.grid(
        rx.grid_item(action_form(), col_span=2, row_span=1),
        rx.grid_item(recent_history_table(), col_span=1, row_span=1),
        rx.grid_item(recent_plans_table(), col_span=1, row_span=1),
        template_columns="repeat(2, 1fr)",
        template_rows="repeat(2, 1fr)",
        width="80%",
        gap=4,
    )


def home() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.heading(
            "Welcome to FriendCRM!",
            font_size="2em",
            weight=base_style.BOLD_WEIGHT,
            color=base_style.ACCENT_COLOR_DARK,
        ),
        rx.cond(
            AppState.is_authorised == False,
            need_login(),
            homepage_content(),
        ),
        padding_top="5em",
    )
