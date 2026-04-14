import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import streamlit as st
import logging
import zipfile
import pandas as pd
import shutil
import pdfplumber
#import spacy
from typing import List, Tuple, Optional

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
logging.basicConfig(level=logging.INFO)

class ATSBackend:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.resume_text = None
        self.job_description = None
        

    def extract_text_from_pdf(self, uploaded_file):
        """Extracts text from an uploaded PDF file or file path."""
        try:
            # Accept both file path (str) and file-like object
            if isinstance(uploaded_file, str):
                pdf_file = open(uploaded_file, "rb")
                close_after = True
            else:
                pdf_file = uploaded_file
                close_after = False
            with pdfplumber.open(pdf_file) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            if close_after:
                pdf_file.close()
            self.resume_text = text
            logging.info("Text extracted successfully from PDF.")
            return text
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {str(e)}")
            raise

    def set_job_description(self, jd):
        """Set the job description."""
        self.job_description = jd

    def generate_prompt(self, prompt_template, max_retries=3):
        """Generate a response from the model based on the provided prompt template."""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt_template,
                    generation_config={
                        "temperature": 0.5,  # Lower temperature for less randomness
                        "max_output_tokens": 1024,
                    }
                )
                return response.text
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception("Failed to generate content after multiple attempts. Please try again.") from e
                import time
                time.sleep(2 ** attempt)  # Exponential backoff

    def get_resume_analysis(self):
        """Get detailed resume analysis."""
        prompt = f"""
        You are an experienced Technical Human Resource Manager. Review the provided 
        resume against the job description and provide a detailed evaluation in the 
        following format:

        **Match Score:**
        [Provide match percentage and 2-3 sentence explanation of overall fit]

        **Skills Analysis:**
        Present Skills:
        [List key matching skills found in resume]

        Missing Skills:
        [List important skills from JD that are missing]

        Additional Skills:
        [List relevant extra skills the candidate has]

        Key Strengths:
        [List 3-4 main strengths]

        Areas for Improvement:
        [List 2-3 areas needing enhancement]

        **Recommendations:**
        Provide 3-4 specific, actionable recommendations

        Resume: {self.resume_text}
        Job Description: {self.job_description}
        """
        return self.generate_prompt(prompt)

    # ... rest of class omitted for brevity (kept identical to original) ...


class BulkATSBackend:
    def __init__(self, ats_backend: ATSBackend):
        self.resumes_data: List[Tuple[str, str]] = []  # Store extracted resume texts
        self.ats_backend = ats_backend  

    def extract_text_from_zip(self, uploaded_file):
        """Extract text from uploaded ZIP file containing resumes."""
        temp_dir = "temp_resumes"
        os.makedirs(temp_dir, exist_ok=True)

        try:
            if not zipfile.is_zipfile(uploaded_file):
                raise ValueError("Invalid ZIP file format")

            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            for filename in os.listdir(temp_dir):
                sanitized_filename = os.path.basename(filename)  # Sanitize filename
                file_path = os.path.join(temp_dir, sanitized_filename)
                if sanitized_filename.endswith('.pdf'):
                    try:
                        # Use ATSBackend's extract_text_from_pdf
                        text = self.ats_backend.extract_text_from_pdf(file_path)
                        if text:  # Check if text is not empty
                            self.resumes_data.append((sanitized_filename, text))  # Store extracted text as a tuple
                            logging.info(f"Successfully extracted text from {sanitized_filename}.")
                        else:
                            logging.warning(f"No text extracted from {sanitized_filename}. Skipping.")
                    except Exception as e:
                        logging.error(f"Error processing PDF {sanitized_filename}: {e}")

        finally:
            # Guaranteed cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)  # Add ignore_errors

    def process_bulk_resumes(self, job_description):
        """Processes all uploaded resumes against the job description and determine suitability."""
        if not self.resumes_data:
            logging.error("No resumes to process.")
            raise ValueError("No resumes to process.")

        logging.info(f"Processing {len(self.resumes_data)} resumes.")  # Log the number of resumes being processed

        results = []  # Initialize an empty list to hold results
        for filename, resume_text in self.resumes_data:
            try:
                # Get the analysis using the ATSBackend's analyze_resume method, passing is_bulk=True
                analysis = self.ats_backend.analyze_resume(resume_text, job_description, is_bulk=True)

                # --- New logic: determine suitability based on match percentage ---
                match_str = analysis.get("Match Percentage", "0")
                try:
                    match_score = float(match_str.replace("%", "").strip())
                except Exception:
                    match_score = 0

                suitability = "Suitable" if match_score > 70 else "Not Suitable"
                analysis["Suitability"] = suitability
                
                results.append({
                    "filename": filename,
                    "Suitability": analysis.get("Suitability", "N/A"),
                    "Match Percentage": analysis.get("Match Percentage", "N/A"),
                    "Key Strengths": analysis.get("Key Strengths", ""),  # Use the string directly
                    "Areas for Improvement": analysis.get("Areas for Improvement", "")  # Use the string directly
                })

            except Exception as e:
                logging.exception(f"Error analyzing resume {filename}: {e}")
                results.append({
                    "filename": filename,
                    "Suitability": "Error",
                    "Match Percentage": "N/A",
                    "Key Strengths": "",
                    "Areas for Improvement": f"Error during processing: {e}"
                })

        return results  # Return the list of dictionaries

    def sanitize_input(self, text: str) -> str:
        """Sanitize input text to remove problematic characters."""
        # Example sanitization: replace special characters with HTML entities
        return text.replace("&", "&").replace("<", "<").replace(">", ">")

    def _get_llm_response(self, prompt: str) -> str:
        """Helper function to get the LLM response. Abstract this out so you can swap implementations."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment.")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("Gemini 2.0 Flash")  

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"LLM generation failed: {e}")  # Log LLM failures specifically
            raise  # Re-raise so analyze_resume handles it

    def clear_resumes(self):
        """Clear stored resumes data."""
        self.resumes_data = []
