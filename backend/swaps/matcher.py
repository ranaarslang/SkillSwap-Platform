"""Bidirectional semantic matching for skill swaps."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

_model = None


def _text(skills):
    return ", ".join(skills) if skills else ""


def calculate_matches(user, profiles):
    people = [profile for profile in profiles if profile.user_id != user.id]
    corpus = []
    for profile in [user.profile, *people]:
        corpus.extend([_text(profile.skills_offered), _text(profile.skills_wanted)])
    global _model
    if SentenceTransformer and any(corpus):
        if _model is None:
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        matrix = _model.encode(corpus, normalize_embeddings=True)
    else:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(corpus) if any(corpus) else np.zeros((len(corpus), 1))
    current_teach, current_learn = matrix[0], matrix[1]
    results = []
    for index, profile in enumerate(people):
        teach = matrix[(index + 1) * 2]
        learn = matrix[(index + 1) * 2 + 1]
        score = (cosine_similarity(current_teach, learn)[0][0] + cosine_similarity(teach, current_learn)[0][0]) / 2
        results.append({"profile": profile, "score": round(score * 100)})
    return sorted(results, key=lambda result: result["score"], reverse=True)
