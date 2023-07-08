"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx

from .base_state import AppState
from .base_style import AppStyle, STYLESHEETS
from .pages.home import home
from .pages.analytics import analytics
from .pages.person_details import person_details
from .pages.auth import login, logout

# Add state and page to the app.
app = rx.App(state=AppState, style=AppStyle, stylesheets=STYLESHEETS)
app.add_page(analytics, route="/analytics", title="FriendCRM: Analytics")
app.add_page(login, route="/login", title="FriendCRM: Login")
app.add_page(logout, route="/logout", title="FriendCRM: Logout")
app.add_page(home, route="/", title="FriendCRM")
# app.add_page(person_details, route="/person-details")
app.compile()
