import reflex as rx
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
        with rx.session() as session:
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
                rx.console_log(f"Login success: {self.authorised_user_id}"),
                rx.redirect("/"),
            ]
        else:
            return rx.alert("Login failed")

    def handle_logout(self):
        self.is_authorised = False
        self.authorised_user_id = 0
        return rx.redirect("/")


def login_component():
    return card_page(
        header_text="Login to FriendCRM below",
        body_component=rx.vstack(
            rx.hstack(
                rx.text("Email:"),
                rx.input(
                    placeholder="Enter your email",
                    on_change=LocalLoginState.set_filled_username,
                ),
                text_align="left",
            ),
            rx.hstack(
                rx.text("Password:"),
                rx.password(
                    placerholder="Enter your password",
                    on_change=LocalLoginState.set_filled_password,
                ),
                text_align="left",
            ),
            rx.center(
                rx.button(
                    "Login",
                    on_click=LocalLoginState.handle_login,
                    **Style.ACTION_BUTTON_STYLE,
                )
            ),
        ),
    )


def logout_component() -> rx.Component:
    return card_page(
        header_text="Click below to confirm logout",
        button_text="Logout",
        button_fn=LocalLoginState.handle_logout,
    )


def login() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.cond(
            AppState.is_authorised == False,
            login_component(),
            card_page(
                header_text="You're already logged in",
                button_text="Go to Home",
                button_fn=lambda _: rx.redirect("/"),
            ),
        ),
    )


def logout() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.cond(
            AppState.is_authorised == True,
            logout_component(),
            card_page(
                header_text="You're not logged in",
                button_text="Login",
                button_fn=lambda _: rx.redirect("/login"),
            ),
        ),
    )
