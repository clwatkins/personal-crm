"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc

from .base_state import State

filename = f"{config.app_name}/{config.app_name}.py"


# Add state and page to the app.
app = pc.App(state=State)
app.compile()
