import base64
import os
import uuid
from flask import (
    Blueprint,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user

from ..extensions import db
from ..models.scan import ScanHistory
from ..services.market_price_service import get_price_for_crop
from ..services.vision_service import identify_plant

camera_bp = Blueprint('camera', __name__, url_prefix='/camera')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def _allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@camera_bp.route('/')
def index():
    """Renders the camera capture and image upload page."""
    return render_template('main/camera.html')


@camera_bp.route('/upload', methods=['POST'])
def upload():
    """Receives an uploaded photo (from file input or camera capture canvas),
    runs plant identification and Nepal market pricing, and saves to ScanHistory.
    """
    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    os.makedirs(upload_folder, exist_ok=True)

    filename = None
    saved_path = None

    # Case 1: JSON payload with base64 data URI (camera snap)
    if request.is_json and request.json.get('image_data'):
        data_uri = request.json['image_data']
        try:
            header, encoded = data_uri.split(',', 1)
            ext = 'jpg'
            if 'png' in header:
                ext = 'png'
            elif 'webp' in header:
                ext = 'webp'

            file_bytes = base64.b64decode(encoded)
            filename = f"scan_{uuid.uuid4().hex[:12]}.{ext}"
            saved_path = os.path.join(upload_folder, filename)
            with open(saved_path, 'wb') as f:
                f.write(file_bytes)
        except Exception as e:
            return jsonify({'success': False, 'error': f'Failed to decode camera capture: {e}'}), 400

    # Case 2: Multipart form file upload
    elif 'image' in request.files and request.files['image'].filename:
        file = request.files['image']
        if not _allowed_file(file.filename):
            error_msg = 'Please upload a valid image (PNG, JPG, JPEG, WEBP).'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'error': error_msg}), 400
            return render_template('main/camera.html', error=error_msg), 400

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"scan_{uuid.uuid4().hex[:12]}.{ext}"
        saved_path = os.path.join(upload_folder, filename)
        file.save(saved_path)

    # Case 3: Form-encoded base64 fallback
    elif request.form.get('image_data'):
        data_uri = request.form['image_data']
        try:
            _, encoded = data_uri.split(',', 1)
            file_bytes = base64.b64decode(encoded)
            filename = f"scan_{uuid.uuid4().hex[:12]}.jpg"
            saved_path = os.path.join(upload_folder, filename)
            with open(saved_path, 'wb') as f:
                f.write(file_bytes)
        except Exception as e:
            error_msg = f'Failed to process image: {e}'
            return render_template('main/camera.html', error=error_msg), 400

    else:
        error_msg = 'No image provided. Please take a photo or select an image file.'
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': error_msg}), 400
        return render_template('main/camera.html', error=error_msg), 400

    # Perform multimodal botanical and agronomic identification
    try:
        vision_result = identify_plant(saved_path)
    except Exception as e:
        current_app.logger.error(f'Identification error: {e}')
        error_msg = 'Could not analyze this photo. Please try again with a clearer picture.'
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': error_msg}), 500
        return render_template('main/camera.html', error=error_msg), 500

    # Look up Nepal benchmark market price
    crop_keyword = vision_result.get('crop_keyword') or vision_result.get('common_name')
    market_result = get_price_for_crop(crop_keyword)

    # Store scan record in database
    relative_img_path = f"uploads/{filename}"
    scan = ScanHistory(
        user_id=current_user.id if current_user.is_authenticated else None,
        image_path=relative_img_path,
        common_name=vision_result.get('common_name'),
        common_name_ne=vision_result.get('common_name_ne'),
        scientific_name=vision_result.get('scientific_name'),
        family=vision_result.get('family'),
        confidence=vision_result.get('confidence'),
        description=vision_result.get('description'),
        description_ne=vision_result.get('description_ne'),
        growing_tips=vision_result.get('growing_tips'),
        growing_tips_ne=vision_result.get('growing_tips_ne'),
        planting_season=vision_result.get('planting_season'),
        planting_season_ne=vision_result.get('planting_season_ne'),
        growth_duration=vision_result.get('growth_duration'),
        growth_duration_ne=vision_result.get('growth_duration_ne'),
        fertilizer_guide=vision_result.get('fertilizer_guide'),
        fertilizer_guide_ne=vision_result.get('fertilizer_guide_ne'),
        optimal_climate=vision_result.get('optimal_climate'),
        optimal_climate_ne=vision_result.get('optimal_climate_ne'),
        unfavorable_climate=vision_result.get('unfavorable_climate'),
        unfavorable_climate_ne=vision_result.get('unfavorable_climate_ne'),
        profitability_window=vision_result.get('profitability_window'),
        profitability_window_ne=vision_result.get('profitability_window_ne'),
        ai_provider=vision_result.get('ai_provider'),
        market_crop_name=market_result.get('crop_name') if market_result else None,
        market_min_price=market_result.get('min_price') if market_result else None,
        market_max_price=market_result.get('max_price') if market_result else None,
        market_avg_price=market_result.get('avg_price') if market_result else None,
        market_unit=market_result.get('unit') if market_result else None,
        market_name=market_result.get('market') if market_result else None,
    )

    try:
        db.session.add(scan)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Database error saving scan: {e}')
        error_msg = 'Failed to save crop record. Please try again.'
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': error_msg}), 500
        return render_template('main/camera.html', error=error_msg), 500

    redirect_url = url_for('results.view_scan', scan_id=scan.id)

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'redirect_url': redirect_url,
            'scan_id': scan.id,
        })

    return redirect(redirect_url)
