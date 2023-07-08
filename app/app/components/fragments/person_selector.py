# Wrapped "react-select" for multi-select dropdowns.
import reflex as rx


class CreatableSelect(rx.Component):
    library = "react-select/creatable"
    tag = "Creatable"
    is_multi: rx.Var[bool]
    is_searchable: rx.Var[bool]
    options: rx.Var[list[dict[str, str]]]
    placeholder: rx.Var[str]

    def _get_imports(self):
        return {}

    def _get_custom_code(self) -> str:
        return """
    import Creatable from 'react-select/creatable';
    """

    @classmethod
    def get_controlled_triggers(cls) -> dict[str, rx.Var]:
        return {"on_change": rx.EVENT_ARG}


class Select(rx.Component):
    library = "react-select"
    tag = "Select"
    is_multi: rx.Var[bool]
    is_searchable: rx.Var[bool]
    options: rx.Var[list[dict[str, str]]]
    placeholder: rx.Var[str]

    def _get_imports(self):
        return {}

    def _get_custom_code(self) -> str:
        # Prevent name collision with base select component
        return """
    import Select from 'react-select';
    """

    @classmethod
    def get_controlled_triggers(cls) -> dict[str, rx.Var]:
        return {"on_change": rx.EVENT_ARG}


select = Select.create
creatable_select = CreatableSelect.create


def creatable_person_selector(
    state, setter_func, is_multi: bool = True, is_searchable: bool = True
) -> rx.Component:
    return creatable_select(
        is_multi=is_multi,
        is_searchable=is_searchable,
        options=state.current_people,
        placeholder="Select or create person(s)",
        on_change=setter_func,
    )


def person_selector(
    state, setter_func, is_multi: bool = True, is_searchable: bool = True
) -> rx.Component:
    return select(
        is_multi=is_multi,
        is_searchable=is_searchable,
        options=state.current_people,
        placeholder="Select person(s)",
        on_change=setter_func,
    )
