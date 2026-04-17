# SmartScreen Backend Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (for production) or SQLite (for development)
- pip or poetry

### Installation

1. **Clone and Navigate**
```bash
cd SmartScreen
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize Database**
```bash
export PYTHONPATH=.
python backend/db/connection.py
# Tables will be created on first app startup
```

6. **Run Backend**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

---

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── app.py                  # Legacy Flask app (to be deprecated)
│
├── db/
│   └── connection.py       # Database configuration
│
├── models/
│   ├── user.py            # User model
│   ├── transaction.py      # Credit transactions
│   └── usage.py           # Usage logs
│
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Authentication endpoints
│   ├── resume.py          # Resume parsing
│   ├── jd.py              # Job description parsing
│   ├── match.py           # Resume-JD matching
│   ├── credit.py          # Admin credit operations
│   └── billing.py         # User billing endpoints
│
├── schemas/
│   ├── user_schema.py     # User/auth schemas
│   ├── parsing_schema.py  # Resume/JD schemas
│   └── request_schema.py  # API request/response schemas
│
├── services/
│   ├── auth.py            # Authentication logic
│   ├── credit_service.py  # Credit system logic
│   ├── parsing_service.py # Resume/JD parsing (regex-based)
│   └── llm_service.py     # Placeholder for HF models
│
└── utils/
    └── deps.py            # JWT dependency injection
```

---

## 🗄️ Database Configuration

### Development (SQLite)
No setup needed! SQLite database is created automatically.

```python
DATABASE_URL=sqlite:///./smartscreen.db
```

### Production (PostgreSQL)

#### Via Neon (Recommended)
1. Create account at https://console.neon.tech
2. Create a database
3. Copy connection string
4. Update .env:
```
DATABASE_URL=postgresql://user:password@host:5432/smartscreen?sslmode=require
```

#### Via Local PostgreSQL
```bash
createdb smartscreen
```

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/smartscreen
```

---

## 🔐 Security Setup

### Generate Secret Key
```python
import secrets
print(secrets.token_urlsafe(32))
```

Add to `.env`:
```
SECRET_KEY=your-generated-secret-key
```

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    credits INTEGER DEFAULT 0,
    role VARCHAR DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    type VARCHAR NOT NULL,  -- 'add' or 'deduct'
    amount INTEGER NOT NULL,
    description VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Usage Logs Table
```sql
CREATE TABLE usage_logs (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    action VARCHAR NOT NULL,  -- 'parse_resume', 'parse_jd', 'match'
    credits_used INTEGER NOT NULL,
    details JSON,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🧪 Testing

### Run Tests
```bash
pytest
```

### Test an Endpoint
```bash
# Sign up
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Parse a resume
TOKEN="your_access_token"
curl -X POST http://localhost:8000/resume/parse \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"John Doe\nSkills: Python, FastAPI"}'
```

---

## 🚀 Deployment

### Via Render
1. Connect GitHub repo
2. Set environment variables
3. Deploy main.py

### Via Railway
```bash
railway link
railway up
```

### Via Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📝 Credit System Logic

### Costs
| Operation | Credits |
|-----------|---------|
| Parse Resume | 5 |
| Parse JD | 3 |
| Match Resume to JD | 5 |

### Flow
1. **Check Balance**: User must have enough credits
2. **Process**: Execute operation (parse/match)
3. **Deduct**: Reduce credits from user account
4. **Log**: Record transaction for audit trail
5. **Return**: Send results + remaining balance

### Important
- Both `user.credits` and `transactions` table are maintained
- `transactions` table is the source of truth
- Credits are deducted AFTER successful operation
- Failed operations don't deduct credits

---

## 🔄 Development Workflow

### Making Changes
1. Edit code in respective modules
2. Tests run automatically (with `--reload`)
3. Check http://localhost:8000/docs for Swagger UI

### Creating New Endpoint
1. Create route in `/routes/`
2. Define schemas in `/schemas/`
3. Add service logic in `/services/`
4. Update `routes/__init__.py` with router export
5. Router automatically included in `main.py`

### Database Migrations (Future)
```bash
alembic init alembic
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

---

## 🔮 Future: Hugging Face Integration

When ready to add LLM:

1. Install transformers:
   ```bash
   pip install transformers torch
   ```

2. Create `llm_service.py`:
   ```python
   from transformers import pipeline
   
   class LLMService:
       def __init__(self):
           self.model = pipeline("feature-extraction", model="...")
       
       def extract_features(self, text):
           return self.model(text)
   ```

3. Update parsing_service.py to use LLM

---

## 🆘 Troubleshooting

### "Database connection refused"
- Check PostgreSQL is running
- Verify DATABASE_URL
- For SQLite, ensure write permissions

### "Invalid token"
- Token expired (24 hours default)
- Re-login to get new token

### "Insufficient credits"
- User needs to buy credits first
- Admin can add credits via `/credits/add`

### "CORS error"
- Check CORS_ORIGINS in .env
- Ensure frontend URL is in allowed origins

---

## 📞 Support

For issues or questions, refer to:
- API Docs: http://localhost:8000/docs
- GitHub Issues
- Documentation files in root directory

---
