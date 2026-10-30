import os
from pathlib import Path

from flask import Flask, send_from_directory

from .config import Config
from .extensions import db, login_manager


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # In local environments, make sure instance/ directory exists for SQLite
    if not os.environ.get('VERCEL'):
        try:
            Path(app.root_path).parent.joinpath('instance').mkdir(exist_ok=True)
        except OSError:
            pass

    # Ensure upload folder exists
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)

    # Explicit route to serve user uploads seamlessly from UPLOAD_FOLDER (works both locally and on Vercel /tmp)
    @app.route('/static/uploads/<path:filename>')
    def serve_uploaded_file(filename: str):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    from .routes.camera import camera_bp
    from .routes.history import history_bp
    from .routes.home import home_bp
    from .routes.results import results_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(camera_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(history_bp)

    # Import models so SQLAlchemy knows about them before create_all().
    from . import models  # noqa: F401

    with app.app_context():
        db.create_all()

    return app
