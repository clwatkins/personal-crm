import pynecone as pc
from ... import base_style


def card_page(
    *,
    header_text: str,
    body_component: None | pc.Component = None,
    button_text: str = None,
    button_fn=None
) -> pc.Component:
    return pc.flex(
        pc.card(
            header=pc.heading(header_text, size="lg"),
            body=(
                body_component
                or pc.center(
                    pc.button(
                        button_text,
                        on_click=button_fn,
                        **base_style.ACTION_BUTTON_STYLE,
                    )
                )
            ),
        ),
        padding_top="5em",
    )
