import pynecone as pc

from ..base_state import AppState
from .. import base_style as Style


def handle_logout():
    AppState.is_authorised = False
    AppState.authorised_user_id = 0
    return pc.redirect("/")


def navbar():
    """The navbar for the top of the page."""
    return pc.hstack(
        # Left anchored
        pc.hstack(
            pc.link(
                pc.heading("FriendCRM", size="md"), href="/", **Style.HEADER_LINK_STYLE
            ),
            pc.link(
                pc.heading("Analytics", size="md"),
                href="/analytics",
                **Style.HEADER_LINK_STYLE
            ),
            justify="left",
            margin_left="1em",
            padding_top="1em",
        ),
        # Right anchored
        pc.hstack(
            pc.link(
                pc.heading("Login", size="md"), href="/login", **Style.HEADER_LINK_STYLE
            ),
            pc.link(
                pc.heading("Logout", size="md"),
                href="/logout",
                **Style.HEADER_LINK_STYLE
            ),
            justify="right",
            position="fixed",
            right="1em",
            padding_top="1em",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500",
        bg=Style.ACCENT_COLOR_DARK,
    )
