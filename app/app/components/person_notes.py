import reflex as rx
from .fragments.notes_table import notes_table


def person_notes(state) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.input(
                on_change=state.set_new_note,
                placeholder="What have you learned about this person?",
            ),
            notes_table(state),
        )
    )
