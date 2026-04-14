# SmartScreen SaaS – Complete Development Plan

## 🚀 Overview
SmartScreen is a SaaS platform for Training & Placement (TnP) cells that:
- Parses resumes
- Parses job descriptions (JD)
- Matches candidates with jobs
- Provides recommendations
- Uses a credit-based billing system

---

# ⚠️ LLM USAGE POLICY (IMPORTANT)

🚫 DO NOT use:
- OpenAI API
- Any paid LLM APIs
- External API keys for inference

✅ ONLY use:
- Locally hosted / self-deployed models
- Hugging Face models (self-hosted)
- Fine-tuned models (your own)

---

## 🔧 Future LLM Setup Plan

- Model will be loaded using Hugging Face (`transformers`)
- Model configuration will be stored in `.env` file

### Example `.env`:

MODEL_NAME=mistralai/Mistral-7B-Instruct  
MODEL_PATH=/models/mistral  
DEVICE=cuda  

---

## 🧠 LLM Integration Strategy (Later Phase)

- Create `llm_service.py`
- Load model once at startup
- Use pipeline or custom inference
- Avoid repeated loading (performance issue)

---

# 🧠 SYSTEM ARCHITECTURE

Frontend → Backend (FastAPI) → Database (PostgreSQL)  
                           → Credit System  
                           → LLM Service (HF local model)

---

# ⚙️ BACKEND DEVELOPMENT (FastAPI)

## 📁 Project Structure

backend/
│
├── main.py
├── routes/
│   ├── auth.py
│   ├── resume.py
│   ├── jd.py
│   ├── match.py
│   ├── billing.py
│
├── services/
│   ├── llm_service.py   # (HF model later)
│   ├── credit_service.py
│   ├── parsing_service.py
│
├── models/
│   ├── user.py
│   ├── transaction.py
│   ├── usage.py
│
├── schemas/
│   ├── user_schema.py
│   ├── request_schema.py
│
├── db/
│   ├── connection.py
│
└── utils/
    ├── auth.py
    ├── logger.py
    ├── deps.py   # JWT dependency

---

## 🔑 Core Backend Features

### 1. Authentication
- JWT-based login/signup
- Password hashing (bcrypt)
- Protected routes using dependency injection

---

### 2. APIs

#### Auth APIs
- POST /signup
- POST /login

#### Resume APIs
- POST /parse_resume

#### JD APIs
- POST /parse_jd

#### Matching APIs
- POST /match

#### Billing APIs
- GET /credits
- POST /buy_credits (trigger payment)
- GET /transactions

---

## ⚡ Core Backend Flow

1. User sends request
2. Authenticate user (JWT)
3. Check credits
4. Process request
5. Deduct credits
6. Store result
7. Return response

---

## 🪙 Credit System (Core Logic)

### Functions:
- add_credits(user_id, amount)
- deduct_credits(user_id, amount)
- check_balance(user_id)

---

### Rules:
- Resume parse → 5 credits
- JD parse → 3 credits
- Match → 5 credits

---

### ⚠️ Important Design Rule:
- Maintain BOTH:
  - `users.credits` (fast access)
  - `transactions` table (source of truth)

---

## 🔐 Security

- JWT authentication (mandatory)
- Input validation (Pydantic)
- Rate limiting (middleware)
- Secure payment webhook
- Environment variable usage for secrets

---

# 🗄️ DATABASE DESIGN (PostgreSQL)

## Tables

### Users

| Field        | Type        |
|--------------|------------|
| id           | UUID       |
| email        | TEXT       |
| password     | TEXT       |
| credits      | INT        |
| created_at   | TIMESTAMP  |

---

### Transactions

| Field        | Type        |
|--------------|------------|
| id           | UUID       |
| user_id      | UUID       |
| type         | TEXT       |
| amount       | INT        |
| description  | TEXT       |
| created_at   | TIMESTAMP  |

---

### Usage Logs

| Field        | Type        |
|--------------|------------|
| id           | UUID       |
| user_id      | UUID       |
| action       | TEXT       |
| credits_used | INT        |
| created_at   | TIMESTAMP  |

---

### Parsed Data (Optional)

| Field        | Type        |
|--------------|------------|
| id           | UUID       |
| user_id      | UUID       |
| resume_data  | JSONB      |
| jd_data      | JSONB      |
| match_score  | INT        |

---

## 🧠 DB Best Practices

- Use JSONB for flexibility
- Add indexes on user_id
- Use DB transactions for credit operations
- Avoid SQLite in production

---

# 🎨 FRONTEND DEVELOPMENT

## 🔹 Phase 1 (MVP)
Use **Streamlit**

### Features:
- Upload Resume
- Input JD
- Show match score
- Display credits
- Buy credits button

---

## 🔹 Phase 2 (Scale)
Use **React.js**

### Pages:

#### Dashboard
- Credits balance
- Usage summary

#### Upload Page
- Resume upload
- JD input

#### Results Page
- Match score
- Recommendations

#### Billing Page
- Buy credits
- Transaction history

---

## 🔹 Frontend Stack

- React.js
- Axios (API calls)
- Tailwind CSS (UI)
- Chart.js (analytics)

---

# 💳 PAYMENT INTEGRATION

## Use:
- :contentReference[oaicite:0]{index=0}

---

## Flow:

1. User clicks "Buy Credits"
2. Payment page opens
3. Payment success
4. Webhook triggers backend
5. Credits added to user

---

## Backend Webhook

- Verify signature
- Update DB
- Log transaction

---

# ⚡ SCALABILITY PLAN

## 🔹 Stage 1 (MVP)
- Single FastAPI server
- Single GPU (external or local)

---

## 🔹 Stage 2 (Growth)

Add:
- :contentReference[oaicite:1]{index=1} (caching)
- Background jobs (Celery)

---

## 🔹 Stage 3 (Scale)

- Multiple workers
- Load balancing
- Separate services

---

# 🚀 DEPLOYMENT PLAN

## 🔹 Backend
- Use: Render / Railway / VPS

## 🔹 Database
- Neon (PostgreSQL)

## 🔹 Frontend
- Vercel / Netlify

---

# 📊 MONITORING

Track:
- API latency
- Credits usage
- Errors

---

# 🧪 TESTING PLAN

## Unit Testing
- API endpoints
- Credit logic

## Integration Testing
- Full pipeline

## User Testing
- 2–3 colleges

---

# 💰 PRICING MODEL

## Base Plan
- ₹5,000/month
- Includes credits

## Usage
- Extra credits charged

---

# 🗓️ DEVELOPMENT TIMELINE

## Week 1
- Backend setup
- DB setup (PostgreSQL)

## Week 2
- Core APIs
- Credit system
- JWT protection

## Week 3
- Frontend (Streamlit)
- Payment integration

## Week 4
- Testing
- Deployment

---

# ⚠️ RISKS & SOLUTIONS

| Risk | Solution |
|------|---------|
| High GPU cost | Optimize tokens |
| Low adoption | Early feedback |
| Bugs in billing | Use transactions |
| Model latency | Load model once |

---

# 🎯 FINAL GOAL

Build a:
- Scalable SaaS
- Credit-based system
- Fully self-hosted AI product (no external LLM dependency)

---

# 🔥 MVP CHECKLIST

- [ ] Auth system
- [ ] Resume parsing
- [ ] JD parsing
- [ ] Matching logic
- [ ] Credit system
- [ ] Payment integration
- [ ] Basic UI
- [ ] Deployment
- [ ] Local HF model integration (later phase)

---