# 🎓 SmartScreen SaaS

**Smart Resume & Job Description Matching Platform for Training & Placement Cells**

> A production-ready SaaS platform that intelligently matches resumes with job descriptions using regex-based parsing (HF models coming soon). No external LLM APIs - fully self-hosted.

---

## 🚀 Quick Start

### Backend (FastAPI)
```bash
cd backend
pip install -r ../requirements.txt
export PYTHONPATH=.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API Available at:** http://localhost:8000/docs

### Frontend (React)
```bash
cd frontend
npm install
REACT_APP_API_URL=http://localhost:8000 npm start
```

**Frontend Available at:** http://localhost:3000

---

## 📋 Overview

SmartScreen is a **credit-based SaaS platform** that:
- ✅ **Parses resumes** - Extracts skills, experience, education, contact info
- ✅ **Parses job descriptions** - Identifies requirements, qualifications, responsibilities
- ✅ **Matches candidates** - Calculates compatibility scores & recommendations
- ✅ **Manages billing** - Credit system: parse (5 cr), JD (3 cr), match (5 cr)
- ✅ **Authenticates users** - JWT-based authentication with password hashing
- ✅ **Logs transactions** - Full audit trail in database

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     React Frontend (Port 3000)                  │
│              (HomePage, Dashboard, Upload, Results)             │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/JSONs with JWT
┌──────────────────────────┴──────────────────────────────────────┐
│                     FastAPI Backend (Port 8000)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Auth Routes       Resume Routes    Billing Routes       │   │
│  │  • Signup          • Parse Resume   • Get Credits        │   │
│  │  • Login           • Get Balance    • Buy Credits        │   │
│  │                                     • Transactions       │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Services Layer                                          │   │
│  │  • Auth (JWT, hashing)                                  │   │
│  │  • Credit System (add, deduct, balance)                 │   │
│  │  • Parsing Service (regex-based, HF-ready)             │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ SQLAlchemy ORM
┌──────────────────────────┴──────────────────────────────────────┐
│  Database Layer (SQLite Dev / PostgreSQL Prod)                 │
│  • Users (id, email, password, credits)                        │
│  • Transactions (id, user_id, type, amount)                    │
│  • Usage Logs (id, user_id, action, credits_used)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Core Features

### 1. Authentication System
- **Signup**: Register with email + password
- **Login**: Get JWT token (24-hour expiry)
- **Password Hashing**: Argon2 for security
- **Role-Based Access**: User and admin roles

### 2. Resume Parsing
Extracts from resume text:
- **Personal**: Name, email, phone
- **Skills**: Python, FastAPI, PostgreSQL, AWS, etc.
- **Experience**: Company, role, duration
- **Education**: Degree, institution, field

### 3. JD Parsing
Extracts from job description:
- **Position**: Title, company
- **Requirements**: Required skills, years of experience
- **Preferences**: Nice-to-have skills
- **Details**: Salary, qualifications, responsibilities

### 4. Smart Matching
Compares resume vs JD:
- **Match Score**: 0-100 based on skill overlap
- **Skill Breakdown**: Required matched vs missing
- **Recommendations**: "Excellent Match", "Good Match", etc.
- **Gaps Analysis**: Shows which skills are missing

### 5. Credit System
- **Pricing**: Resume (5), JD (3), Match (5) credits
- **Purchase**: Buy credits anytime
- **Deduction**: Automatic on operation completion
- **Audit Trail**: All transactions logged

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    credits INTEGER,
    role VARCHAR,
    created_at TIMESTAMP
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR,
    type VARCHAR,  -- 'add' or 'deduct'
    amount INTEGER,
    description VARCHAR,
    created_at TIMESTAMP
);
```

### Usage Logs Table
```sql
CREATE TABLE usage_logs (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR,
    action VARCHAR,  -- 'parse_resume', 'parse_jd', 'match'
    credits_used INTEGER,
    details JSON,
    created_at TIMESTAMP
);
```

---

## 🔗 API Endpoints

### Authentication
```
POST   /auth/signup              - Register new user
POST   /auth/login               - Get access token
```

### Resume Operations
```
POST   /resume/parse             - Parse resume (5 credits)
```

### JD Operations
```
POST   /jd/parse                 - Parse job description (3 credits)
```

### Matching
```
POST   /match/                   - Match resume to JD (5 credits)
```

### Billing
```
GET    /billing/credits          - Get credit balance
POST   /billing/buy-credits      - Purchase credits
GET    /billing/transactions     - Get transaction history
```

**Full API Documentation**: http://localhost:8000/docs (when running)

---

## 💾 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React, Axios | Web UI |
| **Backend** | FastAPI, Uvicorn | REST API |
| **Database** | SQLAlchemy + PostgreSQL/SQLite | Data persistence |
| **Auth** | JWT, Argon2, python-jose | Security |
| **Parsing** | Regex patterns | Extract data from text |

---

## 📦 Project Structure

```
SmartScreen/
├── backend/
│   ├── main.py              # FastAPI app entry
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── resume.py        # Resume parsing
│   │   ├── jd.py            # JD parsing
│   │   ├── match.py         # Matching logic
│   │   └── billing.py       # Credit operations
│   ├── services/            # Business logic
│   │   ├── auth.py          # Auth service
│   │   ├── credit_service.py # Credit logic
│   │   └── parsing_service.py # Parse functionality
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── transaction.py
│   │   └── usage.py
│   ├── schemas/             # Pydantic schemas
│   ├── db/                  # Database config
│   └── utils/               # Utilities
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API calls
│   │   └── App.js
│   └── package.json
│
├── requirements.txt         # Python dependencies
├── BACKEND_SETUP.md        # Backend setup guide
├── API_DOCUMENTATION.md    # Full API docs
└── README.md              # This file
```

---

## 🚦 Running Locally

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL (optional, SQLite for dev)

### Step 1: Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env if needed

# Run backend
cd backend
export PYTHONPATH=.
uvicorn main:app --reload
```

### Step 2: Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm start
```

### Step 3: Test
1. Open http://localhost:3000
2. Sign up with email/password
3. Buy credits
4. Parse resume/JD
5. Test matching

---

## 📚 Documentation

- **[Backend Setup Guide](BACKEND_SETUP.md)** - Detailed backend configuration
- **[API Documentation](API_DOCUMENTATION.md)** - Complete endpoint reference
- **[Development Plan](plan.md)** - Full project roadmap

---

## 🔮 Future Roadmap

### Phase 2: LLM Integration
- Integrate Hugging Face transformers
- Replace regex parsing with BERT/DistilBERT models
- Better skill extraction and matching

### Phase 3: Advanced Features
- Bulk candidate upload and matching
- Match analytics dashboard
- Resume recommendations (how to improve score)
- Integration with Razorpay/Stripe

### Phase 4: Scaling
- Rate limiting and caching (Redis)
- Background jobs (Celery)
- Multi-region deployment
- Advanced monitoring

---

## 🔐 Security Features

✅ **JWT Authentication** - Secure token-based auth  
✅ **Password Hashing** - Argon2 for strong hashing  
✅ **SQL Injection Protection** - SQLAlchemy ORM  
✅ **CORS Configuration** - Restricted origins  
✅ **Input Validation** - Pydantic schemas  
✅ **Transaction Logging** - Audit trail for billing  

---

## 📊 Pricing Model

| Operation | Cost |
|-----------|------|
| Parse Resume | 5 credits |
| Parse JD | 3 credits |
| Match Resume to JD | 5 credits |

**Base Plan**: ₹5,000/month + usage

---

## 🐛 Troubleshooting

### "Database connection refused"
```bash
# For PostgreSQL, ensure it's running
# For SQLite, it creates automatically
```

### "CORS error"
```bash
# Check CORS_ORIGINS in .env
# Add your frontend URL
```

### "Insufficient credits"
```bash
# Buy credits first via /billing/buy-credits
```

---

## 📞 Support & Questions

Refer to:
- API Docs: http://localhost:8000/docs
- Backend Guide: `BACKEND_SETUP.md`
- Full API Reference: `API_DOCUMENTATION.md`

---

## 📄 License

This project is part of SmartScreen SaaS platform.

---

**Built with ❤️ for Training & Placement Cells**
