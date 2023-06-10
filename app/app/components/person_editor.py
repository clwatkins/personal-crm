import pynecone as pc


def person_editor(state) -> pc.Component:
    return pc.box(
        pc.box(
            pc.hstack(
                pc.text("Name:"),
                pc.input(
                    placeholder="Select someone first",
                    value=state.edited_name,
                    on_change=state.set_edited_name,
                ),
            ),
            pc.hstack(
                pc.text("About:"),
                pc.input(
                    placeholder="Select someone first",
                    value=state.edited_about,
                    on_change=state.set_edited_about,
                ),
            ),
            pc.hstack(
                pc.text("Priority:"),
                pc.text(state.edited_priority),
                pc.slider(
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
        pc.hstack(
            pc.button(
                "Save changes",
                on_click=state.handle_person_edit_form_submit,
                color="green",
            ),
            pc.button(
                "Delete person",
                on_click=state.handle_person_delete,
                color="red",
            ),
        ),
        pc.cond(
            state.show_person_edit_success,
            pc.alert(
                pc.alert_icon(),
                pc.alert_title("Success!"),
                status="success",
                on_mouse_move=lambda _: state.set_show_person_edit_success(False),
            ),
            None,
        ),
    )
