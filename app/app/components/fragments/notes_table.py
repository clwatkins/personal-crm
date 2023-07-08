import reflex as rx


def show_note(note):
    return rx.tr(
        rx.td(note.what),
        rx.td(note.when),
    )


def notes_table(state) -> rx.Component:
    return rx.box(
        rx.heading("Existing Notes", size="md"),
        rx.table(
            rx.thead(
                rx.tr(
                    rx.th("What"),
                    rx.th("When"),
                )
            ),
            rx.tbody(rx.foreach(state.current_notes, show_note)),
        ),
        border="1px solid #ccc",
        border_radius="5px",
    )
