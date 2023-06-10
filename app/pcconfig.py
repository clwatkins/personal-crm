import pynecone as pc

config = pc.Config(
    app_name="app",
    db_url="sqlite:///pynecone.db",
    api_url="http://localhost:3000",
    frontend_packages=[
        "react-select",
    ],
)
