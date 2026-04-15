# SmartScreen Quick Reference

## 🚀 Start Everything

### Terminal 1: Backend
```bash
cd backend
export PYTHONPATH=.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm start
```

## 📍 Endpoints Quick Access

| Feature | Endpoint | Method | Auth |
|---------|----------|--------|------|
| Signup | /auth/signup | POST | ❌ |
| Login | /auth/login | POST | ❌ |
| Parse Resume | /resume/parse | POST | ✅ |
| Parse JD | /jd/parse | POST | ✅ |
| Match | /match/ | POST | ✅ |
| Get Balance | /billing/credits | GET | ✅ |
| Buy Credits | /billing/buy-credits | POST | ✅ |
| History | /billing/transactions | GET | ✅ |
| Swagger Docs | /docs | GET | ❌ |

## 💳 Credit Costs

```
Parse Resume  = 5 credits
Parse JD      = 3 credits
Match Resume  = 5 credits
```

## 🔐 JWT Token

**Format**: `Authorization: Bearer <token>`

**Expires**: 24 hours (configurable in `SECRET_KEY`)

**Extract from login response**:
```javascript
const response = await api.login(email, password);
localStorage.setItem('access_token', response.access_token);
```

## 📝 Request/Response Examples

### 1. Signup
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123"}'

Response:
{"access_token": "eyJ...", "token_type": "bearer"}
```

### 2. Parse Resume
```bash
curl -X POST http://localhost:8000/resume/parse \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"John Doe\nPython, FastAPI, PostgreSQL"}'

Response:
{
  "name": "John Doe",
  "email": null,
  "phone": null,
  "skills": ["python", "fastapi", "postgresql"],
  "credits_used": 5,
  "remaining_credits": 95
}
```

### 3. Match Resume to JD
```bash
curl -X POST http://localhost:8000/match/ \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text":"John Doe\nSkills: Python, FastAPI, PostgreSQL",
    "jd_text":"Senior Backend Engineer\nRequired: Python, FastAPI"
  }'

Response:
{
  "match_score": 95.0,
  "overall_recommendation": "Excellent Match - Highly Recommended",
  "missing_skills": [],
  "credits_used": 5,
  "remaining_credits": 90
}
```

## 🗄️ Database Tables

### users
```sql
SELECT * FROM users;
-- id, email, hashed_password, credits, role, created_at
```

### transactions
```sql
SELECT * FROM transactions;
-- id, user_id, type ('add'/'deduct'), amount, description, created_at
```

### usage_logs
```sql
SELECT * FROM usage_logs;
-- id, user_id, action, credits_used, details, created_at
```

## 🔧 Configuration Files

### Backend .env
```
DATABASE_URL=sqlite:///./smartscreen.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### Frontend .env
```
REACT_APP_API_URL=http://localhost:8000
```

## 📁 File Locations

```
src/
├── routes/
│   ├── auth.py         - /auth/* endpoints
│   ├── resume.py       - /resume/parse endpoint
│   ├── jd.py           - /jd/parse endpoint
│   ├── match.py        - /match/ endpoint
│   └── billing.py      - /billing/* endpoints
│
├── services/
│   ├── auth.py         - Auth logic (hashing, JWT)
│   ├── credit_service.py - add/deduct/check balance
│   └── parsing_service.py - parse_resume, parse_jd, match
│
└── models/
    ├── user.py        - User SQLAlchemy model
    ├── transaction.py - Transaction model
    └── usage.py       - UsageLog model
```

## 🆘 Common Issues

### Issue: "CORS error"
**Solution**: Check `CORS_ORIGINS` in .env, add frontend URL

### Issue: "Invalid token"
**Solution**: Token expired or malformed. Re-login to get new token

### Issue: "Insufficient credits"
**Solution**: User must buy credits first via `/billing/buy-credits`

### Issue: "Database Error"
**Solution**: For SQLite, check file permissions. For PostgreSQL, verify connection string

## 🧪 API Testing Tools

### Using cURL
```bash
export TOKEN="eyJ..."
curl -X GET http://localhost:8000/billing/credits \
  -H "Authorization: Bearer $TOKEN"
```

### Using Swagger UI
Go to: http://localhost:8000/docs (automatically available when backend runs)

### Using Python Requests
```python
import requests
headers = {"Authorization": "Bearer eyJ..."}
response = requests.get("http://localhost:8000/billing/credits", headers=headers)
print(response.json())
```

### Using JavaScript Fetch
```javascript
const token = localStorage.getItem('access_token');
const response = await fetch('http://localhost:8000/billing/credits', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();
```

## 🚀 Deployment Checklist

- [ ] Update SECRET_KEY to random value
- [ ] Change DATABASE_URL to PostgreSQL
- [ ] Set ENVIRONMENT=production
- [ ] Update CORS_ORIGINS with production domain
- [ ] Enable HTTPS for frontend
- [ ] Setup error monitoring
- [ ] Configure backup strategy
- [ ] Test all endpoints in production

## 📊 Monitoring & Logs

### View Backend Logs
```bash
# Check backend terminal for real-time logs
# Or check database for transaction history
SELECT * FROM transactions ORDER BY created_at DESC LIMIT 10;
```

### Database Queries

Get user credit history:
```sql
SELECT * FROM transactions WHERE user_id = 'user_id' ORDER BY created_at DESC;
```

Get total credits used by user:
```sql
SELECT SUM(amount) FROM transactions WHERE user_id = 'user_id' AND type = 'deduct';
```

Get usage statistics:
```sql
SELECT action, COUNT(*), SUM(credits_used) FROM usage_logs GROUP BY action;
```

## 🎓 Key Files to Understand

1. **backend/main.py** - App setup, router registration
2. **backend/routes/auth.py** - Authentication logic
3. **backend/services/credit_service.py** - Credit system core
4. **backend/services/parsing_service.py** - Data extraction
5. **frontend/src/services/api.js** - API client

## 🔮 Future Development

When adding HF models:
```python
# In backend/services/parsing_service.py
from transformers import pipeline

class HFParsingService:
    def __init__(self):
        self.resume_extractor = pipeline("ner", model="distilbert-base-uncased")
    
    def parse_resume(self, text):
        # Use model instead of regex
        pass
```

## 📞 Quick Help

- API Docs: http://localhost:8000/docs
- Backend Guide: `BACKEND_SETUP.md`
- Full API Reference: `API_DOCUMENTATION.md`
- Project Checklist: `COMPLETION_CHECKLIST.md`

---

**Ready to build? Start with the setup guides above!** 🚀
