import pynecone as pc


def show_note(note):
    return pc.tr(
        pc.td(note.what),
        pc.td(note.when),
    )


def notes_table(state) -> pc.Component:
    return pc.box(
        pc.heading("Existing Notes", size="md"),
        pc.table(
            pc.thead(
                pc.tr(
                    pc.th("What"),
                    pc.th("When"),
                )
            ),
            pc.tbody(pc.foreach(state.current_notes, show_note)),
        ),
        border="1px solid #ccc",
        border_radius="5px",
    )
