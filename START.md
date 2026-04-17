# SmartScreen - Start Guide

## Prerequisites
- Python 3.10+ installed
- Node.js 16+ installed
- PostgreSQL/Neon database configured in `.env`

## 1. Setup Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Start the backend server (from project root)
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 2. Setup Frontend

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the frontend development server
npm start
```

Frontend will be available at: `http://localhost:3000`

## 3. Access Admin Panel

After both servers are running:

1. **Admin Login:** `http://localhost:3000/admin-login`
2. **Admin Dashboard:** `http://localhost:3000/admin-dashboard`
3. **Admin Management:** `http://localhost:3000/admin-management`

### Admin Credentials (Created)
- **Email:** rishigupta9711@gmail.com
- **Password:** rishi@9711

## Project Structure

```
SmartScreen/
├── backend/              FastAPI application
│   ├── main.py          Entry point
│   ├── routes/          API endpoints
│   ├── models/          Database models
│   ├── services/        Business logic
│   └── schemas/         Request/response schemas
│
├── frontend/            React application
│   └── src/
│       ├── components/  React components
│       └── services/    API client
│
├── docs/                Documentation
├── scripts/             Utility and setup scripts
├── tests/               Test files and results
├── config/              Configuration files
│
├── .env                 Environment variables (gitignored)
├── requirements.txt     Python dependencies
└── package.json         Node.js dependencies
```

## Common Commands

### Backend
```bash
# Run tests
python scripts/test_admin_endpoints.py

# Create admin account interactively
python scripts/create_admin_seed.py

# Check database configuration
python scripts/check_db_urls.py
```

### Frontend
```bash
# Build for production
npm run build

# Run tests
npm test
```

## Environment Variables (.env)

```
DATABASE_URL=postgresql://...
API_KEY=...
JWT_SECRET=...
ENVIRONMENT=production
```

See `.env.example` in config/ folder for all available variables.

## Documentation

- [Admin Panel Guide](docs/ADMIN_PANEL_GUIDE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Backend Setup](docs/BACKEND_SETUP.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)

## Troubleshooting

### Backend not starting?
```bash
# Check Python dependencies
pip install -r requirements.txt

# Clear cache and restart
rm -rf backend/__pycache__
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend not connecting?
```bash
# Clear node_modules and reinstall
rm -rf frontend/node_modules
cd frontend && npm install
npm start
```

### Database connection issues?
```bash
# Check database URL configuration
python scripts/check_db_urls.py

# Verify admin exists
python scripts/check_admin.py
```
