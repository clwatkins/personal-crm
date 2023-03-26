import pynecone as pc
from ..base_state import State
from .action_form_switcher import action_form_switcher, SwitchState
from ..backend import crud


class ActionFormState(State):
    """The state for the action form."""

    context_text: str = None
    person: str = None
    new_person: str = None
    current_people: list[str] = []

    @pc.var
    def get_current_people(self):
        with pc.session() as session:
            people = crud.get_persons(
                db=session, user_id=self.authorised_user_id, limit=100
            )

        self.current_people = [person.name for person in people]

    def create_new_people(self):
        with pc.session() as session:
            crud.create_persons(
                db=session,
                user_id=self.authorised_user_id,
                names=[self.new_person],
                first_met_comment=self.context_text,
            )


def action_form() -> pc.Component:
    return pc.container(
        pc.heading("What are you up to?"),
        action_form_switcher(),
        pc.hstack(
            pc.select(
                options=ActionFormState.current_people,
                on_change=ActionFormState.set_person,
                placeholder=SwitchState.people_form_placeholder_text,
            ),
            pc.input(
                on_change=ActionFormState.set_new_person,
                placeholder="If they're a new compadre add them here!",
            ),
        ),
        pc.input(
            on_change=ActionFormState.set_context_text,
            placeholder=SwitchState.context_form_placeholder_text,
        ),
        pc.button("Add", on_click=ActionFormState.create_new_people),
        padding="2em",
        border="1px solid #ccc",
        border_radius="5px",
        margin="1em",
    )
