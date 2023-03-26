import pynecone as pc
from ..components.add_form_switcher import add_form_switcher


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Welcome to FriendCRM!", font_size="2em"),
            add_form_switcher(),
        ),
        padding_top="10%",
    )
