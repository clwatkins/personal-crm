"""The base application state."""

import pynecone as pc


class State(pc.State):
    """The base state."""

    authorised_user_id: int = 0
