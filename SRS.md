
# Software Requirements Specification (SRS) for SmartScreen

## Introduction

This document outlines the Software Requirements Specification (SRS) for the SmartScreen application. The purpose of this document is to provide a detailed description of the project's goals, features, and technical requirements.

## The STAR Method: A Framework for Understanding SmartScreen

### Situation

In the current competitive job market, recruiters and hiring managers are inundated with a high volume of resumes for every open position. Manually sifting through these resumes is not only a time-consuming and labor-intensive process, but it is also susceptible to unconscious bias and human error. This can lead to overlooking qualified candidates and making suboptimal hiring decisions. The need for a tool that can automate and enhance the resume screening process is more critical than ever.

### Task

The primary objective of the SmartScreen project is to develop a sophisticated, web-based application that empowers recruiters and hiring managers to screen resumes with greater efficiency and accuracy. The application will provide a suite of tools for analyzing resumes, comparing them against job descriptions, and ranking candidates based on their qualifications. This will enable hiring teams to focus their time and energy on the most promising applicants.

### Action

To accomplish this, we will develop a single-page application (SPA) using the React library. The application will be designed with a clean, intuitive, and user-friendly interface. The core features of the SmartScreen application are detailed below:

*   **Home Page:** The application will feature a welcoming and informative home page that serves as the main entry point for users. This page will provide a brief overview of the application's capabilities and guide users on how to get started with the resume analysis process.

*   **Individual Resume Analysis:** This feature will allow users to perform a detailed analysis of a single resume.
    *   **File Upload:** Users will be able to upload a resume file (in formats such as .pdf, .docx, or .txt) and a corresponding job description.
    *   **Skills Matching:** The application will parse the resume and the job description to identify and compare the skills, keywords, and qualifications.
    *   **Match Score:** A percentage-based match score will be calculated to provide a quick quantitative assessment of the candidate's suitability for the role.
    *   **Detailed Report:** A comprehensive report will be generated, highlighting the matching and missing skills, and providing a side-by-side comparison of the resume and the job description.

*   **Bulk Resume Analysis:** This feature is designed to streamline the screening of multiple resumes for a single job opening.
    *   **Multiple File Upload:** Users will be able to upload a batch of resumes (e.g., in a .zip file) for a specific job description.
    *   **Candidate Ranking:** The application will analyze all the resumes in the batch and rank them based on their match score, from highest to lowest.
    *   **Top Candidate Identification:** This will allow recruiters to quickly identify a shortlist of the most qualified candidates for further evaluation.

*   **Resume Analysis View:** This dedicated view will present the results of the analysis in a clear, concise, and visually appealing manner. It will use data visualization techniques to make the information easy to understand and interpret.

The frontend application will communicate with a backend API, as defined in `src/services/api.js`, which will be responsible for the heavy lifting of parsing resumes, performing the analysis, and returning the results.

### Result

The SmartScreen application is expected to deliver significant benefits to recruiters and hiring managers:

*   **Increased Efficiency:** By automating the initial resume screening process, the application will drastically reduce the time and effort required to identify qualified candidates.
*   **Improved Accuracy and Objectivity:** The data-driven approach of the application will help to minimize human bias and ensure that candidates are evaluated based on their skills and qualifications.
*   **Enhanced Decision-Making:** The comprehensive analysis and ranking features will provide hiring teams with the insights they need to make more informed and strategic hiring decisions.
*   **Streamlined Workflow:** The application will integrate seamlessly into the existing recruitment workflow, making the entire process more efficient and effective.

## Current Challenges and Limitations

While the SmartScreen application holds great promise, its success is contingent on overcoming a significant challenge: the **lack of comprehensive data resources** and **limitations of external APIs**.

*   **Limited LLM Model API Access:** Our current reliance on a third-party Large Language Model (LLM) API for resume analysis presents a significant bottleneck. The API has usage limits and costs associated with it, which will not be sustainable as we scale our application. Over-reliance on this external service also limits our ability to customize the analysis to our specific needs and domain.

*   **The Need to Train Our Own NLP Model:** To overcome the limitations of the LLM API and to have more control over the analysis process, it is imperative that we train our own Natural Language Processing (NLP) model. This will allow us to build a solution that is tailored to the nuances of resume and job description parsing. However, training a robust and accurate NLP model requires a substantial amount of high-quality data.

*   **Lack of Data Resources:** We are currently facing a critical shortage of the following resources, which are essential for training our custom NLP model:
    *   **A Large and Diverse Resume Database:** To build robust and unbiased models, we need access to a vast collection of resumes from various industries, job roles, and experience levels. This will help us to account for the different formats, styles, and terminologies used in resumes.
    *   **A Comprehensive Collection of Job Descriptions:** A wide range of job descriptions is essential for training our algorithms to accurately identify the key requirements and qualifications for different roles.
    *   **A Curated Database of Top Skills:** To perform accurate skills matching, we need a well-maintained database of the top skills, keywords, and qualifications for various job families and industries.

Without access to these critical data resources, the development and testing of our custom NLP model will be severely hampered. The models we build may not be generalizable, and the accuracy of the analysis may not meet the required standards. Therefore, acquiring or building these data resources is a top priority for the SmartScreen project.
