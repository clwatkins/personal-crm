import pynecone as pc

config = pc.Config(
    app_name="friend-crm-app",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
