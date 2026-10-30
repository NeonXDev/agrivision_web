import os
from flask import Blueprint, current_app, redirect, render_template, url_for
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
    """Deletes all recorded scans and cleans up saved image files from disk."""
    try:
        if current_user.is_authenticated:
            scans_to_delete = ScanHistory.query.filter_by(user_id=current_user.id).all()
        else:
            scans_to_delete = ScanHistory.query.all()

        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        if upload_folder and os.path.isdir(upload_folder):
            for scan in scans_to_delete:
                if scan.image_path:
                    filename = os.path.basename(scan.image_path)
                    file_path = os.path.join(upload_folder, filename)
                    if os.path.isfile(file_path):
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass

        if current_user.is_authenticated:
            ScanHistory.query.filter_by(user_id=current_user.id).delete()
        else:
            ScanHistory.query.delete()

        db.session.commit()
    except Exception as e:
        current_app.logger.error(f'Failed to clear history: {e}')
        db.session.rollback()

    return redirect(url_for('history.index'))
