import pynecone as pc
from ..base_state import AppState
from .. import base_style as Style
from .fragments.action_form_switcher import action_form_switcher, SwitchState
from .fragments.person_selector import creatable_person_selector
from ..backend import crud
from typing import Optional, Union


def create_new_people(
    *,
    authorised_user_id: int,
    first_met_comment: str,
    new_people_names: list[str] = None
):
    with pc.session() as session:
        crud.create_persons(
            db=session,
            user_id=authorised_user_id,
            names=new_people_names,
            first_met_comment=first_met_comment,
        )

        # Get back the person object so we can create a meeting
        # based on the newly-generated person id.
        new_people_obj = crud.get_people_by_name(
            db=session,
            user_id=authorised_user_id,
            person_names=new_people_names,
        )

    return new_people_obj


class ActionFormState(AppState):
    """The state for the action form."""

    context_text: Optional[str] = None
    selected_people: Optional[list[dict[str, Union[int, str]]]] = None
    show_success: bool = False

    @pc.var
    def current_people(self) -> list[dict[str, Union[int, str]]]:
        with pc.session() as session:
            people = crud.get_persons(
                db=session, user_id=self.authorised_user_id, limit=100
            )

        return [{"value": person.id, "label": person.name} for person in people]

    def handle_form_submit(self):
        # Handle case where forms aren't properly filled:
        # - no people selected
        # - no context provided (but we could put a default in place)

        new_people = []
        existing_people_ids = []
        for person in self.selected_people:
            if "__isNew__" in person:
                new_people.append(person["label"])
            else:
                existing_people_ids.append(person["value"])

        if new_people:
            new_people_objs = create_new_people(
                authorised_user_id=self.authorised_user_id,
                first_met_comment=self.context_text,
                new_people_names=new_people,
            )
            new_people_ids = [person.id for person in new_people_objs]
        else:
            new_people_ids = []

        with pc.session() as session:
            if SwitchState.current_selection == "see":
                crud.create_meeting(
                    db=session,
                    user_id=self.authorised_user_id,
                    person_ids=existing_people_ids + new_people_ids,
                    what=self.context_text,
                )
            elif SwitchState.current_selection == "plan":
                crud.create_plan(
                    db=session,
                    user_id=self.authorised_user_id,
                    person_ids=existing_people_ids + new_people_ids,
                    what=self.context_text,
                )

        self.context_text = None
        self.show_success = True
        # TODO: reset selected people

    def create_new_people(self, new_people_names: list[str] = None):
        with pc.session() as session:
            crud.create_persons(
                db=session,
                user_id=self.authorised_user_id,
                names=new_people_names,
                first_met_comment=self.context_text,
            )

            # Get back the person object so we can create a meeting
            # based on the newly-generated person id.
            new_people_obj = crud.get_people_by_name(
                db=session,
                user_id=self.authorised_user_id,
                person_names=new_people_names,
            )

        return new_people_obj


def action_form() -> pc.Component:
    return pc.card(
        header=pc.heading("What are you up to?", size="lg"),
        body=pc.vstack(
            action_form_switcher(),
            creatable_person_selector(
                ActionFormState, ActionFormState.set_selected_people
            ),
            pc.divider(),
            pc.input(
                on_change=ActionFormState.set_context_text,
                placeholder=SwitchState.context_form_placeholder_text,
            ),
            pc.center(
                pc.button(
                    "Add",
                    on_click=ActionFormState.handle_form_submit,
                    **Style.ACTION_BUTTON_STYLE
                )
            ),
            pc.cond(
                ActionFormState.show_success,
                pc.alert(
                    pc.alert_icon(),
                    pc.alert_title("Success!"),
                    status="success",
                    on_mouse_move=lambda _: ActionFormState.set_show_success(False),
                ),
                None,
            ),
            margin="0.5em",
            display="flex",
            justify_content="left",
        ),
    )
