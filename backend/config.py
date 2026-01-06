# backend/config.py
import os


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Define the path for the data directory
DATA_DIR = os.path.join(BASE_DIR, 'data')

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(DATA_DIR, 'ats.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Data folders
    RESUMES_FOLDER = os.path.join(DATA_DIR, 'resumes')
    JOBS_FOLDER = os.path.join(DATA_DIR, 'jobs')

    # LLM Configuration 
    LLM_PROVIDER = os.environ.get('LLM_PROVIDER', None)  # e.g., 'OLLAMA'
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'phi3:mini')

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
