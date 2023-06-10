import pynecone as pc
from app.components.fragments.person_selector import person_selector


def person_details_selector(state) -> pc.Component:
    return person_selector(
        state,
        state.set_selected_person,
        is_multi=False,
        is_searchable=True,
    )
