from flask import Blueprint, render_template

camera_bp = Blueprint('camera', __name__, url_prefix='/camera')


@camera_bp.route('/')
def index():
    """STAGE 3 replaces this placeholder with the live browser-camera
    (getUserMedia) capture flow plus a file-upload fallback, POSTing the
    photo to a route that saves it under UPLOAD_FOLDER."""
    return render_template('main/camera.html')
