import reflex as rx
from ... import base_style as style


def need_login() -> rx.Component:
    """The login requirement."""
    return rx.card(
        header=rx.heading("You need to login to access this page.", size="md"),
        body=rx.center(
            rx.button(
                "Login", on_click=rx.redirect("/login"), **style.ACTION_BUTTON_STYLE
            )
        ),
    )
