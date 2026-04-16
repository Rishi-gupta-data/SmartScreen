# SmartScreen Project Structure

## 📁 Directory Layout (ORGANIZED)

```
SmartScreen/
│
├── 📱 FRONTEND APPLICATION
│   └── frontend/
│       ├── src/
│       │   ├── components/        React components
│       │   ├── services/          API integration
│       │   ├── App.js
│       │   └── index.js
│       ├── package.json           Frontend dependencies
│       └── public/
│
├── 🔌 BACKEND APPLICATION  
│   └── backend/
│       ├── main.py               Entry point
│       ├── config.py             Configuration
│       ├── db/
│       │   └── connection.py      Database connection
│       ├── models/               SQLAlchemy models
│       │   ├── user.py
│       │   ├── transaction.py
│       │   └── usage.py
│       ├── routes/               API endpoints
│       │   ├── admin.py          Admin management API
│       │   ├── auth.py           Authentication
│       │   ├── billing.py
│       │   ├── credit.py
│       │   ├── resume.py
│       │   ├── jd.py
│       │   └── match.py
│       ├── schemas/              Request/response schemas
│       │   ├── admin_schema.py
│       │   ├── user_schema.py
│       │   └── request_schema.py
│       ├── services/             Business logic
│       │   ├── admin.py          Admin service
│       │   ├── auth.py           Authentication service
│       │   └── parsing_service.py
│       ├── utils/
│       │   └── deps.py           Dependency injection
│       └── tests/                Unit tests
│
├── 📚 DOCUMENTATION (organized)
│   └── docs/
│       ├── README.md                 Main documentation
│       ├── QUICK_START.md            Quick setup guide
│       ├── ADMIN_PANEL_GUIDE.md      Admin features
│       ├── API_DOCUMENTATION.md      API reference
│       ├── BACKEND_SETUP.md          Backend setup
│       ├── DEPLOYMENT_GUIDE.md       Production deployment
│       └── [20+ more docs]
│
├── 🛠️ SCRIPTS & UTILITIES
│   └── scripts/
│       ├── create_admin_seed.py      Create initial admin
│       ├── test_admin_endpoints.py   API endpoint tests
│       ├── check_admin.py            Admin verification
│       ├── check_db_urls.py          DB configuration check
│       ├── diagnose_backend.py       Backend diagnostics
│       └── [7+ more scripts]
│
├── 🧪 TESTS
│   └── tests/
│       └── [test output files]
│
├── ⚙️ CONFIGURATION
│   └── config/
│       ├── Procfile                  Deployment config
│       └── skills.json               Skills configuration
│
├── 🌐 ROOT DIRECTORY (clean)
│   ├── .env                          Environment variables
│   ├── requirements.txt              Python dependencies
│   ├── package.json                  Node.js dependencies
│   ├── START.md                      Startup guide
│   ├── start.py                      Startup script
│   ├── CLEANUP_SUMMARY.md            This cleanup summary
│   ├── LICENSE                       License
│   └── venv/                         Python virtual environment
│
└── 📦 OTHER
    ├── .git/                         Git repository
    ├── .gitignore                    Git ignore rules
    ├── .vscode/                      VS Code settings
    ├── .devcontainer/                Docker container config
    └── photos/                       Static resources
```

## 🚀 Quick Start

### Option 1: Using start.py
```bash
python start.py
```

### Option 2: Manual startup

**Terminal 1 - Backend:**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

## 📋 Key Locations

| Component | Location | Port |
|-----------|----------|------|
| Backend API | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | - |
| Frontend | http://localhost:3000 | 3000 |
| Admin Login | http://localhost:3000/admin-login | - |

## 🔑 Admin Credentials
```
Email:    rishigupta9711@gmail.com
Password: rishi@9711
```

## 📖 Documentation Index

### Getting Started
- [START.md](START.md) - This quick reference
- [docs/README.md](docs/README.md) - Complete documentation
- [docs/QUICK_START.md](docs/QUICK_START.md) - 5-minute setup

### Development
- [docs/ADMIN_PANEL_GUIDE.md](docs/ADMIN_PANEL_GUIDE.md) - Admin features
- [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - API reference
- [docs/BACKEND_SETUP.md](docs/BACKEND_SETUP.md) - Backend details

### Deployment
- [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) - Production setup
- [docs/PRODUCTION_STATUS.md](docs/PRODUCTION_STATUS.md) - Status report

### Architecture
- [docs/IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md) - Implementation details
- [docs/SRS.md](docs/SRS.md) - Requirements specification

## 🔧 Useful Scripts

```bash
# Create new admin account
python scripts/create_admin_seed.py

# Test all admin API endpoints
python scripts/test_admin_endpoints.py

# Check database configuration
python scripts/check_db_urls.py

# Verify admin in database
python scripts/check_admin.py

# Diagnose backend issues
python scripts/diagnose_backend.py
```

## ✅ Verification

**Backend running?**
```bash
curl http://localhost:8000/docs
```

**Frontend running?**
```bash
curl http://localhost:3000
```

**Admin panel accessible?**
- http://localhost:3000/admin-login
- http://localhost:3000/admin-dashboard
- http://localhost:3000/admin-management

## 🐛 Troubleshooting

### Module Import Error
**Problem:** `ModuleNotFoundError: No module named 'backend'`
**Solution:** Run from project root, not backend folder
```bash
# ✓ Correct
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# ✗ Wrong
cd backend
python -m uvicorn main:app --reload
```

### Database Connection Error
```bash
# Check database URL
python scripts/check_db_urls.py

# Verify admin exists
python scripts/check_admin.py
```

### Frontend Not Connecting
```bash
cd frontend
rm -rf node_modules
npm install
npm start
```

## 📞 Getting Help

1. Check documentation in `docs/`
2. Run diagnostic script: `python scripts/diagnose_backend.py`
3. Check API docs at: http://localhost:8000/docs
4. Review logs in the terminal

---

**Last Updated:** 2026-04-16  
**Status:** ✅ Production Ready  
**Backend:** ✅ Running  
**Frontend:** Ready to start  
**Tests:** ✅ All Passing (11/11)
