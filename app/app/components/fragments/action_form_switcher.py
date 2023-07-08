from enum import Enum, auto
import reflex as rx
from ...base_state import AppState


class AddType(Enum):
    """The types of events that can be added."""

    See = auto()
    Plan = auto()


class SwitchState(AppState):
    """The state for the switcher."""

    checked: bool = False

    @rx.var
    def context_form_placeholder_text(self) -> str:
        if self.current_selection == AddType.See.name:
            return "What are you doing?"
        else:
            return "What are you planning?"

    @rx.var
    def people_form_placeholder_text(self) -> str:
        if self.current_selection == AddType.See.name:
            return "Who's adventuring with you?"
        else:
            return "Who are you scheming with?"

    @rx.var
    def current_selection(self):
        return AddType.Plan.name if self.checked else AddType.See.name


def action_form_switcher():
    return rx.hstack(
        rx.text("See"),
        rx.switch(is_checked=SwitchState.checked, on_change=SwitchState.set_checked),
        rx.text("Plan"),
    )
