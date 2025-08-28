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

    def get_percentage_match(self):
        """Get ATS percentage match analysis."""
        prompt = f"""
        You are a skilled ATS (Applicant Tracking System) scanner. Evaluate the resume 
        against the job description and provide a detailed analysis in the following format:

        **Match Analysis:**
        Overall Match: [XX%]
        [2-3 sentences explaining the match percentage]

        **Keyword Analysis:**
        Found Keywords:
        [List important keywords found in resume]

        Missing Keywords:
        [List important keywords from JD that are missing]

        **Final Assessment:**
        [2-3 sentences with final thoughts and key recommendations]

        Resume: {self.resume_text}
        Job Description: {self.job_description}
        """
        return self.generate_prompt(prompt)

    def get_quick_analysis(self):
        """Get quick ATS analysis"""
        try:
            prompt = f"""
            Act as an experienced ATS (Applicant Tracking System) with expertise in tech field, 
            software engineering, data science, and data analysis. Evaluate the resume against 
            the job description and provide a detailed analysis in the following format:

            **Match Score:**
            [Provide a percentage match and 1-2 sentences explaining the overall compatibility]

            **Skills Analysis:**
            Present Skills:
            [List the key skills found in the resume that match the job requirements]

            Missing Skills:
            [List important skills from the job description that are not found in the resume]

            Additional Skills:
            [List any extra relevant skills the candidate has]

            **Profile Summary:**
            [2-3 sentences summarizing the candidate's profile and key qualifications]

            Strengths:
            [List 3-4 key strengths based on the resume]

            Areas for Improvement:
            [List 2-3 areas where the candidate could improve]

            **Recommendations:**
            [Provide 3-4 specific recommendations for improving the resume]

            Resume:
            {self.resume_text}

            Job Description:
            {self.job_description}
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error in quick analysis: {str(e)}")

    def get_detailed_review(self):
        """Get detailed resume review"""
        try:
            prompt = f"""
            You are an experienced Technical Human Resource Manager, your task is to
            review the provided resume against the job description. Please share your
            professional evaluation on whether the candidate's profile aligns with
            the role. Highlight the strengths and weaknesses of the applicant in
            relation to the specified job requirements.

            Please structure your response in the following format:
            **Overall Match Assessment:**
            [Your assessment here]

            **Key Strengths:**
            [List of strengths]

            **Areas for Improvement:**
            [List of areas for improvement]

            **Technical Skills Alignment:**
            [Your evaluation here]

            **Recommendations:**
            [Your recommendations here]

            Resume:
            {self.resume_text}

            Job Description:
            {self.job_description}
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error in detailed review: {str(e)}")

    def get_match_score(self):
        """Get resume match score"""
        try:
            prompt = f"""
            You are a skilled ATS (Applicant Tracking System) scanner with a deep
            understanding of data science and ATS functionality. Evaluate the resume
            against the provided job description and provide a detailed analysis.

            Please provide your response in the following format:
            **Match Percentage:** [X%]
            **Missing Keywords:** [List them]
            **Found Keywords:** [List them]
            **Key Strengths:** [Brief points]
            **Improvement Areas:** [Brief points]
            **Final Thoughts:** [Brief conclusion]

            Resume:
            {self.resume_text}

            Job Description:
            {self.job_description}
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error in match score calculation: {str(e)}")

    def save_analysis(self, analysis_data):
        """Save analysis results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_analysis_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(analysis_data, f, indent=2)
            return filename
        except Exception as e:
            raise Exception(f"Error saving analysis: {str(e)}")

    def get_formatting_suggestions(self):
        """Get resume formatting recommendations"""
        try:
            prompt = f"""
            As an ATS expert, analyze the resume formatting and provide recommendations in the following format:

            **Formatting Analysis:**
            [Overall assessment of resume formatting]

            **Key Recommendations:**
            **File Format:**
            [Assess PDF formatting and compatibility]

            **Layout:**
            [Analyze spacing, sections, and organization]

            **Headers & Sections:**
            [Review section headers and hierarchy]

            **Fonts & Styling:**
            [Evaluate font choices and text styling]

            **Optimization Tips:**
            [List 3-4 specific formatting improvements]

            Resume: {self.resume_text}
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error in formatting analysis: {str(e)}")

    def get_keyword_optimization(self):
        """Get keyword optimization suggestions"""
        try:
            prompt = f"""
            As an ATS expert, analyze the resume for keyword optimization and provide suggestions in the following format:

            **Keyword Optimization:**
            [Overall keyword optimization score]

            **Industry-Specific Keywords:**
            **Current Keywords:**
            [List current industry keywords found]

            **Recommended Keywords:**
            [List recommended keywords based on job description]

            **Placement Suggestions:**
            [Specific suggestions for keyword placement]

            Resume: {self.resume_text}
            Job Description: {self.job_description}
            """
            
            response = self.model.generate_content(prompt)
            formatted_response = self.format_response(response.text)  # Format the response
            return formatted_response
        except Exception as e:
            raise Exception(f"Error in keyword optimization: {str(e)}")

    def get_interactive_suggestions(self):
        """Get interactive suggestions with specific locations in the resume."""
        try:
            # Prompt the LLM to return JSON
            prompt = f"""
            As an ATS expert, analyze the resume and job description and provide up to 5 most important suggestions for improvement. Return the response as a JSON array of objects. Each object should have the following keys:

            * section: The name of the section in the resume where the suggestion applies.
            * line_content: The original text from the resume that the suggestion refers to.
            * suggestion: The suggested change to the text.
            * reason: A brief explanation of why the change is recommended.

            Here's an example of the JSON format:
            [
                {{
                    "section": "Skills",
                    "line_content": "Proficient in Python",
                    "suggestion": "Quantify your Python skills. For example, 'Developed Python scripts for data analysis pipelines that processed 1TB of data daily.'",
                    "reason": "Quantifying your skills makes them more impactful and easier to assess."
                }}
            ]

            Resume: {self.resume_text}
            Job Description: {self.job_description}
            """

            response = self.model.generate_content(prompt)
            logging.info(f"Raw response from model: {response.text}")

            try:
                suggestions = json.loads(response.text)  # Load response as JSON
            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode JSON from LLM: {e}")
                raise Exception("The LLM returned an invalid JSON format. Please try again.")

            # Validate the structure of the suggestions
            if not isinstance(suggestions, list):
                raise Exception("The LLM did not return a JSON array.")
            for suggestion in suggestions:
                if not isinstance(suggestion, dict):
                    raise Exception("Each suggestion must be a JSON object.")
                if not all(key in suggestion for key in ["section", "line_content", "suggestion", "reason"]):
                    raise Exception("Each suggestion must have 'section', 'line_content', 'suggestion', and 'reason' keys.")
            return {"suggestions": suggestions}

        except Exception as e:
            logging.error(f"Error in interactive suggestions: {str(e)}")
            raise

    def suggest_resume_template(self):
        """Suggest resume templates based on job analysis"""
        prompt = f"""
        As an ATS expert, analyze the job description and current resume to suggest 
        the most appropriate resume template. Provide response in the following format:

        **Recommended Template:**
        [Template name and brief explanation why it's suitable]

        **Template Details:**
        **Structure:**
        [Recommended sections order and layout]

        **Key Features:**
        [List of important template features]

        **Visual Elements:**
        [Recommendations for visual presentation]

        **Customization Tips:**
        [3-4 specific tips to customize the template]

        Job Description: {self.job_description}
        Current Resume Format: {self.resume_text}
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def format_response(self, response_text):
        """Format the response text for better readability."""
        # Example: Remove unnecessary whitespace or newlines
        return "\n".join(line.strip() for line in response_text.splitlines() if line.strip())

    def validate_input(self):
        """Validate the resume and job description inputs."""
        if not self.resume_text:
            raise ValueError("Resume text cannot be empty.")
        if not self.job_description:
            raise ValueError("Job description cannot be empty.")
        if len(self.resume_text.strip()) < 50:
            raise ValueError("Resume text appears too short to be valid.")
        if len(self.job_description.strip()) < 50:
            raise ValueError("Job description appears too short to be valid.")

    def determine_suitability(self, match_score, thresholds=(75, 50)):
        """Determine if the candidate is suitable based on the match score."""
        if match_score >= thresholds[0]:  # Threshold for suitability
            return "Suitable"
        elif match_score >= thresholds[1]:
            return "Potentially Suitable"
        else:
            return "Not Suitable"

    def analyze_resume(self, resume_text: str, job_description: str, is_bulk: bool = False) -> dict:
        """Analyzes a single resume against the job description using AI."""
        try:
            # Ensure resume_text is a string before proceeding
            if not isinstance(resume_text, str):
                logging.error(f"Invalid resume_text type: {type(resume_text)}. Expected str.")
                raise ValueError("Invalid resume_text type. Expected a string.")

            logging.info(f"Analyzing resume: {resume_text[:500]}")  

            # Sanitize inputs to avoid issues with special characters
            resume_text = self.sanitize_input(resume_text)
            job_description = self.sanitize_input(job_description)

            # Generate the prompt for the AI model
            if is_bulk:
                prompt = self.generate_bulk_analysis_prompt(resume_text, job_description)
            else:
                prompt = f"""You are an expert recruiter tasked with determining if a candidate is suitable for a position.
                You are given a job description and a resume.
                Based on the resume and the job description, provide a detailed suitability assessment. Return the response as a JSON object.
                The JSON object should contain the following keys:
                * match_percentage: A string representing the percentage match between the resume and the job description (0-100).
                * found_keywords: A list of keywords found in the resume.
                * missing_keywords: A list of essential keywords missing from the resume.
                * key_strengths: A list of the main strengths of the candidate.
                * areas_for_improvement: A list of key areas where the resume could be enhanced.
                * resume_formatting_tips: A list of specific suggestions for making the resume more ATS-friendly.
                Job Description: {job_description}
                Resume: {resume_text}"""

            # Get the LLM response
            response_text = self._get_llm_response(prompt)

            # Log the raw response
            logging.info(f"Raw LLM Response: {response_text}")

            if not response_text:
                logging.error("Received an empty response from the model.")
                raise ValueError("Received an empty response from the model.")

            # Parse the response based on the type of analysis
            if is_bulk:
                return self.parse_bulk_analysis_response(response_text)
            else:
                return self.parse_individual_analysis_response(response_text)

        except Exception as e:
            logging.exception(f"Error during analyze_resume: {e}")
            raise

    def shorten_text(self, text: str, max_length: int = 150) -> str:
        """Shortens the text to a specified maximum length."""
        if len(text) > max_length:
            return text[:max_length] + "..."  # Truncate and add ellipsis
        return text

    def sanitize_input(self, text: str) -> str:
        """Sanitize input text to remove problematic characters."""
        return text.replace("&", "&").replace("<", "<").replace(">", ">")

    def clean_json_response(self, response_text: str) -> str:
        """Cleans the JSON response text to ensure it is valid JSON."""
        # Remove any extraneous characters before and after the JSON object
        start = response_text.find("{")
        end = response_text.rfind("}")
        if start != -1 and end != -1:
            return response_text[start:end + 1]
        return "{}"  # Return an empty JSON object if no valid JSON found

    def generate_bulk_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        """Generates a prompt for bulk resume analysis."""
        return f"""Based on a careful comparison of the job description and the resume, please provide a concise evaluation. Your evaluation should include:

1. **Suitability Assessment:** A definitive statement declaring the candidate as either "Suitable" or "Not Suitable" for the role. Base this decision on the overall alignment of skills, experience, and qualifications.

2. **Key Strengths:** Identify 2-3 of the candidate's strongest qualifications, skills, or experiences that directly align with the requirements outlined in the job description. Explain briefly how each strength maps to the job description.

3. **Areas for Improvement:** Identify 1-2 potential areas where the candidate's resume may be lacking or where their experience doesn't fully align with the job description's requirements.

4. **Match Percentage:** Estimate the overall percentage match between the candidate's qualifications and the job requirements. Provide a single percentage value (e.g., "75%").

Your response should be formatted as follows:

**Suitability Assessment:** [Suitable/Not Suitable]
**Key Strengths:**
- [Strength 1]: [Explanation of alignment]
- [Strength 2]: [Explanation of alignment]
- [Strength 3]: [Explanation of alignment]

**Areas for Improvement:**
- [Area 1]
- [Area 2]

**Match Percentage:** [Percentage]%

Please provide an objective and data-driven assessment, focusing on concrete skills and experience rather than subjective interpretations.

Here's the job description:
{job_description}

And here's the candidate's resume:
{resume_text}
"""

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
            raise  
    def parse_bulk_analysis_response(self, response_text: str) -> dict:
        """Parses the text response from the LLM based on the bulk analysis prompt."""
        try:
            # Split the response into sections
            sections = response_text.split('\n\n')

           
            analysis = {}

            # Extract Suitability Assessment
            for section in sections:
                if section.startswith("**Suitability Assessment:**"):
                    analysis["Suitability"] = section.split('**Suitability Assessment:**')[1].strip()
                    break
            else:
                analysis["Suitability"] = "N/A"  # If not found

            # Extract Key Strengths
            analysis["Key Strengths"] = []
            for section in sections:
                if section.startswith("**Key Strengths:**"):
                    strengths = section.split('**Key Strengths:**')[1].strip().split('\n- ')
                   
                    if strengths and strengths[0] == '':
                        strengths.pop(0)  # This is crucial for avoiding the extra empty element!
                    analysis["Key Strengths"] = [s.strip() for s in strengths]  # Store as a list of strings
                    break
            else:
                analysis["Key Strengths"] = []  # If not found

            # Extract Areas for Improvement
            analysis["Areas for Improvement"] = []
            for section in sections:
                if section.startswith("**Areas for Improvement:**"):
                    improvements = section.split('**Areas for Improvement:**')[1].strip().split('\n- ')
                    # Remove the first empty element if it exists
                    if improvements and improvements[0] == '':
                        improvements.pop(0)  # This is crucial for avoiding the extra empty element!
                    analysis["Areas for Improvement"] = [i.strip() for i in improvements]  # Store as a list of strings
                    break
            else:
                analysis["Areas for Improvement"] = []  # If not found

            # Extract Match Percentage
            for section in sections:
                if section.startswith("**Match Percentage:**"):
                    match_percentage = section.split('**Match Percentage:**')[1].strip()
                    analysis["Match Percentage"] = match_percentage.replace('%', '') if match_percentage else "N/A"
                    break
            else:
                analysis["Match Percentage"] = "N/A"  # If not found

            return analysis

        except Exception as e:
            logging.error(f"Error parsing LLM response: {e}")
            # Log the raw response for debugging
            logging.debug(f"Raw response from LLM: {response_text}")
            raise ValueError(f"Could not parse LLM response: {e}")

    def parse_individual_analysis_response(self, response_text: str) -> dict:
        """Parses the JSON response text from the LLM based on the individual analysis prompt."""
        try:
            # Clean the response to remove any extraneous characters
            cleaned_response = self.clean_json_response(response_text)

            # Attempt to parse the cleaned response
            analysis = json.loads(cleaned_response)

            # Check for expected keys in the response
            expected_keys = ['match_percentage', 'found_keywords', 'missing_keywords', 'key_strengths', 'areas_for_improvement', 'resume_formatting_tips']
            for key in expected_keys:
                if key not in analysis:
                    logging.error(f"Response is missing expected key: {key}")
                    raise ValueError(f"Response is missing required key: {key}")

            # Format the output for better readability
            formatted_analysis = {
                "Match Percentage": analysis["match_percentage"],
                "Found Keywords": analysis["found_keywords"],
                "Missing Keywords": analysis["missing_keywords"],
                "Key Strengths": analysis["key_strengths"],
                "Areas for Improvement": analysis["areas_for_improvement"],
                "Resume Formatting & Optimization Tips": analysis["resume_formatting_tips"]
            }

            return formatted_analysis  # Return the formatted analysis

        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON response from LLM: {e}, Raw Response: {cleaned_response}")
            raise ValueError(f"Error decoding JSON response: {e}")

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
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Or the model you prefer

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"LLM generation failed: {e}")  # Log LLM failures specifically
            raise  # Re-raise so analyze_resume handles it

    def clear_resumes(self):
        """Clear stored resumes data."""
        self.resumes_data = []
