from flask import Blueprint, render_template

results_bp = Blueprint('results', __name__, url_prefix='/results')


@results_bp.route('/')
def index():
    """STAGE 4 builds the real layout (name, scientific name, confidence,
    growing tips) once vision_service.identify_plant() is implemented.
    STAGE 5 adds the market-price section."""
    return render_template('main/results.html')
