# backend/services/resume_parser.py
import os
import logging
import zipfile
import shutil
import pdfplumber
import docx

def parse_resume_file(file_path: str) -> str:
    """
    Parses a resume file (.pdf, .docx) and extracts the text content.

    Args:
        file_path: The absolute path to the resume file.

    Returns:
        The extracted text from the file.
        
    Raises:
        ValueError: If the file type is not supported.
        Exception: For any other parsing errors.
    """
    try:
        logging.info(f"Parsing file: {file_path}")
        if file_path.endswith('.pdf'):
            return _parse_pdf(file_path)
        elif file_path.endswith('.docx'):
            return _parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {os.path.basename(file_path)}")
    except Exception as e:
        logging.error(f"Error parsing file {file_path}: {e}")
        raise

def _parse_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    with pdfplumber.open(file_path) as pdf:
        text = "\\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def _parse_docx(file_path: str) -> str:
    """Extracts text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\\n".join([para.text for para in doc.paragraphs])

def parse_zip_file(zip_file_path: str) -> list[tuple[str, str]]:
    """
    Extracts all resume files from a ZIP archive, parses them, and returns their content.

    Args:
        zip_file_path: The absolute path to the zip file.

    Returns:
        A list of tuples, where each tuple contains the filename and its extracted text.
    """
    temp_dir = "temp_zip_extraction"
    os.makedirs(temp_dir, exist_ok=True)
    
    resumes_data = []

    try:
        if not zipfile.is_zipfile(zip_file_path):
            raise ValueError("Invalid ZIP file format")

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path) and (filename.endswith('.pdf') or filename.endswith('.docx')):
                try:
                    text = parse_resume_file(file_path)
                    if text:
                        resumes_data.append((filename, text))
                        logging.info(f"Successfully extracted text from {filename} in ZIP.")
                    else:
                        logging.warning(f"No text extracted from {filename} in ZIP. Skipping.")
                except Exception as e:
                    logging.error(f"Error processing file {filename} from ZIP: {e}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return resumes_data
