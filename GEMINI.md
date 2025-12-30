Here is a **complete `GEMINI.md`** you can drop directly into your repository root.
This is written as **clear, enforceable instructions** for Gemini CLI (or any coding LLM) so it understands **scope, constraints, architecture, and behavior** for SmartScreen.

---

md
# GEMINI.md
## SmartScreen – Intelligent Applicant Tracking System (ATS)

This document defines **strict instructions, scope, and constraints** for any AI coding assistant (Gemini CLI or similar) working on the SmartScreen project.

---

## 🔒 CORE RULES (MANDATORY)

1. **DO NOT use any external paid APIs**
   - No Gemini API
   - No OpenAI
   - No Anthropic
   - No cloud LLM inference

2. **LOCAL-FIRST DESIGN**
   - All logic must run locally
   - Must work in GitHub Codespaces
   - Must be portable to a self-hosted Linux server (SSH-only)

3. **NO FRONTEND IN MVP**
   - Backend-only
   - REST APIs only
   - JSON responses only

4. **LLM USAGE IS OPTIONAL & ABSTRACTED**
   - LLMs must be behind an abstraction layer
   - Default state: **LLM DISABLED**
   - Code must run even if no LLM is installed

5. **CLEAN, MODULAR CODE**
   - No monolithic `app.py`
   - Follow separation of concerns
   - Production-style folder structure

---

## 🎯 PROJECT GOAL (MVP)

Build a **Minimum Viable Product (MVP)** of an **Intelligent Applicant Tracking System (ATS)** that:

- Accepts resumes (PDF / DOCX)
- Accepts a job description (text)
- Extracts and processes text
- Computes similarity between resume and job description
- Ranks candidates by relevance score
- Runs fully offline

---

## 🧩 MVP SCOPE (WHAT TO BUILD)

### 1. Resume Processing
- Accept PDF and DOCX files
- Extract raw text
- Store text locally
- Handle multiple resumes

### 2. Job Description Processing
- Accept plain text input
- Store job descriptions
- Reuse job descriptions for matching

### 3. NLP & Matching
- Use spaCy (`en_core_web_md`)
- Use vector similarity / cosine similarity
- Return similarity score (0–1)
- Deterministic, explainable scoring

### 4. Ranking
- Rank resumes based on score
- Return sorted list
- Support top-N results

### 5. API Design
- Flask-based REST API
- Stateless endpoints
- JSON in / JSON out

---

## 🚫 OUT OF SCOPE (DO NOT IMPLEMENT)

- No UI / dashboard
- No authentication
- No role-based access
- No resume fine-tuning
- No cloud deployment logic
- No GPU-specific optimizations (yet)
- No background task queues
- No web scraping

---

## 🏗️ REQUIRED PROJECT STRUCTURE


SmartScreen/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── resume_api.py
│   │   ├── job_api.py
│   │   └── match_api.py
│   │
│   ├── services/
│   │   ├── resume_parser.py
│   │   ├── job_parser.py
│   │   ├── matcher.py
│   │   └── llm_engine.py
│   │
│   ├── models/
│   │   ├── db.py
│   │   ├── candidate.py
│   │   └── job.py
│   │
│   ├── embeddings/
│   │   └── vector_store.py
│   │
│   └── utils/
│       └── file_utils.py
│
├── data/
│   ├── resumes/
│   ├── jobs/
│   └── embeddings/
│
├── scripts/
│   └── init_db.py
│
├── requirements.txt
├── docker/
│   └── Dockerfile
└── README.md



---

## 🧠 LLM USAGE POLICY

### Allowed
- Code generation assistance
- Refactoring suggestions
- Explaining architecture
- Writing tests or documentation

### NOT Allowed
- Making API calls to LLM services
- Embedding secret keys
- Tight coupling logic to Gemini or any LLM

### LLM Abstraction Rule
All LLM logic must live inside:



backend/services/llm_engine.py



With behavior like:
- Graceful fallback if LLM not installed
- No hard dependency on Ollama / llama.cpp
- Easy swap in future

---

## 🗄️ DATABASE RULES

- Use SQLite for MVP
- Must be abstracted via SQLAlchemy
- Schema must support:
  - Candidates
  - Job descriptions
  - Scores / metadata

Switching to MySQL later must require **minimal changes**.

---

## 🧪 TESTING & QUALITY

- Prefer simple unit-testable functions
- Avoid magic numbers
- Use clear variable naming
- Add comments only where logic is non-obvious

---

## 📦 DEPLOYMENT EXPECTATIONS

- Must run in:
  - GitHub Codespaces
  - Local Linux machine
  - Self-hosted home server
- Docker support is required but optional in MVP
- No systemd / supervisor configs yet

---

## ✅ MVP SUCCESS CRITERIA

The MVP is considered complete when:

- A job description and resumes can be submitted
- The system returns ranked candidates with scores
- Everything runs offline
- Codebase is clean, modular, and extensible
- LLM integration can be added later without refactor

---

## 🔮 FUTURE PHASES (DO NOT IMPLEMENT NOW)

- Vector databases (FAISS / Chroma)
- Local LLM inference (Ollama / llama.cpp)
- GPU acceleration
- Authentication & RBAC
- UI dashboard
- Cloud deployment
- Resume fine-tuning

---

## 🧭 GUIDING PRINCIPLE

> **Build for correctness, clarity, and extensibility first.  
> Optimize and add intelligence later.**

Any suggestion or code must respect this principle.
