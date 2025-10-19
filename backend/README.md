# Backend (Django + DRF)

Ports
- Backend server: 3001
- PostgreSQL: 5001

Setup
1) Copy .env.example to .env and adjust values if necessary.
2) Install dependencies:
   - pip install -r requirements.txt
3) Apply migrations and create an admin:
   - python manage.py migrate
   - python manage.py createsuperuser
4) Run server on port 3001:
   - python manage.py runserver 0.0.0.0:3001

Environment variables
- SECRET_KEY, DEBUG, ALLOWED_HOSTS
- POSTGRES_HOST=localhost, POSTGRES_PORT=5001, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
  or POSTGRES_URL=postgresql://user:pass@host:5001/dbname
- CORS_ALLOW_ALL_ORIGINS=true (or set CORS_ALLOWED_ORIGINS)

Health
- GET /api/health -> {"message": "Server is up!"}

Docs
- Swagger UI: /api/docs/
- Redoc: /api/redoc/
