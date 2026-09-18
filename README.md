daphne -b 127.0.0.1 -p 8000 config.asgi:application
# SkillSwap Platform

SkillSwap is a full-stack skill exchange platform. People discover reciprocal learning partners through bidirectional skill matching, schedule sessions, leave peer reviews, and chat in real time.

## Architecture

- `backend/`: Django 5, Django REST Framework, SQLite for local development, and Channels/Daphne for WebSockets.
- `backend/swaps/`: profiles, matching, sessions, messages, reviews, API views, and the chat consumer.
- `frontend/`: React, TypeScript, Vite, and Tailwind/PostCSS tooling.
- REST API base URL: `http://localhost:8000/api`.
- WebSocket chat URL: `ws://localhost:8000/ws/chat/<user_id>/`.

The matcher uses Sentence Transformers when available and falls back to TF-IDF for lightweight local development. The local channel layer is in-memory; use a Redis channel layer for multi-process production deployments.

## Requirements

- Python 3.11+
- Node.js 20+
- npm

## Backend setup

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8000
```

For WebSocket support, run Daphne instead of Django's development server:

```powershell
daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

The development database is `backend/db.sqlite3` and is intentionally ignored by Git. Demo credentials are `maya` / `demo1234` after seeding.

## Frontend setup

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Set `VITE_API_URL` when the API is hosted somewhere other than `http://localhost:8000/api`.

Create a production build with:

```powershell
npm run build
```

## API endpoints

All endpoints below require token authentication unless noted otherwise.

- `POST /api/auth/signup/` and `POST /api/auth/login/`: account creation and login.
- `GET /api/profile/me/`: current profile.
- `GET /api/matches/`: ranked reciprocal matches.
- `GET /api/matches/<user_id>/`: one ranked match and its score.
- `GET|POST /api/sessions/`: list or request sessions.
- `GET|PUT /api/sessions/<id>/`: inspect or update a session.
- `POST /api/reviews/`: review a completed session.
- `GET /api/messages/?peer=<user_id>`: retrieve a conversation.
- `ws://localhost:8000/ws/chat/<user_id>/`: authenticated real-time chat.

## Verification

From the repository root:

```powershell
cd backend
python manage.py check
python manage.py test
cd ..\frontend
npm run build
```

The Django admin is available at `http://localhost:8000/admin/`; `Profile`, `Session`, `Message`, and `Review` are registered in the admin site.
