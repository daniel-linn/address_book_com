from functools import wraps
from flask import session, redirect, render_template, url_for
from app.models import Users_role, Users_information

def role(user_id):
    user = Users_role.query.filter_by(user_id=user_id).first()
    return user.role

def validate(user_id):
    user = Users_role.query.filter_by(user_id=user_id).first()
    return user.is_hidden

def check_inform(user_id):
    user = Users_information.query.filter_by(user_id=user_id).first()
    return user.realname

# Apology function was provided by CS50 staff
def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = role(session.get('user_id'))
        if user_role != 'admin':
            return apology("Admin rights required")
        return f(*args, **kwargs)
    return decorated_function

def validate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if validate(session['user_id']) == 1:
            return apology("Wait for validating or contact admin")
        return f(*args, **kwargs)
    return decorated_function