import pynecone as pc
from ..components.navbar import navbar
from ..components.person_editor import person_editor
from ..components.fragments.person_details_selector import person_details_selector
from ..components.person_notes import person_notes
from ..base_state import AppState
from typing import Union, Optional
from ..backend import crud
from ..backend.models import Note, Person


class PersonInfo(pc.Base):
    # Qualify person_name to avoid collision with default name prop
    person_name: str = ""
    about: str = ""
    priority: int = 0


class PersonDetailsState(AppState):
    """The state for Person Details + related components."""

    @pc.var
    def current_people(self) -> list[dict[str, Union[int, str]]]:
        with pc.session() as session:
            people = crud.get_persons(
                db=session, user_id=self.authorised_user_id, limit=100
            )
        return [{"value": person.id, "label": person.name} for person in people]

    selected_person: Optional[dict[str, Union[int, str]]] = None
    selected_person_info: PersonInfo = PersonInfo()

    def set_selected_person(self, person: dict[str, Union[int, str]]):
        self.selected_person = person
        pc.console_log(f"Selected person: {self.selected_person}")
        return [
            self.set_person_info,
            self.set_edited_person_info,
            # self.set_current_notes,
        ]

    def set_person_info(self):
        with pc.session() as session:
            person: Person = crud.get_person(
                db=session,
                user_id=self.authorised_user_id,
                person_id=self.selected_person["value"],
            )
        self.selected_person_info = PersonInfo(
            name=person.name, about=person.first_met_comment, priority=person.priority
        )
        pc.console_log(f"Selected person info: {self.selected_person_info}")

    @pc.var
    def person_name(self) -> str:
        return self.selected_person_info.person_name

    @pc.var
    def person_about(self) -> str:
        return self.selected_person_info.about

    @pc.var
    def person_priority(self) -> int:
        return self.selected_person_info.priority

    # Notes
    # current_notes: list[Note] = []
    # new_note: Optional[str] = None
    # show_notes_success: bool = False
    #
    # def set_current_notes(self) -> list[Note]:
    #     if self.selected_person is None:
    #         return []
    #     with pc.session() as session:
    #         notes = crud.get_notes_for_person(
    #             db=session,
    #             user_id=self.authorised_user_id,
    #             person_id=self.selected_person["value"],
    #         )
    #     self.current_notes = notes

    def handle_notes_form_submit(self):
        pass
        # self.context_text = None
        # self.show_success = True
        # TODO: reset selected people

    # Person Editor
    show_person_edit_success: bool = False

    edited_name: Optional[str] = ""
    edited_about: Optional[str] = ""
    edited_priority: Optional[int] = ""

    def set_edited_person_info(self):
        self.edited_name = self.selected_person_info.person_name
        self.edited_about = self.selected_person_info.about
        self.edited_priority = self.selected_person_info.priority

    def handle_person_delete(self):
        pass

    def handle_person_edit_form_submit(self):
        pass
        # self.context_text = None
        # self.show_success = True
        # TODO: reset selected people


def person_details() -> pc.Component:
    return pc.vstack(
        navbar(),
        pc.heading(
            "Person Details",
            font_size="2em",
            padding_top="2em",
        ),
        pc.hstack(
            pc.text("Select a friend:"),
            person_details_selector(PersonDetailsState),
            width="100%",
        ),
        pc.divider(margin_bottom="0.5em", margin_top="0.5em"),
        # person_notes(PersonDetailsState),
        pc.divider(margin_bottom="0.5em", margin_top="0.5em"),
        person_editor(PersonDetailsState),
        border="1px solid #ccc",
        border_radius="5px",
        padding=5,
    )
