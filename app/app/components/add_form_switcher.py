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
    current_selection = AddType.See.name

    def change_check(self, checked):
        self.checked = checked
        self.current_selection = AddType.Plan.name if checked else AddType.See.name


def add_form_switcher():
    return pc.hstack(
        pc.text('See'),
        pc.switch(is_checked=SwitchState.checked, on_change=SwitchState.change_check),
        pc.text('Plan'),
    )
