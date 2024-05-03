import haitch as H


def login_form() -> H.Element:
    """Login form for authenticating users."""
    return H.fragment(
        H.h1("Login"),
        H.form(action="/login", method="post")(
            H.fieldset(
                H.legend("Log in to add or edit posts"),
                H.label(for_="username")("Username:"),
                H.input(type_="text", name="username", required=True),
                H.label(for_="password")("Password:"),
                H.input(type_="password", name="password", required=True),
                H.button(type_="submit")("Login"),
            ),
        ),
    )
