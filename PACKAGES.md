# SmartScreen - Complete Package List

## 📦 All Packages Used

### Installation
```bash
pip install -r requirements.txt
```

---

## 📊 Package Summary

| Category | Package | Version | Purpose |
|----------|---------|---------|---------|
| **WEB FRAMEWORK** | fastapi | 0.115.8 | Modern async web framework |
| | uvicorn[standard] | 0.30.0 | ASGI server |
| | python-multipart | 0.0.6 | Multipart form data handling |
| | httptools | 0.6.2 | HTTP parser (performance) |
| **DATABASE** | sqlalchemy | 2.0.45 | SQL toolkit and ORM |
| | psycopg2-binary | 2.9.10 | PostgreSQL adapter for Python |
| | alembic | 1.13.3 | Database migrations |
| **AUTH & SECURITY** | python-jose[cryptography] | 3.3.0 | JWT token handling |
| | pyjwt | 2.10.1 | JSON Web Token implementation |
| | argon2-cffi | 25.1.0 | Password hashing (Argon2) |
| | cryptography | 43.0.0 | Cryptographic recipes |
| | email-validator | 2.2.0 | Email validation |
| **CONFIG & VALIDATION** | pydantic | 2.10.6 | Data validation using type hints |
| | pydantic-settings | 2.7.1 | Settings management |
| | python-dotenv | 1.0.1 | Environment variables from .env |
| **LOGGING** | python-json-logger | 3.2.1 | JSON logging formatter |
| | structlog | 24.4.0 | Structured logging library |
| **HTTP CLIENT** | requests | 2.31.0 | HTTP library |
| **PRODUCTION** | gunicorn | 22.0.0 | WSGI HTTP Server |
| **TESTING** | pytest | 7.4.0 | Testing framework |
| | pytest-asyncio | 0.21.0 | AsyncIO support for pytest |
| | httpx | 0.25.0 | Async HTTP client for testing |
| **CODE QUALITY** | black | 23.0.0 | Code formatter |
| | flake8 | 6.0.0 | Code linter |

---

## 🎯 Breakdown by Purpose

### 🔌 Web & API (4 packages)
- **fastapi** - Modern async web framework for building APIs
- **uvicorn** - ASGI server that runs FastAPI
- **python-multipart** - Handles file uploads and form data
- **httptools** - Performance boost for HTTP parsing

### 💾 Database (3 packages)
- **sqlalchemy** - ORM for database queries and models
- **psycopg2-binary** - PostgreSQL connector (Neon compatibility)
- **alembic** - Database schema migrations

### 🔐 Security (5 packages)
- **python-jose** - JWT token creation and validation
- **pyjwt** - JSON Web Token standard library
- **argon2-cffi** - Secure password hashing algorithm
- **cryptography** - Encryption and cryptographic operations
- **email-validator** - Email validation with DNS checks

### ⚙️ Configuration (3 packages)
- **pydantic** - Request/response validation using Python types
- **pydantic-settings** - Configuration management from environment
- **python-dotenv** - Load variables from .env file

### 📝 Monitoring (2 packages)
- **python-json-logger** - Structured JSON logging
- **structlog** - Advanced structured logging

### 📡 Network (1 package)
- **requests** - Making HTTP requests to external APIs

### 🚀 Production (1 package)
- **gunicorn** - Production-grade WSGI server

### 🧪 Testing (3 packages)
- **pytest** - Test framework
- **pytest-asyncio** - Async test support
- **httpx** - Async HTTP client for testing APIs

### 🎨 Code Quality (2 packages)
- **black** - Code formatter for consistency
- **flake8** - Code linter for style violations

---

## 🧮 Total Package Count

| Category | Count |
|----------|-------|
| Production Core | 16 packages |
| Development Tools | 5 packages |
| **TOTAL** | **21 packages** |

---

## 🚀 Quick Install

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "fastapi|sqlalchemy|pydantic|uvicorn"
```

---

## 🗂️ What Each Package Does

### Core Application
```
User Request 
    ↓
uvicorn (ASGI Server)
    ↓
FastAPI (Web Framework)
    ↓
pydantic (Validation)
    ↓
Application Logic
    ↓
SQLAlchemy (ORM)
    ↓
psycopg2 (PostgreSQL Driver)
    ↓
Neon Database
```

### Security Flow
```
User Login
    ↓
argon2-cffi (Hash Password)
    ↓
python-jose (Create JWT)
    ↓
pyjwt (Validate Token)
    ↓
Authorized Request
```

### Configuration Flow
```
.env File
    ↓
python-dotenv (Load Variables)
    ↓
pydantic-settings (Validate Settings)
    ↓
Application Config
```

---

## 📋 Version Strategy

- **Fixed Versions (==)**: Ensures reproducible deployments
- **All versions tested** with current codebase
- **No breaking changes** expected with these versions

---

## ⚠️ Important Notes

### NOT Included
- ❌ No OpenAI / Anthropic APIs
- ❌ No Google AI
- ❌ No paid LLM services
- ❌ No PyTorch (yet) - will be added when ML features needed
- ❌ No Transformers (yet) - will be added for local model inference

### Philosophy
✅ **Local/Self-Hosted First**
✅ **Open Source Focused**
✅ **Production Ready**
✅ **Secure by Default**

---

## 🔄 Update Instructions

To update dependencies safely:
```bash
# Check for outdated packages
pip list --outdated

# Update pip itself
pip install --upgrade pip

# Install all dependencies fresh
pip install --upgrade -r requirements.txt
```

---

## 📚 Documentation Links

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **PostgreSQL**: https://www.postgresql.org/
- **JWT**: https://jwt.io/
- **Argon2**: https://argon2-cffi.readthedocs.io/

---

## ✅ System Requirements

- Python 3.10+
- PostgreSQL 12+ (or Neon)
- pip (Python package manager)

---

**Last Updated:** 2026-04-16  
**Status:** Production Ready ✅
