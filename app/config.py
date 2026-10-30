import os
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Central app configuration read from environment variables (.env).
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'agrivision-nepal-local-secret-key')

    # Database configuration
    _db_url = os.environ.get('DATABASE_URL')
    if os.environ.get('VERCEL'):
        if _db_url and not _db_url.startswith('sqlite:'):
            if _db_url.startswith('postgres://'):
                _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
            SQLALCHEMY_DATABASE_URI = _db_url
        else:
            # On Vercel serverless, SQLite must live in /tmp ephemeral storage
            _temp_db = os.path.join(tempfile.gettempdir(), 'agrivision.db').replace('\\', '/')
            SQLALCHEMY_DATABASE_URI = f'sqlite:///{_temp_db}'
    else:
        if _db_url:
            if _db_url.startswith('postgres://'):
                _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
            SQLALCHEMY_DATABASE_URI = _db_url
        else:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///agrivision.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Gemini AI: https://aistudio.google.com/app/apikey
    GEMINI_API_KEY = (
        os.environ.get('GEMINI_API_KEY')
        or os.environ.get('GOOGLE_API_KEY')
        or ''
    )
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')

    # Fallback Vision Provider (Groq): https://console.groq.com/keys
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

    # Where captured/uploaded plant photos are saved
    if os.environ.get('VERCEL'):
        UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'uploads')
    else:
        UPLOAD_FOLDER = str(BASE_DIR / 'app' / 'static' / 'uploads')

    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
