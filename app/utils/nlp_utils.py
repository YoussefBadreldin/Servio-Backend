# app/utils/nlp_utils.py
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict, Tuple
from functools import lru_cache

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

@lru_cache(maxsize=1000)
def enhanced_similarity(aspect: str, field_value: str) -> float:
    """Enhanced similarity with WordNet and substring matching"""
    if not aspect or not field_value:
        return 0.0
        
    aspect_proc = aspect.lower().strip()
    field_proc = str(field_value).lower().strip()
    
    # Substring match
    if aspect_proc in field_proc:
        return 1.0
        
    # WordNet similarity
    synsets_aspect = wn.synsets(aspect_proc)
    synsets_field = wn.synsets(field_proc)
    
    if not synsets_aspect or not synsets_field:
        return 0.0
        
    max_sim = max(
        (s1.wup_similarity(s2) or 0.0
         for s1 in synsets_aspect
         for s2 in synsets_field),
        default=0.0
    )
    
    return max_sim

def expand_query(query: str) -> str:
    """Expand query with related terms"""
    expansions = {
        "api": ["gateway", "rest", "graphql"],
        "microservice": ["service", "container", "kubernetes"],
        "database": ["storage", "query", "nosql", "sql"]
    }
    
    expanded = [query]
    for term, related in expansions.items():
        if term in query.lower():
            expanded.extend(related)
    
    return " ".join(expanded)