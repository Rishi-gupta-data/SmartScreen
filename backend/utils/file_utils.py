# backend/utils/file_utils.py
import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

def save_resume_file(file) -> str:
    """
    Saves an uploaded resume file to the configured RESUMES_FOLDER.

    Args:
        file: The file object from the request.

    Returns:
        The full path to the saved file.
    """
    if not file or not file.filename:
        raise ValueError("Invalid file provided.")

    # Get the original filename and extension
    original_filename = secure_filename(file.filename)
    extension = os.path.splitext(original_filename)[1]
    
    # Generate a unique filename to prevent overwrites and conflicts
    unique_filename = f"{uuid.uuid4()}{extension}"
    
    # Get the folder from the app config
    upload_folder = current_app.config['RESUMES_FOLDER']
    
    # Ensure the upload folder exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Build the full path and save the file
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    return filepath, original_filename
