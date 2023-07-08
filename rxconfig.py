import reflex as rx

class PersonalcrmConfig(rx.Config):
    pass

config = PersonalcrmConfig(
    app_name="personal_crm",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)