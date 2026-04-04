import os
import spacy
from backend.models.db import db
from backend.models.candidate import Candidate
from backend.utils.file_utils import extract_text_from_file
from sentence_transformers import SentenceTransformer

class ResumeParser:
    def __init__(self):
        # Load the sentence-transformer model
        model_name = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)

    def process_resume(self, file_path: str) -> Candidate:
        """
        Extracts text from a resume file, generates its embedding,
        and saves the data to the database.
        """
        filename = os.path.basename(file_path)
        extracted_text = extract_text_from_file(file_path)

        if not extracted_text:
            raise ValueError(f"Could not extract text from {filename}")

        # Generate embedding using SentenceTransformer
        embedding_vec = self.model.encode(extracted_text)
        embedding = embedding_vec.tobytes() # Store as bytes for PickleType

        candidate = Candidate(
            filename=filename,
            extracted_text=extracted_text,
            embedding=embedding
        )
        db.session.add(candidate)
        db.session.commit()
        return candidate

    def get_candidate_by_id(self, candidate_id: str) -> Candidate:
        return Candidate.query.get(candidate_id)

    def get_all_candidates(self):
        return Candidate.query.all()