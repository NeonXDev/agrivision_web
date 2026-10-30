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
        'sqlite:///agrivision.db',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Gemini AI: https://aistudio.google.com/app/apikey
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', os.environ.get('GOOGLE_API_KEY', ''))
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash-lite')

    # Fallback Vision Provider (Groq): https://console.groq.com/keys
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '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')

    # Nepal Market price API / source configuration
    MARKET_PRICE_API_KEY = os.environ.get('MARKET_PRICE_API_KEY', '')

    # Where captured/uploaded plant photos are saved
    UPLOAD_FOLDER = str(BASE_DIR / 'app' / 'static' / 'uploads')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
