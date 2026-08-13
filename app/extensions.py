"""Extension instances live here, separate from both app/__init__.py and
the models that use them — the standard fix for the circular-import knot
that app-factory-pattern Flask projects otherwise run into.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please sign in to continue.'
login_manager.login_message_category = 'info'
