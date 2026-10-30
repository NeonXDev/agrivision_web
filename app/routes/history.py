from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from ..extensions import db
from ..models.scan import ScanHistory

history_bp = Blueprint('history', __name__, url_prefix='/history')


@history_bp.route('/')
def index():
    """Displays user scan history or all recent scans."""
    if current_user.is_authenticated:
        scans = (
            ScanHistory.query.filter_by(user_id=current_user.id)
            .order_by(ScanHistory.scanned_at.desc())
            .all()
        )
    else:
        scans = ScanHistory.query.order_by(ScanHistory.scanned_at.desc()).all()

    return render_template('main/history.html', scans=scans)


@history_bp.route('/clear', methods=['POST'])
def clear():
    """Deletes all recorded scans."""
    try:
        if current_user.is_authenticated:
            ScanHistory.query.filter_by(user_id=current_user.id).delete()
        else:
            ScanHistory.query.delete()
        db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for('history.index'))
