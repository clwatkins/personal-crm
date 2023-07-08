import reflex as rx

config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    frontend_packages=[
        "react-select",
    ],
)
