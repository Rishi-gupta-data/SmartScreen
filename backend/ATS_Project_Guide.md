
# Intelligent Applicant Tracking System (ATS) - Tech Stack and Deployment Guide

## Tech Stack Overview

- **Backend**: Python (Flask)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript (Optional: React/Angular)
- **Libraries/Tools**:
  - **NLP**: spaCy, Hugging Face Transformers
  - **Parsing**: PyPDF2 (for PDF files), python-docx (for DOCX files)
  - **Data Analysis**: Pandas, NumPy
  - **Web Scraping**: BeautifulSoup, Scrapy (Optional for scraping job data)
  - **Authentication**: Flask-Login, JWT (for user sessions)
  - **Deployment**: Docker, AWS/GCP for cloud hosting

---

## Step 1: **Set Up the Backend (Flask)**

### 1.1 Install Required Libraries

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv ats-env
   source ats-env/bin/activate  # On Windows: ats-env\Scripts\activate
   ```

2. **Install Flask**:
   ```bash
   pip install Flask
   ```

3. **Install Other Required Libraries**:
   ```bash
   pip install pandas spacy transformers flask-mysqldb Flask-Login PyPDF2 python-docx
   ```

### 1.2 Flask Project Structure

Create the project structure as follows:

```
/ats
    /static
    /templates
    /models
    app.py
    config.py
    requirements.txt
```

### 1.3 Flask App Basic Setup

**app.py**:
```python
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin
import MySQLdb

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Step 2: **Set Up the Database (MySQL)**

### 2.1 Install MySQL

1. **Install MySQL** on your local machine or use a cloud database service like AWS RDS or GCP.

2. **Create a Database** for your ATS:
   ```sql
   CREATE DATABASE ats_db;
   ```

3. **Create Tables for Candidates, Job Descriptions, Applications, etc.**

Example table for `candidates`:
```sql
CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    resume TEXT,
    skills TEXT
);
```

### 2.2 Configure Database Connection in Flask

**config.py**:
```python
import os

class Config:
    MYSQL_HOST = 'localhost'  # or your cloud DB host
    MYSQL_USER = 'root'  # your DB username
    MYSQL_PASSWORD = 'password'  # your DB password
    MYSQL_DB = 'ats_db'

app.config.from_object(Config)

mysql = MySQLdb.connect(host=app.config['MYSQL_HOST'],
                         user=app.config['MYSQL_USER'],
                         password=app.config['MYSQL_PASSWORD'],
                         database=app.config['MYSQL_DB'])
```

---

## Step 3: **Set Up Resume and Job Description Parsing**

### 3.1 Install Parsing Libraries

```bash
pip install PyPDF2 python-docx
```

### 3.2 Resume Parsing Example (PDF and DOCX)

```python
from PyPDF2 import PdfReader
import docx

# PDF Parsing
def parse_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# DOCX Parsing
def parse_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text
```

### 3.3 Job Description Parsing (Text-Based Matching)

Using NLP models from **spaCy** or **Transformers** (e.g., BERT) for semantic matching between job descriptions and resumes.

```python
import spacy

nlp = spacy.load("en_core_web_md")

def match_resume_to_job_desc(resume_text, job_desc_text):
    resume_doc = nlp(resume_text)
    job_desc_doc = nlp(job_desc_text)
    
    # Example: Using cosine similarity for matching
    similarity = resume_doc.similarity(job_desc_doc)
    return similarity
```

---

## Step 4: **Frontend (HTML, CSS, JavaScript)**

### 4.1 Basic Flask HTML Template

Create a basic HTML template in the `/templates` folder to display job listings, candidate profiles, and other features.

Example: `index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ATS - Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Welcome to the ATS</h1>
    <p>View job listings and applications.</p>
</body>
</html>
```

### 4.2 Styling with CSS

In `/static/style.css`, add basic styles for the page.

```css
body {
    font-family: Arial, sans-serif;
}

h1 {
    color: #333;
}
```

---

## Step 5: **Deploy the Application**

### 5.1 Create a Dockerfile for Deployment

Create a **Dockerfile** to containerize your Flask application for deployment:

```Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

### 5.2 Build and Run the Docker Image

1. Build the Docker image:
   ```bash
   docker build -t ats-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 ats-app
   ```

### 5.3 Deploy to AWS/GCP

Use AWS Elastic Beanstalk or Google App Engine to deploy your Dockerized Flask app to the cloud.

1. **AWS Elastic Beanstalk**: Follow the [AWS docs](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html).
2. **Google App Engine**: Follow the [Google docs](https://cloud.google.com/appengine/docs).

---

## Step 6: **Test and Improve the System**

### 6.1 Test All Features

- Ensure job parsing, resume parsing, and candidate matching are working as expected.
- Perform integration testing for the job description and resume matching logic.

### 6.2 Improve Based on Feedback

- Implement more advanced NLP techniques such as **Named Entity Recognition (NER)** for extracting candidate skills, experiences, etc.
- Add machine learning models for better candidate ranking.

---

## Conclusion

This guide covers the key steps to set up your **ATS project** with **Flask**, **MySQL**, and **NLP-based resume parsing**. You can enhance and optimize this project with additional features such as machine learning-powered candidate ranking, interactive frontend, and advanced job matching algorithms.

Happy coding!
