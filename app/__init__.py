from pathlib import Path

from flask import Flask

from .config import Config
from .extensions import db, login_manager


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Make sure the instance folder (holds the SQLite file) exists.
    Path(app.root_path).parent.joinpath('instance').mkdir(exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

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
