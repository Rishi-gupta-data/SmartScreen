# backend/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Define the path for the data directory
DATA_DIR = os.path.join(BASE_DIR, 'data')

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    
    # Database configuration
    # For Supabase: postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(DATA_DIR, 'ats.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Data folders
    RESUMES_FOLDER = os.path.join(DATA_DIR, 'resumes')
    JOBS_FOLDER = os.path.join(DATA_DIR, 'jobs')

    # NLP & Embedding Configuration
    HF_EMBEDDING_MODEL = os.environ.get('HF_EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')

    # Admin Credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'rishi')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '9711')
    
 
    @staticmethod
    def init_app(app):
        os.makedirs(Config.RESUMES_FOLDER, exist_ok=True)
        os.makedirs(Config.JOBS_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    #
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
