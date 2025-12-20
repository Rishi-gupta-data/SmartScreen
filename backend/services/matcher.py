# backend/services/matcher.py
import spacy
import numpy as np
import logging

class MatcherService:
    """
    A service to calculate the similarity between a resume and a job description
    using SpaCy's text vectorization and cosine similarity.
    """
    _nlp = None

    @classmethod
    def _load_model(cls):
        """Loads the SpaCy model if it hasn't been loaded yet."""
        if cls._nlp is None:
            try:
                logging.info("Loading SpaCy model 'en_core_web_md'...")
                cls._nlp = spacy.load('en_core_web_md')
                logging.info("SpaCy model loaded successfully.")
            except OSError:
                logging.error("SpaCy model 'en_core_web_md' not found.")
                logging.info("Please run 'python -m spacy download en_core_web_md' to install it.")
                raise

    def __init__(self):
        self._load_model()

    def calculate_similarity(self, resume_text: str, job_description_text: str) -> float:
        """
        Calculates the cosine similarity between the resume and job description.

        Args:
            resume_text: The text content of the resume.
            job_description_text: The text content of the job description.

        Returns:
            A similarity score between 0.0 and 1.0.
        """
        if not resume_text or not job_description_text:
            return 0.0

        try:
            resume_doc = self._nlp(resume_text)
            jd_doc = self._nlp(job_description_text)

            # Check for zero vectors, which can happen with empty or out-of-vocabulary text
            if not resume_doc.has_vector or not jd_doc.has_vector or resume_doc.vector_norm == 0 or jd_doc.vector_norm == 0:
                logging.warning("Could not generate a vector for resume or job description. Returning 0.0 similarity.")
                return 0.0

            # Cosine similarity
            similarity = np.dot(resume_doc.vector, jd_doc.vector) / (resume_doc.vector_norm * jd_doc.vector_norm)
            
            # Ensure the result is a standard float and within the [0, 1] range
            return float(np.clip(similarity, 0.0, 1.0))

        except Exception as e:
            logging.error(f"Error calculating similarity: {e}")
            return 0.0

# You can create a single instance to be used across the application
matcher_service = MatcherService()
