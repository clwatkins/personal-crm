from enum import Enum, auto
import pynecone as pc
from ..base_state import State


class AddType(Enum):
    """The types of events that can be added."""

    See = auto()
    Plan = auto()


class SwitchState(State):
    """The state for the switcher."""

    checked: bool = False

    @pc.var
    def context_form_placeholder_text(self) -> str:
        if self.current_selection == AddType.See.name:
            return "What are you doing?"
        else:
            return "What are you planning?"

    @pc.var
    def people_form_placeholder_text(self) -> str:
        if self.current_selection == AddType.See.name:
            return "Who's adventuring with you?"
        else:
            return "Who are you scheming with?"

    @pc.var
    def current_selection(self):
        return AddType.Plan.name if self.checked else AddType.See.name


def action_form_switcher():
    return pc.hstack(
        pc.text("See"),
        pc.switch(is_checked=SwitchState.checked, on_change=SwitchState.set_checked),
        pc.text("Plan"),
        padding="1em",
    )
