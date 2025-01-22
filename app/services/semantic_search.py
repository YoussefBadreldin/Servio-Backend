import time
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text: str) -> str:
    """
    Preprocesses text by converting it to lowercase and removing extra spaces.
    """
    return " ".join(text.lower().split())


def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__} with args: {args} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Result: {len(result)} match(es) found")
        return result
    return wrapper


def track_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper


@log_execution
@track_performance
def semantic_search(query: str, registry: List[Dict], aspects: List[str], top_n: int = 5) -> List[Dict]:
    """
    Performs semantic search over the registry using TF-IDF and cosine similarity.

    Args:
    - query: The search query string.
    - registry: The service registry (list of dictionaries).
    - aspects: List of aspects to search in (e.g., "docstring").
    - top_n: Number of top matches to return.

    Returns:
    - List of top matching entries.
    """
    documents = [" ".join(preprocess_text(entry.get(aspect, "")) for aspect in aspects) for entry in registry]
    query = preprocess_text(query)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents + [query])
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    results = sorted(zip(similarities, registry), key=lambda x: x[0], reverse=True)
    return [entry for score, entry in results[:top_n]]
