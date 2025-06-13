

# Software Requirements Specification (SRS) Document

## Overview
This document outlines the Software Requirements Specification (SRS) for the Applicant Tracking System (ATS). The ATS is designed to bridge the gap between candidates and recruiters by automating the recruitment process. It includes functionalities for parsing job descriptions, filtering candidates, analyzing resumes, and providing suggestions for improvement.

## 1. Introduction

### 1.1 Purpose
The purpose of this SRS document is to define the requirements for an ATS that serves as a bridge between candidates and recruiters. The system will:
- Parse job descriptions
- Extract relevant skills
- Filter candidates
- Analyze resumes
- Suggest improvements to both recruiters and candidates

### 1.2 Scope
The ATS will assist recruiters by:
- Analyzing job descriptions
- Filtering candidates based on skills, projects, experience, and keywords
- Generating ranked lists of candidates for specific job roles

For candidates, the system will:
- Provide resume-building tools
- Analyze resumes for keyword matches
- Suggest more efficient keywords for better visibility

### 1.3 Definitions, Acronyms, and Abbreviations
- **ATS:** Applicant Tracking System
- **JD:** Job Description
- **CV:** Curriculum Vitae
- **Keyword:** Specific terms or phrases used to filter and match candidates to job descriptions.

### 1.4 Overview
This document outlines the functional and non-functional requirements for developing the ATS system. It covers:
- Job description parsing
- Candidate searching and filtering using a pre-existing database
- Resume analysis
- Keyword suggestions for both job descriptions and resumes

---

## 2. Overall Description

### 2.1 Product Perspective
The ATS system will integrate with existing job portals and act as an intermediary tool for recruiters and candidates. It will offer:
- Parsing
- Filtering
- Ranking functionalities for recruiters
- Resume-building and analysis tools for candidates

### 2.2 Product Functions
The system will provide the following functionalities:
- Job description parsing and analysis
- Skill extraction from job descriptions
- Candidate filtering based on keywords, projects, and experience
- Ranking candidates according to predefined criteria
- Resume building tool for candidates
- Resume and CV analysis based on matching keywords
- Keyword suggestion for both job descriptions and resumes

### 2.3 User Characteristics
- **Recruiters:** Use the system to post jobs, parse job descriptions, and search/filter candidates.
- **Candidates:** Use the system to create and optimize resumes/CVs and apply for jobs.
- **Administrators:** Manage the system, users, and ensure smooth functioning.

### 2.4 Assumptions and Dependencies
- The system assumes that job descriptions follow a standard format for effective parsing.
- The system will integrate with third-party job boards for importing job descriptions.
- The resume builder will assume common resume formats (PDF, DOCX).

---

## 3. System Features

### 3.1 Job Description Parsing
- **Description:** The system will parse job descriptions to extract key information, including required skills, job roles, experience, and qualifications.
- **Inputs:** Job description text.
- **Outputs:** Parsed list of skills, qualifications, job title, and other key job details.
- **Functional Requirements:**
  - F1: The system must parse job descriptions using natural language processing (NLP).
  - F2: The system must extract key skills from the parsed job description.

### 3.2 Skill Extraction and Analysis
- **Description:** The system will analyze job descriptions and extract a list of relevant skills required for the role.
- **Inputs:** Parsed job description.
- **Outputs:** List of key skills.
- **Functional Requirements:**
  - F3: The system must extract skills from the parsed job description.
  - F4: The system must suggest additional relevant skills if they are missing from the job description.

### 3.3 Candidate Search and Filtering
- **Description:** The system will enable recruiters to search and filter candidates based on multiple criteria such as keywords, experience, projects, and matching job role.
- **Inputs:** Candidate database, search query from recruiter.
- **Outputs:** Filtered list of candidates.
- **Functional Requirements:**
  - F5: The system must allow searching candidates by keywords found in resumes.
  - F6: The system must rank candidates based on their match with the job description.
  - F7: The system must filter candidates by their experience, projects, and job role fit.
  - F8: The system will provide ranking of the candidate on the basis of categories and criteria set by the recruiter.

### 3.4 Resume Builder
- **Description:** A tool for candidates to build and format their resumes based on provided templates.
- **Inputs:** Candidate's personal data, skills, and work experience.
- **Outputs:** Formatted resume (PDF, DOCX).
- **Functional Requirements:**
  - F9: The system must provide an ATS-friendly template for candidates.
  - F10: The system must allow candidates to export their resume in PDF or DOCX format.

### 3.5 Resume and CV Analysis
- **Description:** The system will analyze the candidate's resume for relevant keywords and suggest improvements.
- **Inputs:** Candidate's resume (uploaded or built via the system).
- **Outputs:** Analysis report including matching keywords and suggestions for improvement.
- **Functional Requirements:**
  - F11: The system must analyze resumes for keyword matching against job descriptions.
  - F12: The system must suggest additional relevant keywords for better resume optimization.

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- The system must parse job descriptions and analyze resumes efficiently.
- The search and filtering process should return results promptly.

### 4.2 Security Requirements
- The system must ensure secure data transmission using HTTPS.
- All user data must be encrypted when stored in the database.

### 4.3 Usability Requirements
- The user interface should be intuitive and provide guidance during the resume-building process.
- The system should be accessible via both desktop and mobile devices.

### 4.4 Reliability Requirements
- The system must have a 99.9% uptime guarantee.

### 4.5 Scalability Requirements
- The system must be able to handle at least 1,000 concurrent users without performance degradation.

---

## 5. External Interface Requirements

### 5.1 User Interfaces
- The system will have separate interfaces for recruiters, candidates, and administrators.
- User interfaces will include forms, dashboards, and search tools optimized for ease of use.

### 5.2 Hardware Interfaces
- The system will run on standard web browsers (Chrome, Firefox, etc.) and does not require specific hardware interfaces.

---

## 6. Other Requirements
- **Legal and Compliance Requirements:** The system must comply with data protection regulations such as GDPR and CCPA.

---

## 7. Appendices
- Any additional information such as wireframes, flowcharts, or sample data would be included here.

---

This document provides a clear and structured outline of the requirements for building an ATS system. Would you like to explore or expand on any specific section?

F1 
●	THE SYSTEM WILL SCAN THE JOB DESCRIPTION AND FIND RELEVANT INFORMATION FROM IT
●	IT WILL USE NLP MODELS TO SCAN AND EXTRACT THE INFO
F2
●	THE INFORMATION EXTRACTED FROM F1, IT WILL NOW FIND THE RELEVANT KEYWORDS FOR JOB DESCRIPTION AND RESUME MATCHING

F3
●	FROM F2. IT WILL EXTRACT ONLY SKILLS LIST AND STORE THEM
F4
●	NOW , THE SYSTEM WILL PROVIDE OR SUGGEST SOME RELEVANT SKILLS KEYWORDS FROM OUR PRE EXISTING- DATABASE , FOR THAT PARTICULAR JOB DESCRIPTION IN F1.
F5
●	SEARCHING AND FILTERING OF CANDIDATE.
●	RECRUITER CAN SEARCH CANDIDATE ON  THE BASIS OF HIS/HER KEYWORDS FOUND IN RESUME
F7
●	IF RECRUITER WANTS TO HIRE SOMEONE FOR A PROJECT BASE, THE CAN SEE THE PROJECTS DONE BY THEIR CANDIDATE
●	AND ALSO THEY CAN GET THE VIEW OF THEIR PAST EXPERIENCE.

F8
●	NOW THE SYSTEM WILL CALCULATE THE ATS SCORE AND RANK THEM ON THE BASIS OF CRITERIA SET BY RECRUITER
●	IT WILL ALLOW RECRUITERS TO VIEW THE SORTED AND RANKED LIST OF CANDIDATES AS PER HIS/HER CRITERIA.

F11
●	It will take the scanned and updated resume from the candidate.(F1,F2,F3)
●	THE SYSTEM WILL ANALYSE THE RESUME USING MULTIPLE ML models and it will compare it with the given JD. 
●	SUGGESTION AND IMPROVEMENT IN THE CV ON THE BASIS OF ATS SCORE AND JD REQUIREMENTS .
F12
●	FIRSTLY SYSTEM WILL PROVIDE THE KEYWORDS FOR JD TO RECRUITER (F2)
●	AND THE SYSTEM WILL ALSO GIVE SOME ADDITIONAL KEYWORDS AND ITS RECRUITERS CHOICE TO ADD THEM OR NOT. THIS IS FOR THOSE WHO ARE UNEXPERIENCED IN HR AND RECUTERMENT. 
Here's a detailed breakdown of each feature's purpose, functionality, and working mechanism for the ATS system:

Feature 1 (F1): Job Description Parsing and Relevant Information Extraction
Purpose: To streamline and automate the analysis of job descriptions by extracting critical details such as required skills, experience, job title, and qualifications.
Functionality: The system uses NLP models to parse and identify essential keywords and phrases from job descriptions.
Working:
Input: The recruiter uploads a job description.
Processing: The NLP model scans the text for pre-defined entities (e.g., "skills," "experience," "qualifications").
Output: A structured list containing parsed job information (skills, roles, experience, qualifications) is generated and stored for later comparison against candidate profiles.

Feature 2 (F2): Keyword Extraction for JD and Resume Matching
Purpose: To identify and list the critical skills and keywords for effective matching between job descriptions and resumes.
Functionality: The system isolates relevant keywords from the job description extracted in F1 to enable accurate candidate matching.
Working:
Input: Parsed job description data from F1.
Processing: Using text analysis, the system filters out non-essential terms, focusing on skills and role-specific keywords.
Output: A list of extracted keywords ready for comparison against resumes.

Feature 3 (F3): Skill List Extraction and Storage
Purpose: To create a concise skills list derived from the job description to streamline candidate filtering.
Functionality: The system saves the skills extracted in F2 for further filtering in candidate searches.
Working:
Input: Extracted keywords (skills) from F2.
Processing: The skills are organised into a structured list.
Output: The skill list is stored in the ATS database to assist in later searches and comparisons.

Feature 4 (F4): Skill Suggestion for Job Description Enhancement
Purpose: To suggest additional relevant skills based on the job description to help recruiters improve their job listings.
Functionality: The system compares the job description against a database of relevant skills, suggesting missing but important skills.
Working:
Input: The skill list created in F3.
Processing: The system checks for missing but relevant skills by comparing with a predefined database.
Output: Suggested additional skills are displayed, and recruiters can choose to add them to the job description.

Feature 5 (F5): Candidate Search and Filtering
Purpose: To filter candidates based on resume keywords and relevant experience, making it easier for recruiters to locate suitable candidates.
Functionality: The recruiter can search and filter candidates by specifying desired keywords found in candidate resumes.
Working:
Input: A recruiter's search query containing specific keywords.
Processing: The system scans the stored resume database, identifying candidates whose resumes contain the specified keywords.
Output: A list of candidates filtered by the keywords relevant to the job description.

Feature 7 (F7): Display of Candidate Projects and Experience
Purpose: To provide insights into a candidate's relevant project experience and professional background, especially for project-based roles.
Functionality: Recruiters can view a candidate's project history and experience for more context.
Working:
Input: Recruiter's request for a candidate's project and experience details.
Processing: The system retrieves detailed project history and work experience from the candidate's profile.
Output: An overview of projects and experience is displayed for the recruiter to evaluate fit for the role.

Feature 8 (F8): ATS Score Calculation and Candidate Ranking
Purpose: To rank candidates by an ATS score calculated based on matching criteria set by the recruiter.
Functionality: Candidates are scored and ranked according to how closely their resume matches the job description.
Working:
Input: Job description criteria specified by the recruiter.
Processing: The system compares each resume against the job criteria, calculating a score based on keyword matches, experience, and skill relevance.
Output: Candidates are ranked and sorted by ATS scores, enabling recruiters to prioritize the most qualified candidates.

Feature 11 (F11): Resume Analysis and Improvement Suggestions
Purpose: To provide candidates with actionable feedback to improve their resumes based on ATS scores and job requirements.
Functionality: The system evaluates a candidate's resume against job descriptions and suggests improvements in keywords and formatting to align better with ATS systems.
Working:
Input: Candidate's resume, job description criteria.
Processing: Using ML models, the system checks for keyword density, skill relevance, and formatting to ensure the resume is optimised for ATS.
Output: An analysis report with suggestions for adding or modifying keywords and other resume improvements to increase the candidate's ATS score.

Feature 12 (F12): Additional Keyword Suggestions for Recruiters
Purpose: To assist recruiters, particularly those inexperienced in recruitment, by providing suggested keywords for job descriptions.
Functionality: The system generates an initial keyword list based on job requirements and suggests additional terms that can enhance search accuracy.
Working:
Input: Parsed job description.
Processing: The system identifies commonly used and effective keywords related to the role.
Output: An additional list of recommended keywords for the recruiter to include, with the option to select which to add to the job description.
Each feature works in concert to make the ATS system highly efficient, ensuring both recruiters and candidates benefit from streamlined matching, optimised resume content, and insightful keyword suggestions. Let me know if you need further detail on any feature!

