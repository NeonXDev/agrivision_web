import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Central app configuration read from environment variables (.env).
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'agrivision-nepal-local-secret-key')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///agrivision.db',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Gemini AI: https://aistudio.google.com/app/apikey
    GEMINI_API_KEY = (
        os.environ.get('GEMINI_API_KEY')
        or os.environ.get('GOOGLE_API_KEY')
        or ''
    )
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash-lite')

    # Fallback Vision Provider (Groq): https://console.groq.com/keys
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

    # Where captured/uploaded plant photos are saved
    UPLOAD_FOLDER = str(BASE_DIR / 'app' / 'static' / 'uploads')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
