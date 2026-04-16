# SmartScreen API Documentation

## 🎯 Overview
SmartScreen SaaS API provides:
- Resume parsing
- Job description (JD) analysis
- Resume-to-job matching
- Credit-based billing system

---

## ⚠️ LLM POLICY (IMPORTANT)

🚫 This system DOES NOT use:
- External LLM APIs (OpenAI, etc.)
- Paid inference services
- API keys for model access

✅ This system WILL use:
- Self-hosted Hugging Face models
- Fine-tuned local models
- Configurable via environment variables

---

## 🔧 Future LLM Configuration (.env)

```
MODEL_NAME=mistralai/Mistral-7B-Instruct
MODEL_PATH=/models/mistral
DEVICE=cuda
```

👉 LLM will be loaded in `llm_service.py` during startup (singleton pattern)

---

## 🌐 Base Configuration

- **Base URL:** `http://127.0.0.1:8001`
- **Auth Type:** Bearer Token (JWT)
- **Content-Type:** application/json

---

## 🔐 Authentication Endpoints

### 1. Signup
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 💳 Credit Management Endpoints

### 3. Get Credit Balance
```http
GET /credits/
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user_id": "af8f865d-d078-4b17-90f6-dd8721eda00e",
  "credits": 50
}
```

---

### 3. Get Credit Balance
```http
GET /credits/
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user_id": "af8f865d-d078-4b17-90f6-dd8721eda00e",
  "credits": 50
}
```

---

### 4. Add Credits (Admin / Payment Webhook Only)
```http
POST /credits/add
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 100
}
```

⚠️ **PRODUCTION NOTE:**
- This endpoint should NOT be exposed to frontend
- Use payment webhook only (Razorpay/Stripe callback)
- Should have admin-only middleware

---

### 5. Deduct Credits (Internal Only - Testing)
```http
POST /credits/deduct
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 10
}
```

⚠️ **PRODUCTION NOTE:**
- Internal/testing only
- Should be removed or protected with admin middleware
- Credits deducted automatically by parsing/matching endpoints

---

### 6. Get Transaction History
```http
GET /transactions
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "transactions": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "type": "deduct",
      "amount": 5,
      "description": "consumed for operation",
      "created_at": "2024-04-14T10:30:00Z"
    },
    {
      "id": "uuid",
      "user_id": "uuid",
      "type": "add",
      "amount": 50,
      "description": "credit top-up",
      "created_at": "2024-04-14T10:25:00Z"
    }
  ]
}
```

---

## 💳 Credit System Rules

| Operation | Credits | Notes |
|-----------|---------|-------|
| Resume Parse | 5 | Deducted after successful parse |
| JD Parse | 3 | Deducted after successful parse |
| Matching | 5 | Deducted after successful match |
| **Full Workflow** | **13** | All three operations |

---

## 📄 Resume Parsing Endpoint

### 6. Parse Resume
**Cost:** 5 credits per request

```http
POST /resume/parse
Authorization: Bearer <token>
Content-Type: application/json

{
  "resume_text": "John Doe\njohn@example.com\n\nSKILLS\nPython, Java, React, Django...",
  "file_name": "john_doe_resume.txt"
}
```

**Response (200):**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-1234",
  "skills": ["python", "java", "react", "django", "fastapi"],
  "experience": [
    {
      "company": "Unknown",
      "role": "Unknown",
      "duration": "Unknown"
    }
  ],
  "education": [
    {
      "institution": "Unknown",
      "degree": "Unknown",
      "field": "Unknown"
    }
  ],
  "raw_text": "John Doe\njohn@example.com\n\nSKILLS\nPython, Java, React, Django...",
  "credits_deducted": 5
}
```

**Error Response (400):**
```json
{
  "detail": "Insufficient credits. Required: 5, Available: 2"
}
```

---

## 📋 Job Description Parsing Endpoint

### 7. Parse JD
**Cost:** 3 credits per request

```http
POST /jd/parse
Authorization: Bearer <token>
Content-Type: application/json

{
  "jd_text": "Senior Python Developer\n\nRequired Skills:\n- Python\n- 5+ years experience\n\nPreferred:\n- Docker\n- Kubernetes",
  "file_name": "job_posting.txt"
}
```

**Response (200):**
```json
{
  "title": "Senior Python Developer",
  "company": null,
  "required_skills": ["python", "docker", "kubernetes"],
  "preferred_skills": [],
  "experience_required": "5+ years",
  "salary_range": null,
  "qualifications": ["Bachelor's Degree", "Relevant Experience"],
  "responsibilities": [
    "Design and implement backend systems",
    "Mentor junior developers"
  ],
  "raw_text": "Senior Python Developer\n\nRequired Skills:\n...",
  "credits_deducted": 3
}
```

---

## 🎯 Resume-to-JD Matching Endpoint

### 8. Match Resume to JD
**Cost:** 5 credits per request

```http
POST /match/
Authorization: Bearer <token>
Content-Type: application/json

{
  "resume_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "skills": ["python", "java", "react", "django", "fastapi"],
    "experience": [...],
    "education": [...]
  },
  "jd_data": {
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "required_skills": ["python", "django", "rest apis"],
    "preferred_skills": ["docker", "kubernetes"],
    "qualifications": ["Bachelor's in Computer Science"]
  }
}
```

**Response (200):**
```json
{
  "match_score": 72.5,
  "skill_match": {
    "required_matched": ["python", "django"],
    "preferred_matched": [],
    "match_percentage": 66.67
  },
  "experience_match": "Not analyzed (placeholder)",
  "education_match": "Not analyzed (placeholder)",
  "overall_recommendation": "Good Match - Recommended",
  "missing_skills": ["rest apis"],
  "bonus_skills": [],
  "credits_deducted": 5
}
```

---

## 📊 Credit Cost Summary

| Operation | Credits | Endpoint |
|-----------|---------|----------|
| Resume Parse | 5 | POST /resume/parse |
| JD Parse | 3 | POST /jd/parse |
| Matching | 5 | POST /match/ |
| **Total Flow** | **13** | All three operations |

---

## 🔄 Example Complete Workflow

```
1. Signup: POST /auth/signup
2. Add Credits: POST /credits/add (50 credits)
3. Check Balance: GET /credits/ (50 credits)
4. Parse Resume: POST /resume/parse (-5 credits = 45 remaining)
5. Parse JD: POST /jd/parse (-3 credits = 42 remaining)
6. Match: POST /match/ (-5 credits = 37 remaining)
```

---

## ✅ Smoke Test Results

```
[1/7] Signing up... ✅ Signup successful
[2/7] Checking initial credits... ✅ Credits check successful
[3/7] Adding credits (50)... ✅ Credits added
[4/7] Parsing resume (5 credits)... ✅ Resume parsed: 7 skills found
[5/7] Parsing JD (3 credits)... ✅ JD parsed
[6/7] Matching resume to JD (5 credits)... ✅ Match calculated: 72.5%
[7/7] Checking final credits... ✅ Final balance: 37 (13 credits used)
```

---

## 🔧 Error Handling

### Common Errors

**401 Unauthorized:**
```json
{"detail": "Invalid token"}
```

**400 Bad Request (Insufficient Credits):**
```json
{"detail": "Insufficient credits. Required: 5, Available: 2"}
```

**400 Bad Request (Invalid Input):**
```json
{"detail": "Both resume_data and jd_data are required"}
```

**500 Internal Server Error:**
```json
{"detail": "Error parsing resume: [error message]"}
```

---

## 🚀 Next Enhancements

- [ ] File upload support (PDF, DOCX parsing)
- [ ] Bulk analysis endpoint
- [ ] Transaction history GET endpoint
- [ ] HuggingFace model integration
- [ ] Advanced NER for better extraction
- [ ] Rate limiting
- [ ] API usage analytics

---

## 📝 Notes

- All endpoints require valid JWT token in `Authorization: Bearer <token>` header
- Credit transactions are logged in the `transactions` table
- User credit balance is maintained in the `users` table
- All parsing is currently using regex-based extraction (placeholders for ML models)
