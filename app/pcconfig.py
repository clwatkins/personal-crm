import pynecone as pc

config = pc.Config(
    app_name="friend_crm",
    db_url="sqlite:///pynecone.db",
    api_url="http://localhost:3000",
    bun_path="/app/.bun/bin/bun",
    frontend_packages=[
        "react-select",
    ],
)
