import os
import sys
from pathlib import Path

# Set serverless flags before any application imports
os.environ.setdefault('VERCEL', '1')
os.environ.setdefault('FLASK_SKIP_DOTENV', '1')

# Ensure the root directory is on the Python module search path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import create_app

app = create_app()
