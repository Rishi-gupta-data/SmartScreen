# 🚀 SmartScreen Production Deployment Guide

## Phase 1: Database Setup (Neon PostgreSQL)

### Step 1: Create Neon Account
1. Go to [neon.tech](https://neon.tech)
2. Sign up with GitHub/Google
3. Create new project: `smartscreen-prod`
4. Region: Select closest to your target audience
5. PostgreSQL version: 16 (latest stable)

### Step 2: Get Connection String
1. After project creation, go to **Connection String**
2. Copy the connection string (looks like):
   ```
   postgresql://neondb_owner:password@ep-xxxx.us-east-1.neon.tech/neondb?sslmode=require
   ```
3. Keep this safe ✅

### Step 3: Create Local .env File
In SmartScreen root directory:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
SECRET_KEY=generate-random-complex-string-here
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Phase 2: Initialize Database Schema

### Step 1: Install Dependencies
```bash
# Activate virtual environment
c:\Users\RishiGupta\SmartScreen\venv\Scripts\activate.bat

# Install production requirements
pip install -r requirements-prod.txt
```

### Step 2: Create Tables
```bash
cd backend
python create_tables.py
```

You should see:
```
✓ Connection successful!
✓ Creating users table...
✓ Creating transactions table...
✓ All tables created successfully!
```

**Verify in Neon Dashboard:**
- Go to Neon console → Tables
- Confirm all tables exist ✅

---

## Phase 3: Deploy Backend to Render

### Option A: Using Render Dashboard (Easiest)

#### Step 1: Prepare for Deployment
```bash
# Make sure Procfile exists
# Make sure requirements-prod.txt exists
# Commit everything to Git
git add .
git commit -m "Production deployment setup"
git push origin main
```

#### Step 2: Create Render Service
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select your SmartScreen GitHub repository
5. Fill in details:
   - **Name:** smartscreen-api
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements-prod.txt`
   - **Start Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT backend.main:app`

#### Step 3: Add Environment Variables
In Render dashboard → Environment:

```
DATABASE_URL=postgresql://...
SECRET_KEY=your-generated-secret
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=["https://yourdomain.com"]
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

#### Step 4: Deploy
- Click **Create Web Service**
- Render automatically deploys from main branch
- Monitor logs in Render dashboard
- Once green: ✅ Your API is live!

#### Step 5: Get API URL
Render provides URL like: `https://smartscreen-api.onrender.com`

---

### Option B: Using Railway (Alternative)

1. Go to [railway.app](https://railway.app)
2. Click **Create Project** → **Deploy from GitHub Repo**
3. Select SmartScreen repo
4. Wait for auto-detection → select Python
5. Add variables (right panel):
   - DATABASE_URL
   - SECRET_KEY
   - ENVIRONMENT=production
6. Deploy automatically starts

---

## Phase 4: Verify Deployment

### Test Health Endpoint
```bash
curl https://smartscreen-api.onrender.com/health
# Should return: {"status":"ok","environment":"production"}
```

### Test Auth Endpoint
```bash
curl -X POST https://smartscreen-api.onrender.com/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"TestPass123!"
  }'

# Should return: {"id":"...","email":"test@example.com","..."}
```

### Test Complete Flow
```bash
# 1. Login
curl -X POST https://smartscreen-api.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"TestPass123!"
  }'
# Copy the "access_token" from response

# 2. Parse Resume
curl -X POST https://smartscreen-api.onrender.com/parse_resume \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text":"John Doe\nSoftware Engineer\nPython, FastAPI, PostgreSQL\n5 years experience"
  }'

# 3. Parse JD
curl -X POST https://smartscreen-api.onrender.com/parse_jd \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jd_text":"Senior Backend Engineer\nRequired: Python, FastAPI, Docker\n5+ years"
  }'

# 4. Match Resume to JD
curl -X POST https://smartscreen-api.onrender.com/match \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text":"...",
    "jd_text":"..."
  }'
```

---

## Phase 5: Monitoring & Logs

### View Logs on Render
```
Render Dashboard → Your Service → Logs
```

Watch for errors:
- Database connection issues
- Missing environment variables
- Deployment crashes

### Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `DATABASE_URL not set` | Add DATABASE_URL to Environment variables |
| `Temporary Failure in Name Resolution` | Check DATABASE URL is correct in Neon |
| `ssl certificate verify failed` | Add `?sslmode=require` to DATABASE_URL |
| `Port already in use` | Render handles ports automatically |
| `AttributeError: module 'backend' has no attribute 'main'` | Make sure `backend/main.py` exists and imports correctly |

---

## Phase 6: Frontend Integration

Update React frontend API endpoint:

**frontend/src/services/api.js:**
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  'https://smartscreen-api.onrender.com';

export const api = axios.create({
  baseURL: API_BASE_URL,
});
```

In `.env.local`:
```
REACT_APP_API_URL=https://smartscreen-api.onrender.com
```

---

## Phase 7: Production Checklist

- [x] PostgreSQL database created on Neon
- [x] Connection string obtained
- [x] .env file configured locally
- [x] Database schema created
- [x] Backend deployed to Render/Railway
- [x] Environment variables set in Render
- [x] Health endpoint verified
- [x] Auth APIs tested
- [x] Parsing APIs tested
- [x] Match API tested
- [x] Credit deduction verified
- [x] Logs monitored
- [x] Frontend API endpoint updated

---

## Next Steps: Frontend Deployment

Once backend is verified:

1. **Deploy React to Vercel:**
   ```bash
   npm install -g vercel
   cd frontend
   vercel
   ```

2. **Or deploy to Netlify:**
   ```bash
   npm run build
   # Drag & drop 'build' folder to Netlify
   ```

---

## Support & Troubleshooting

**Database Connection Test:**
```bash
python
>>> import psycopg2
>>> conn = psycopg2.connect("postgresql://...")
>>> cur = conn.cursor()
>>> cur.execute("SELECT 1")
>>> print(cur.fetchone())  # Should print (1,)
```

**API Health Check:**
```bash
curl https://smartscreen-api.onrender.com/docs
# Opens Swagger UI if API is running
```

---

**🎉 Your SmartScreen backend is now production-ready!**

Next: Deploy React frontend to complete the system.
