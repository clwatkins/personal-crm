"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc

from .base_state import AppState
from .base_style import AppStyle, STYLESHEETS
from .pages.index import index
from .pages.analytics import analytics
from .pages.person_details import person_details
from .pages.auth import login, logout

# Add state and page to the app.
app = pc.App(state=AppState, style=AppStyle, stylesheets=STYLESHEETS)
app.add_page(analytics, route="/analytics")
app.add_page(login, route="/login")
app.add_page(logout, route="/logout")
app.add_page(index, route="/")
# app.add_page(person_details, route="/person-details")
app.compile()
