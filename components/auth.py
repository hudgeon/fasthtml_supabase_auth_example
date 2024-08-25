import os
from dataclasses import dataclass

from fasthtml import common as fh
from starlette.responses import RedirectResponse
from supabase import Client, create_client

# Initialize Supabase client
supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
)


@dataclass
class Login:
    email: str
    password: str


def before(req, sess):
    print(f"Before middleware: Session content - {sess}")
    auth = req.scope["auth"] = sess.get("user")
    print(f"Before middleware: Auth value - {auth}")
    if not auth:
        print("Before middleware: No auth, redirecting to login")
        return RedirectResponse("/login", status_code=303)
    print("Before middleware: Auth found, proceeding")


bware = fh.Beforeware(
    before, skip=[r"/favicon\.ico", r"/static/.*", r".*\.css", "/login", "/"]
)


def login_get():
    print("Rendering login page")
    frm = fh.Form(
        fh.Input(type="email", name="email", placeholder="Email"),
        fh.Input(type="password", name="password", placeholder="Password"),
        fh.Button("Log in", type="submit"),
        action="/login",
        method="post",
    )
    return fh.Titled("Login", frm)


def login_post(login: Login, sess):
    print(f"Login attempt for email: {login.email}")
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": login.email, "password": login.password}
        )
        print(f"Supabase login response: {response}")
        sess["user"] = response.user.email
        print(f"Session after login: {sess}")
        print("Redirecting to protected page")
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        print(f"Login failed with error: {str(e)}")
        return fh.Titled("Login Failed", fh.P(str(e)))


def logout(sess):
    print(f"Logging out. Session before clear: {sess}")
    sess.clear()
    print(f"Session after clear: {sess}")
    return RedirectResponse("/login", status_code=303)


# Helper functions
def set_user_session(sess, user_email):
    sess["user"] = user_email


def clear_session(sess):
    sess.clear()


def is_authenticated(sess):
    return "user" in sess
