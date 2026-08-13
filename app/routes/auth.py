from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    """STAGE 2 adds the real form: POST handler, Flask-WTF form + CSRF,
    password check, login_user()."""
    return render_template('auth/login.html')


@auth_bp.route('/signup')
def signup():
    """STAGE 2 adds the real form: POST handler, Flask-WTF form + CSRF,
    User.set_password(), db.session.add/commit."""
    return render_template('auth/signup.html')
