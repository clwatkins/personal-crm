import pynecone as pc
from ..components.action_form import action_form


@pc.route('/', title="FriendCRM")
def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Welcome to FriendCRM!", font_size="2em"),
            action_form(),
        ),
        padding="2em",
    )
