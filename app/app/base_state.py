"""The base application state."""

import reflex as rx


class AppState(rx.State):
    """The base state."""

    is_authorised: bool = False
    authorised_user_id: int = 0
