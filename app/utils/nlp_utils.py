# app/utils/nlp_utils.py
from nltk.corpus import wordnet as wn
import nltk

# Download required NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

def enhanced_similarity(aspect: str, field_value: str) -> float:
    """Calculate similarity between aspect and field value"""
    aspect_proc = aspect.lower().strip()
    field_proc = field_value.lower().strip()
    
    if aspect_proc in field_proc:
        return 1.0
        
    synsets_aspect = wn.synsets(aspect_proc)
    synsets_field = wn.synsets(field_proc)
    
    if not synsets_aspect or not synsets_field:
        return 0.0
        
    max_sim = max(
      s1.wup_similarity(s2) or 0.0
        for s1 in synsets_aspect
        for s2 in synsets_field
    )
    
    return max_sim

def expand_query(query: str) -> str:
    """Expand search query with related terms"""
    return f"{query} software service microservice API integration cloud service"