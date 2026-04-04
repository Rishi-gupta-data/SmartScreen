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
  OLLAMA_MODEL = "openai/gpt-oss-120b"
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
- Use `sentence-transformers/all-MiniLM-L6-v2` for high-quality semantic embeddings
- Compute cosine similarity
- Output:
- Match score (0–100)

### Phase 6: Removed (Ollama/LLM Integration)
> Note: LLM generative features have been removed to focus on efficient, local semantic matching.

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

