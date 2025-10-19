# site-verification-and-workflow-management-system-176390-176400

Backend (Django + DRF) quick start

1) Setup environment
- Copy backend/.env.example to backend/.env and fill values (SECRET_KEY, DB connection).
- Ensure PostgreSQL is reachable (default port 5001 per project plan).

2) Install dependencies
- From backend/: pip install -r requirements.txt

3) Migrate and create admin
- python manage.py migrate
- python manage.py createsuperuser

4) Run server
- python manage.py runserver 0.0.0.0:8000

API and Auth
- JWT login: POST /api/auth/login/ with { "username": "", "password": "" }
- JWT refresh: POST /api/auth/refresh/ with { "refresh": "" }
- Health: GET /api/health/
- Core endpoints (auth required):
  - /api/sites/
  - /api/verifications/
  - /api/workflow-steps/
  - Custom actions:
    - POST /api/sites/{id}/verify/
    - GET /api/sites/{id}/workflow-steps/
    - POST /api/workflow-steps/{id}/complete/

Docs
- Swagger UI: /api/docs/
- Redoc: /api/redoc/

Environment variables (backend/.env)
- SECRET_KEY: Django secret.
- DEBUG: True/False.
- ALLOWED_HOSTS: comma-separated hosts.
- POSTGRES_HOST, POSTGRES_PORT=5001, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
  or POSTGRES_URL=postgresql://user:pass@host:5001/dbname
- CORS_ALLOW_ALL_ORIGINS (default True) or CORS_ALLOWED_ORIGINS (e.g., http://localhost:3000)

Notes
- If DB env vars are not set, the backend falls back to SQLite for local dev.
- For previews/CI, set POSTGRES_* envs to use the shared PostgreSQL on port 5001.