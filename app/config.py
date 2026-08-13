import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Central app configuration, read from environment variables (see
    .env.example). Values here are safe local-dev defaults — override
    every one of them for anything beyond your own machine.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{BASE_DIR / 'instance' / 'agrivision.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # STAGE 4 — your Groq API key: https://console.groq.com/keys
    GROQ_API_KEY = os.environ.get('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', '')

    # STAGE 5 — only needed if your market-price source requires a key
    MARKET_PRICE_API_KEY = os.environ.get('MARKET_PRICE_API_KEY', '')

    # STAGE 3 — where captured/uploaded plant photos are saved
    UPLOAD_FOLDER = str(BASE_DIR / 'app' / 'static' / 'uploads')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB, generous for a photo
