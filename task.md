# 📌 SmartScreen – Task Breakdown (MVP)

## 🎯 Objective
Build a **local-first, backend-only resume screening system** that:
- Parses resumes and job descriptions
- Computes semantic match scores **offline**
- Optionally uses a **local LLM (Ollama)** for explainability and suggestions
- Works without paid APIs or cloud dependency

This MVP prioritizes **privacy, cost-efficiency, and extensibility**.

---

## 🧩 Core Principles
- **Offline by default**
- **Modular backend architecture**
- **LLM is optional, not required**
- **Deterministic scoring + explainable AI**
- **Future-ready for GPU / self-hosted inference**

---

## 🏗️ Phase 1: Project Foundation

### Task 1.1 – Repository Structure
- Create modular backend layout:


backend/
├── api/
├── services/
├── models/
├── utils/
├── config.py
└── app.py
data/
scripts/


- Ensure separation of concerns

✅ Outcome: Clean, scalable backend structure

---

### Task 1.2 – Configuration Management
- Implement `backend/config.py`
- Add:
- SQLite database URL
- App-level settings
- LLM toggles:
  ```python
  LLM_PROVIDER = "none" | "ollama"
  OLLAMA_BASE_URL = "http://localhost:11434"
  OLLAMA_MODEL = "phi3:mini"
  ```

✅ Outcome: Centralized, environment-agnostic configuration

---

## 🗄️ Phase 2: Database & Models

### Task 2.1 – Database Models
Implement SQLAlchemy models:
- `Candidate`
- `Job`
- `Match` (stores similarity scores + metadata)

### Task 2.2 – Database Initialization
- Create `scripts/init_db.py`
- Auto-create tables on first run

✅ Outcome: Persistent, queryable data layer

---

## 📄 Phase 3: Resume & Job Parsing

### Task 3.1 – Resume Parsing Service
Implement `services/resume_parser.py`:
- Support:
- PDF (pdfplumber)
- DOCX (python-docx)
- ZIP archives (bulk upload)
- Output normalized plain text

### Task 3.2 – Job Description Handling
- Accept raw job description text
- Normalize and store for matching

✅ Outcome: Reliable document ingestion pipeline

---

## 🧠 Phase 4: Core Matching Engine (Offline)

### Task 4.1 – Semantic Matching
Implement `services/matcher.py`:
- Use SpaCy embeddings
- Compute cosine similarity
- Output:
- Match score (0–100)
- Skill overlap indicators (optional)

### Task 4.2 – Match Persistence
- Store results in `Match` table
- Link `Candidate ↔ Job`

✅ Outcome: Deterministic, offline resume-job scoring

---

## 🌐 Phase 5: API Layer

### Task 5.1 – Resume API
- Upload resumes
- Parse and store candidate data

### Task 5.2 – Job API
- Create and manage job descriptions

### Task 5.3 – Match API
- Trigger matching
- Fetch ranked candidates for a job

Refactor `backend/app.py` as an **application factory**.

✅ Outcome: Clean RESTful backend interface

---

## 🤖 Phase 6: Optional Local LLM Integration (Ollama)

> ⚠️ **This phase is OPTIONAL. Core MVP must work without it.**

### Task 6.1 – LLM Abstraction
- Implement `services/llm_engine.py`
- Handle provider switching via config
- Default to disabled

### Task 6.2 – Ollama Integration
- Use OpenAI-compatible client
- Connect to local Ollama server
- Support lightweight models (e.g. `phi3:mini`)

### Task 6.3 – Suggestions API
Add endpoint:


GET /api/suggestions/match/<match_id>


- Generate:
  - Resume improvement suggestions
  - Skill gap explanations
- Fail gracefully if Ollama is unavailable

✅ Outcome: Explainable AI without cloud dependency

---

## 🧪 Phase 7: Testing & Validation

### Task 7.1 – Offline Validation
- Confirm full system works with:
  - No internet
  - No LLM enabled

### Task 7.2 – LLM Validation
- Test Ollama integration
- Verify timeout handling & fallback behavior

✅ Outcome: Robust, failure-safe system

---

## 🚀 Future Enhancements (Post-MVP)
- Skill ontology & taxonomy
- Batch processing (1 job → N resumes)
- RAG over resume corpus
- GPU acceleration
- Recruiter dashboard (frontend)
- Model benchmarking & evaluation metrics

---

## ✅ Definition of Done (MVP)
- [x] Offline resume-job matching works end-to-end
- [x] No paid APIs required
- [x] Modular, readable backend code
- [x] Ollama integration is optional & configurable
- [x] System deployable on a local server via SSH

---

## 🧠 Final Note
SmartScreen is designed as a **self-hosted, privacy-first ATS intelligence engine**, not a demo app.

LLMs enhance understanding — they do not control decisions.

