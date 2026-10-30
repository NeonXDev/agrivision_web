# AgroVision Nepal 🌱 (Python / Flask)

AI-powered plant identification and live Nepal market prices, built for farmers
and growers. Point a camera at a plant, get its name, scientific name, a
confidence score, current market price, and growing tips — in one scan.

**This project pivoted from a Flutter mobile app to a Python website.** The
Dart code doesn't carry over (different language, different runtime), so
this restarts the same six-stage build from Stage 1 — now in Flask. The
architecture and staging philosophy carry over even though the code doesn't:
clean separation of routes/models/services, and each stage leaves a
runnable, clickable app rather than half-finished code.

This is **Stage 1 of 6**: the scaffold. Every page routes correctly and dark
mode fully works; camera, identification, price lookup, and history are
stubbed behind clean interfaces until their stage lands.

## Tech stack

- **Flask** (app-factory pattern + blueprints) — chosen to match the Flask
  + Groq combination from your Azusa project
- **Flask-SQLAlchemy** — SQLite by default, one env var away from Postgres
- **Flask-Login** — session-based auth (Stage 2)
- **Flask-WTF** — CSRF-safe forms (Stage 2)
- **Groq** (official `groq` SDK) — vision-capable chat completions for
  plant ID (Stage 4). Confirmed this via their docs: the vision endpoint
  takes OpenAI-style `image_url` content blocks and supports JSON mode,
  which is what Stage 4 will lean on for structured output.
- Server-rendered Jinja2 templates + vanilla CSS/JS — no separate frontend
  build step

## Folder structure

```
agrovision_web/
├── run.py                    entry point (loads .env, creates the app)
├── requirements.txt
├── app/
│   ├── __init__.py            app factory — registers extensions + blueprints
│   ├── config.py              env-driven config (SECRET_KEY, DB URI, API keys)
│   ├── extensions.py          shared db / login_manager instances
│   ├── models/
│   │   ├── user.py             User (Flask-Login + password hashing)
│   │   └── scan.py             ScanHistory (photo + plant + price snapshot)
│   ├── routes/                 one blueprint per feature area
│   │   ├── auth.py              /login, /signup
│   │   ├── home.py              /
│   │   ├── camera.py            /camera        → Stage 3
│   │   ├── results.py           /results       → Stage 4/5
│   │   ├── history.py           /history       → Stage 6
│   │   └── settings.py          /settings      ✅ dark mode works now
│   ├── services/                one clean interface per external concern
│   │   ├── vision_service.py     identify_plant() → Stage 4 (Groq)
│   │   └── market_price_service.py get_price_for_crop() → Stage 5
│   ├── static/
│   │   ├── css/style.css        green theme, light + dark via CSS variables
│   │   ├── js/theme.js          dark-mode toggle + persistence
│   │   └── uploads/             captured/uploaded photos land here (Stage 3)
│   └── templates/
│       ├── base.html            nav, theme loading, shared layout
│       ├── _macros.html         reusable snippets (this stack's version of
│       │                        the old EmptyState / PrimaryButton widgets)
│       ├── auth/                login.html, signup.html
│       └── main/                home, camera, results, history, settings
└── instance/                   SQLite database lives here (gitignored)
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Generate a real key and paste it into .env as SECRET_KEY:
python -c "import secrets; print(secrets.token_hex(32))"

python run.py
```

Visit `http://127.0.0.1:5000`. You'll land on Home, and every nav link
(History, Settings, Sign in) works — Settings has a real, working dark-mode
toggle. "Continue to Home (dev)" on the sign-in page lets you click through
before real auth exists.

Every file compiles/parses cleanly — I ran `py_compile` on every `.py` file,
parsed every template through the real Jinja2 parser, and cross-checked
every `url_for()` call against the actual registered routes, all in this
sandbox. I can't run `pip install` here (no network), so `flask run` itself
is still worth trying on your machine as a final check.

## Build roadmap

- [x] **Stage 1 — Scaffold**: Flask app factory, blueprints, models, service interfaces, green theme + working dark mode, every page routes correctly
- [ ] **Stage 2 — Authentication**: real login/signup forms (Flask-WTF + CSRF), password hashing, `login_user()`/`logout_user()`, `@login_required` guarding camera/results/history
- [ ] **Stage 3 — Camera & upload**: browser camera capture (`getUserMedia`) + file-upload fallback, saved under `app/static/uploads/`
- [ ] **Stage 4 — Plant identification**: `vision_service.identify_plant()` via Groq, real results page (name, scientific name, confidence, growing tips)
- [ ] **Stage 5 — Market price integration**: `market_price_service.get_price_for_crop()`, price card added to results
- [ ] **Stage 6 — Scan history & polish**: `ScanHistory` rows actually saved/listed, remaining settings (account, sign out), empty/error states

## Where your API keys go

| Key | Where |
|---|---|
| `GROQ_API_KEY` | `.env` (read via `app/config.py`, used in `vision_service.py` from Stage 4) |
| `MARKET_PRICE_API_KEY` | `.env` (used in `market_price_service.py` from Stage 5) |
| `SECRET_KEY` | `.env` — required for sessions/CSRF; the app runs with an insecure placeholder if you skip it, so set a real one before anything but local testing |

`.env` is already gitignored.
