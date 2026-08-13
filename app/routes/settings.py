from flask import Blueprint, render_template

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/')
def index():
    """Dark mode is fully working (client-side, see static/js/theme.js).
    Account info and sign-out land in Stage 2 once auth is real."""
    return render_template('main/settings.html')
