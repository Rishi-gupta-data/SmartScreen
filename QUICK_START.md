# 🚀 SmartScreen Production Deployment - Quick Start

## What's Ready ✅

Your application is now configured for production deployment:

```
✅ Enhanced parsing & matching service (tested)
✅ Production requirements.txt
✅ Database schema script
✅ Environment configuration (.env support)
✅ Production-ready main.py with logging
✅ Render/Railway deployment files (Procfile)
✅ Comprehensive deployment guide
✅ API testing suite
```

---

## 5-Minute Setup 🏃

### Step 1: Get PostgreSQL Connection String

**Go to [neon.tech](https://neon.tech):**
1. Sign up (free tier)
2. Create project → "smartscreen-prod"
3. Copy connection string

📝 **Example:**
```
postgresql://user:password@ep-xxxx.us-east-1.neon.tech/neondb?sslmode=require
```

---

### Step 2: Create `.env` File

In your SmartScreen root:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` and fill in:
```
DATABASE_URL=postgresql://... (from Neon)
SECRET_KEY=<run: python -c "import secrets; print(secrets.token_urlsafe(32))">
ENVIRONMENT=production
```

---

### Step 3: Initialize Database

```bash
# Activate venv
c:\Users\RishiGupta\SmartScreen\venv\Scripts\activate.bat

# Install production deps
pip install -r requirements-prod.txt

# Create tables
cd backend
python create_tables.py
```

✅ You should see: `All tables created successfully!`

---

### Step 4: Test Locally

```bash
# Start API server
python -m uvicorn backend.main:app --reload --port 8000

# In another terminal, run tests
python backend/tests/test_production_api.py
```

✅ Should see: `All tests passed! API is production-ready!`

---

### Step 5: Deploy to Render

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Production deployment setup"
   git push origin main
   ```

2. **Create Render service:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New+" → "Web Service"
   - Select your repo
   - Fill in:
     - Build: `pip install -r requirements-prod.txt`
     - Start: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT backend.main:app`

3. **Add environment variables in Render:**
   - DATABASE_URL (from Neon)
   - SECRET_KEY (generate new)
   - ENVIRONMENT=production

4. **Deploy** → Done! 🎉

---

## Get Your API URL 📍

After deployment completes, you'll have:
```
https://smartscreen-api.onrender.com
```

Test it:
```bash
curl https://smartscreen-api.onrender.com/health
```

---

## Next: Frontend Deployment

Update React frontend `.env.local`:
```
REACT_APP_API_URL=https://smartscreen-api.onrender.com
```

Deploy to Vercel/Netlify:
```bash
cd frontend
npm run build
# Deploy 'build' folder
```

---

## Troubleshooting 🔧

| Problem | Fix |
|---------|-----|
| "DATABASE_URL not set" | Add to Render env vars |
| "Connection refused" | Check Neon connection string has `?sslmode=require` |
| "Port already in use" | Render handles ports automatically |
| Health check fails | Verify database connection in Neon dashboard |

---

## Documentation 📚

- **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
- **API Testing:** `backend/tests/test_production_api.py`
- **Config:** `backend/config.py`

---

## Performance Targets ⚡

- Parse Resume: < 2 seconds
- Parse JD: < 2 seconds  
- Match: < 1 second
- Health Check: < 100ms

---

## Next Steps

1. ✅ Set up Neon database
2. ✅ Deploy to Render
3. ✅ Test all APIs
4. 🔜 Deploy React frontend
5. 🔜 (Optional) Integrate Razorpay for payments
6. 🔜 (Future) Add Hugging Face LLM

---

**Your SmartScreen backend is production-ready! Deploy now! 🚀**
