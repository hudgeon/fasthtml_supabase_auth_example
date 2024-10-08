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
        "Protected Page",
        fh.P(f"Welcome, {auth}!"),
        fh.A("Back", href="/"),
        fh.P(),
        fh.A("Logout", href="/logout"),
    )


@rt("/")
def home(sess):
    if auth.is_authenticated(sess):
        user = sess["user"]
        print(f"User: {user}")
        return fh.Titled(
            "Dashboard",
            fh.P(f"Welcome, {user}!"),
            fh.P("You are logged in. View a protected page below."),
            fh.A("Protected Page", href="/protected"),
            fh.P(),
            fh.P("Logout here:"),
            fh.A("Logout", href="/logout"),
        )

    else:
        return fh.Titled(
            "Home", fh.H1("Welcome to the App"), fh.A("Login", href="/login")
        )


if __name__ == "__main__":
    print("Starting server")
    fh.serve(port=8080)
