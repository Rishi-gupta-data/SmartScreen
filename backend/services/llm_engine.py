# backend/services/llm_engine.py
import logging

class LLMEngine:
    """
    An abstracted service for interacting with a Large Language Model (LLM).

    In the MVP, this service is a placeholder and does not connect to any LLM.
    Its methods are designed to fail gracefully or do nothing, ensuring the
    application can run without any LLM installed or configured.
    """

    def __init__(self):
        logging.info("LLMEngine initialized. NOTE: LLM is disabled in the current configuration.")
        self.enabled = False

    def get_suggestions(self, resume_text: str, job_description_text: str) -> dict:
        """
        Provides suggestions for improving a resume.
        
        This is a placeholder and will not provide real suggestions.
        """
        if not self.enabled:
            logging.warning("LLM is not enabled. Cannot provide suggestions.")
            return {
                "error": "LLM engine is not configured. This feature is disabled."
            }
        
        # In a future implementation, this would call an LLM.
        raise NotImplementedError("LLM interaction is not implemented in the MVP.")

    def get_keyword_optimization(self, resume_text: str, job_description_text: str) -> dict:
        """
        Provides keyword optimization tips.

        This is a placeholder and will not provide real optimization.
        """
        if not self.enabled:
            logging.warning("LLM is not enabled. Cannot provide keyword optimization.")
            return {
                "error": "LLM engine is not configured. This feature is disabled."
            }

        raise NotImplementedError("LLM interaction is not implemented in the MVP.")

# Single instance to be used across the application
llm_engine = LLMEngine()
