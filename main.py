from fasthtml import common as fh

from components import auth

app, rt = fh.fast_app(before=auth.bware)


@rt("/login")
def get():
    return auth.login_get()


@rt("/login")
def post(login: auth.Login, sess):
    return auth.login_post(login, sess)


@rt("/logout")
def logout(sess):
    return auth.logout(sess)


@rt("/protected")
def protected(auth):
    print(f"Accessing protected page. Auth: {auth}")
    return fh.Titled(
        "Protected Page", fh.H1(f"Welcome, {auth}!"), fh.A("Logout", href="/logout")
    )


@rt("/")
def home(sess):
    if auth.is_authenticated(sess):
        user = sess["user"]
        print(f"User: {user}")
        return fh.Div(
            fh.Main(
                fh.H1("Dashboard"),
                # Add your main content here
                cls="main-content",
            ),
            cls="page-container",
        )

    else:
        return fh.Titled(
            "Home", fh.H1("Welcome to the App"), fh.A("Login", href="/login")
        )


if __name__ == "__main__":
    print("Starting server")
    fh.serve(port=8080)
