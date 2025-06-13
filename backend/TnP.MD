# Steps to Create a Separate Portal for Bulk Resume Matching

To keep the bulk resume matching module independent of individual resume parsing and optimization, follow these steps:

## 1. Create a Separate Backend API Module

Set up a new Flask API endpoint specifically for bulk resume processing.

Implement separate API routes such as:

- `/upload_bulk_resumes` → To handle bulk resume uploads.
- `/process_bulk_resumes` → To process and classify resumes.
- `/download_results` → To provide classification reports.

## 2. Develop a Dedicated Frontend Portal

Create a separate React.js frontend for recruiters.

Features should include:

- A dashboard for bulk resume uploads.
- A section for job description input.
- A table listing classified resumes.
- A download button for the results.

## 3. Implement Independent Database Tables

Use separate tables in PostgreSQL/MongoDB for bulk resume processing.

Structure example:

- `bulk_resumes`: Stores raw resume data.
- `bulk_results`: Stores classification results.

## 4. Ensure Modular Codebase

Keep resume parsing logic separate for individual and bulk processing.

Maintain different ML models for personalized keyword optimization and bulk classification.

Separate logs and analytics for both functionalities.

## 5. Deploy on Different Endpoints

Host the individual resume parser at `ats.example.com/individual`.

Host the bulk resume matcher at `ats.example.com/recruiter`.

Ensure both portals have distinct UI designs and access controls.

## How to Use

### For Individual Applicants:

- Upload a resume.
- Get keyword optimization suggestions.
- Download an improved version of the resume.

### For Recruiters & Training Committees:

- Upload a job description.
- Upload resumes in bulk.
- The system will classify resumes into "Suitable" or "Not Suitable."
- Download reports for further hiring decisions.