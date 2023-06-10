"""The base application state."""

import pynecone as pc


class AppState(pc.State):
    """The base state."""

    is_authorised: bool = False
    authorised_user_id: int = 0
