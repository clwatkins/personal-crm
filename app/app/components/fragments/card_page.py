import reflex as rx
from ... import base_style


def card_page(
    *,
    header_text: str,
    body_component: None | rx.Component = None,
    button_text: str = None,
    button_fn=None
) -> rx.Component:
    return rx.flex(
        rx.card(
            header=rx.heading(header_text, size="lg"),
            body=(
                body_component
                or rx.center(
                    rx.button(
                        button_text,
                        on_click=button_fn,
                        **base_style.ACTION_BUTTON_STYLE,
                    )
                )
            ),
        ),
        padding_top="5em",
    )
