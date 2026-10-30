import os
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlencode

# Set serverless flags before any application imports
os.environ.setdefault('VERCEL', '1')
os.environ.setdefault('FLASK_SKIP_DOTENV', '1')

# Ensure the root directory is on the Python module search path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import create_app

flask_app = create_app()


def app(environ, start_response):
    # Restore the original request path from rewritten query parameter if present
    qs = environ.get('QUERY_STRING', '')
    if '__path=' in qs:
        params = parse_qs(qs, keep_blank_values=True)
        raw_path = params.pop('__path', ['/'])[0]
        if not raw_path.startswith('/'):
            raw_path = '/' + raw_path
        environ['PATH_INFO'] = raw_path
        environ['QUERY_STRING'] = urlencode(
            [(k, v) for k, vs in params.items() for v in vs]
        )
    elif environ.get('PATH_INFO', '').startswith('/api/index'):
        rest = environ['PATH_INFO'][len('/api/index'):]
        environ['PATH_INFO'] = rest if rest.startswith('/') else ('/' + rest)

    return flask_app(environ, start_response)
