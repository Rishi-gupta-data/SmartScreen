# backend/config.py
import os

# Build the absolute path for the database file
# This ensures that the path is correct regardless of where the app is run from
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
    
    # Ensure data directories exist
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
    # Add any production-specific settings here

# Dictionary to access config classes by name
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
