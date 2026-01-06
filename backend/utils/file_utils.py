import pdfplumber
from docx import Document

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() if page.extract_text() else ""
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return ""
    return text

def extract_text_from_docx(docx_path: str) -> str:
    """
    Extracts text from a DOCX file.
    """
    text = ""
    try:
        document = Document(docx_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX {docx_path}: {e}")
        return ""
    return text

def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from a file based on its extension.
    Supports PDF and DOCX.
    """
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return ""