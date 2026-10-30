from flask import Blueprint, render_template
from ..models.scan import ScanHistory

results_bp = Blueprint('results', __name__, url_prefix='/results')


@results_bp.route('/')
def index():
    """Displays the most recent scan result, or prompt to scan if none exists."""
    latest_scan = ScanHistory.query.order_by(ScanHistory.scanned_at.desc()).first()
    return render_template('main/results.html', scan=latest_scan)


@results_bp.route('/<int:scan_id>')
def view_scan(scan_id: int):
    """Displays full details for a specific scan."""
    scan = ScanHistory.query.get_or_404(scan_id)
    return render_template('main/results.html', scan=scan)
