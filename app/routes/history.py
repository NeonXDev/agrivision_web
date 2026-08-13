from flask import Blueprint, render_template

history_bp = Blueprint('history', __name__, url_prefix='/history')


@history_bp.route('/')
def index():
    """STAGE 6 connects this to the ScanHistory model, scoped to
    current_user."""
    return render_template('main/history.html')
