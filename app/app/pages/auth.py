import pynecone as pc
from ..base_state import AppState
from .. import base_style as Style
from ..backend import auth
from ..components.navbar import navbar
from ..components.fragments.card_page import card_page

from ..backend.models import User


class LocalLoginState(AppState):
    filled_username: str = ""
    filled_password: str = ""

    def handle_login(self):
        with pc.session() as session:
            is_success, maybe_user = auth.authenticate_user(
                self.filled_username, self.filled_password, session
            )

        # TODO: BIG REMOVE HERE
        is_success = True
        maybe_user = User(id=0)

        if is_success:
            self.is_authorised = True
            self.authorised_user_id = maybe_user.id
            return [
                pc.console_log(f"Login success: {self.authorised_user_id}"),
                pc.redirect("/"),
            ]
        else:
            return pc.alert("Login failed")

    def handle_logout(self):
        self.is_authorised = False
        self.authorised_user_id = 0
        return pc.redirect("/")


def login_component():
    return card_page(
        header_text="Login to FriendCRM below",
        body_component=pc.vstack(
            pc.hstack(
                pc.text("Email:"),
                pc.input(
                    placeholder="Enter your email",
                    on_change=LocalLoginState.set_filled_username,
                ),
                text_align="left",
            ),
            pc.hstack(
                pc.text("Password:"),
                pc.password(
                    placerholder="Enter your password",
                    on_change=LocalLoginState.set_filled_password,
                ),
                text_align="left",
            ),
            pc.center(
                pc.button(
                    "Login",
                    on_click=LocalLoginState.handle_login,
                    **Style.ACTION_BUTTON_STYLE,
                )
            ),
        ),
    )


def logout_component() -> pc.Component:
    return card_page(
        header_text="Click below to confirm logout",
        button_text="Logout",
        button_fn=LocalLoginState.handle_logout,
    )


def login() -> pc.Component:
    return pc.vstack(
        navbar(),
        pc.cond(
            AppState.is_authorised == False,
            login_component(),
            card_page(
                header_text="You're already logged in",
                button_text="Go to Home",
                button_fn=lambda _: pc.redirect("/"),
            ),
        ),
    )


def logout() -> pc.Component:
    return pc.vstack(
        navbar(),
        pc.cond(
            AppState.is_authorised == True,
            logout_component(),
            card_page(
                header_text="You're not logged in",
                button_text="Login",
                button_fn=lambda _: pc.redirect("/login"),
            ),
        ),
    )
