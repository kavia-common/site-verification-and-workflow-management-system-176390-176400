# site-verification-and-workflow-management-system-176390-176400

Full-stack quick start (PostgreSQL + Django backend + Flutter frontend)

Preview/dev ports (consistent across containers):
- PostgreSQL: 5001
- Backend (Django): 3001
- Flutter frontend: 3000

1) Database (PostgreSQL)
- Ensure a PostgreSQL instance is available on port 5001.
- Connection example: host=localhost port=5001 dbname=myapp user=appuser password=dbuser123
- For the database container, ensure postgresql_database/db_connection.txt points to port 5001.

2) Backend (Django + DRF)
- Copy backend/.env.example to backend/.env and adjust if needed.
- From backend/: pip install -r requirements.txt
- Migrations and admin:
  - python manage.py migrate
  - python manage.py createsuperuser
- Run server on preview port 3001:
  - python manage.py runserver 0.0.0.0:3001

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
- ALLOWED_HOSTS: comma-separated hosts (use * for previews).
- POSTGRES_HOST=localhost
- POSTGRES_PORT=5001
- POSTGRES_DB=myapp
- POSTGRES_USER=appuser
- POSTGRES_PASSWORD=dbuser123
  or POSTGRES_URL=postgresql://user:pass@host:5001/dbname
- CORS_ALLOW_ALL_ORIGINS=true (or set CORS_ALLOWED_ORIGINS with http://localhost:3000)

Notes
- If DB env vars are not set, the backend falls back to SQLite for local dev.
- For previews/CI, set POSTGRES_* envs to use the shared PostgreSQL on port 5001.

3) Flutter Frontend
- Ensure flutter_frontend/.env contains:
  - BACKEND_BASE_URL=http://localhost:3001
- Start the Flutter app targeting port 3000 for web preview (if applicable).
- The dashboard performs a connectivity check to GET /api/health on init and displays status.