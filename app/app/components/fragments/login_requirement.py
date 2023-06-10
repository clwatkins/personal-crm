import pynecone as pc
from ... import base_style as style


def need_login() -> pc.Component:
    """The login requirement."""
    return pc.card(
        header=pc.heading("You need to login to access this page.", size="md"),
        body=pc.center(
            pc.button(
                "Login",
                on_click=lambda _: pc.redirect("/login"),
                **style.ACTION_BUTTON_STYLE
            )
        ),
    )
