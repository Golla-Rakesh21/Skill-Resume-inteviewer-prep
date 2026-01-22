# utils/evaluator.py
from typing import Dict, List
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

_model = None

def get_model():
    """Load the SentenceTransformer model once and cache it."""
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def _clean(text: str) -> str:
    """Basic text cleaning: lowercase, remove punctuation/numbers."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z\s]", " ", text)  # keep only letters
    return re.sub(r"\s+", " ", text)

def evaluate_answer(answer: str, references: List[str]) -> Dict[str, float]:
    """
    Compare candidate answer with reference snippets using embeddings.
    Returns a score (0–100) and the best-matching reference.
    """
    if not answer or not references:
        return {"score": 0.0, "best_match": ""}

    model = get_model()
    answer_clean = _clean(answer)
    refs_clean = [_clean(r) for r in references]

    # ✅ Ensure embeddings are NumPy arrays
    a_emb = model.encode([answer_clean], convert_to_numpy=True)
    r_embs = model.encode(refs_clean, convert_to_numpy=True)

    sims = cosine_similarity(a_emb, r_embs)[0]
    best_idx = sims.argmax()
    best_score = float(sims[best_idx]) * 100.0

    return {
        "score": round(best_score, 2),
        "best_match": references[best_idx]
    }
