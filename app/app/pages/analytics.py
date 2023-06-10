import pynecone as pc
from ..base_state import AppState
from .. import base_style

from ..components.navbar import navbar
from ..components.fragments.login_requirement import need_login
from ..components.fragments import most_seen_chart
from ..components.fragments import to_see_table


def analytics_page_content() -> pc.Component:
    return pc.vstack(most_seen_chart.most_seen_chart(), to_see_table.to_see_table())


def analytics() -> pc.Component:
    return pc.vstack(
        navbar(),
        pc.heading(
            "Let's get into the numbers 📊",
            font_size="2em",
            weight=base_style.BOLD_WEIGHT,
            color=base_style.ACCENT_COLOR_DARK,
        ),
        pc.cond(
            AppState.is_authorised == False,
            need_login(),
            analytics_page_content(),
        ),
        padding_top="5em",
    )
