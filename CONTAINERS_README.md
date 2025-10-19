# Multi-container integration guide

Preview/dev ports:
- PostgreSQL: 5001
- Backend (Django): 3001
- Flutter frontend (web preview): 3000

Database
- Location: site-verification-and-workflow-management-system-176390-176399/postgresql_database
- Ensure db_connection.txt uses port 5001.
- Example DSN: postgresql://appuser:dbuser123@localhost:5001/myapp

Backend
- Location: site-verification-and-workflow-management-system-176390-176400/backend
- Copy backend/.env.example to backend/.env
- Run: python manage.py runserver 0.0.0.0:3001

Flutter frontend
- Location: site-verification-and-workflow-management-system-176390-176401/flutter_frontend
- Copy .env.example to .env with BACKEND_BASE_URL=http://localhost:3001
- For web preview: flutter run -d chrome --web-port 3000

Connectivity
- Frontend performs a connectivity check to GET /api/health when the dashboard loads and displays the result.
