# scripts/init_db.py
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
import logging

def initialize_database():
    """
    Creates the database tables based on the defined models.
    This should only be run once, or after dropping the database.
    """
    try:
        # Create a Flask app context
        app = create_app('development')
        with app.app_context():
            logging.info("Dropping all database tables...")
            db.drop_all()
            logging.info("Creating all database tables...")
            db.create_all()
            logging.info("Database tables created successfully.")
            
            # You could add some initial seed data here if needed
            # For example:
            # from backend.models.job import Job
            # if not Job.query.first():
            #     seed_job = Job(title="Sample Job", description="This is a sample job description.")
            #     db.session.add(seed_job)
            #     db.session.commit()
            #     logging.info("Seeded database with a sample job.")

    except Exception as e:
        logging.error(f"An error occurred during database initialization: {e}")
        sys.exit(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print("This script will re-initialize the database, deleting all existing data.")
    confirm = input("Are you sure you want to continue? (y/n): ")
    if confirm.lower() == 'y':
        initialize_database()
    else:
        print("Database initialization cancelled.")
