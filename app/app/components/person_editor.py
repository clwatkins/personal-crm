import reflex as rx


def person_editor(state) -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                rx.text("Name:"),
                rx.input(
                    placeholder="Select someone first",
                    value=state.edited_name,
                    on_change=state.set_edited_name,
                ),
            ),
            rx.hstack(
                rx.text("About:"),
                rx.input(
                    placeholder="Select someone first",
                    value=state.edited_about,
                    on_change=state.set_edited_about,
                ),
            ),
            rx.hstack(
                rx.text("Priority:"),
                rx.text(state.edited_priority),
                rx.slider(
                    value=state.edited_priority,
                    on_change=state.set_edited_priority,
                    min_=1,
                    max_=3,
                    width="33%",
                ),
            ),
            width="100%",
            align="left",
        ),
        rx.hstack(
            rx.button(
                "Save changes",
                on_click=state.handle_person_edit_form_submit,
                color="green",
            ),
            rx.button(
                "Delete person",
                on_click=state.handle_person_delete,
                color="red",
            ),
        ),
        rx.cond(
            state.show_person_edit_success,
            rx.alert(
                rx.alert_icon(),
                rx.alert_title("Success!"),
                status="success",
                on_mouse_move=lambda _: state.set_show_person_edit_success(False),
            ),
            None,
        ),
    )
