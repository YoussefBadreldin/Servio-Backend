import json
from typing import List, Dict

def tokenize(text: str) -> List[str]:
    return text.lower().split()

def jaccard_similarity(tokens1: List[str], tokens2: List[str]) -> float:
    set1, set2 = set(tokens1), set(tokens2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0.0

def semantic_search(query: str, registry: List[Dict], aspects: List[str], top_n: int = 5) -> List[Dict]:
    query_tokens = tokenize(query)
    results = []

    for entry in registry:
        content = " ".join(entry.get(aspect, "") for aspect in aspects)
        content_tokens = tokenize(content)
        similarity = jaccard_similarity(query_tokens, content_tokens)
        results.append((similarity, entry))

    results.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in results[:top_n]]
