import pynecone as pc
from .fragments.notes_table import notes_table


def person_notes(state) -> pc.Component:
    return pc.box(
        pc.hstack(
            pc.input(
                on_change=state.set_new_note,
                placeholder="What have you learned about this person?",
            ),
            notes_table(state),
        )
    )
