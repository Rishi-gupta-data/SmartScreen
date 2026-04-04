# Supabase Database Schema Architecture

For the **SmartScreen ATS** system, we use Supabase (PostgreSQL) to store structured candidate data and job descriptions.

## 🗄️ Database Schema

### 1. `candidates` Table
Stores extracted resume data and their semantic embeddings.

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | Primary Key (Auto-generated) |
| `filename` | `TEXT` | Original filename of the uploaded resume |
| `extracted_text` | `TEXT` | Raw text extracted from the file |
| `embedding` | `BYTEA` | Binary representation of the vector (from `all-MiniLM-L6-v2`) |
| `created_at` | `TIMESTAMPTZ` | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | Last update timestamp |

### 2. `jobs` Table
Stores job descriptions and their semantic embeddings.

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | Primary Key (Auto-generated) |
| `title` | `TEXT` | Job title |
| `description` | `TEXT` | Detailed job description |
| `embedding` | `BYTEA` | Binary representation of the vector |
| `created_at` | `TIMESTAMPTZ` | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | Last update timestamp |

---

## 🚀 Supabase Setup SQL

Run the following SQL in your **Supabase SQL Editor** to create the tables manually (or the system will automatically create them via `scripts/init_db.py` if the connection string is provided).

```sql
-- Create candidates table
CREATE TABLE candidates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    extracted_text TEXT NOT NULL,
    embedding BYTEA,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create jobs table
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    embedding BYTEA,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable uuid-ossp if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## 🛠️ Connection String Configuration

To connect the Flask backend to Supabase, set your `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgresql://postgres:[YOUR_PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres"
```

The system will use this connection to perform all database operations.
