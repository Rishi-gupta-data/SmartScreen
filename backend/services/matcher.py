import numpy as np
from typing import List, Dict, Any
from backend.models.candidate import Candidate
from backend.models.job import Job

class Matcher:
    def __init__(self):
        pass

    def calculate_similarity(self, embedding1: bytes, embedding2: bytes) -> float:
        """
        Calculates cosine similarity between two embeddings.
        Embeddings are expected to be bytes and will be converted to numpy arrays.
        """
        if embedding1 is None or embedding2 is None:
            return 0.0

        vec1 = np.frombuffer(embedding1, dtype=np.float32)
        vec2 = np.frombuffer(embedding2, dtype=np.float32)

        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0 # Avoid division by zero for zero vectors

        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(similarity)

    def match_candidates_to_job(self, job: Job, candidates: List[Candidate]) -> List[Dict[str, Any]]:
        """
        Matches a list of candidates to a job and returns ranked results.
        """
        if job.embedding is None:
            return [] # Cannot match without a job embedding

        results = []
        for candidate in candidates:
            if candidate.embedding:
                similarity = self.calculate_similarity(job.embedding, candidate.embedding)
                results.append({
                    "candidate_id": candidate.id,
                    "filename": candidate.filename,
                    "score": round(similarity, 4)
                })
        
        # Rank candidates by score in descending order
        results.sort(key=lambda x: x["score"], reverse=True)
        return results