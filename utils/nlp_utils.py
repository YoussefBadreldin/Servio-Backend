import nltk
from nltk.corpus import wordnet as wn
from typing import Tuple

def download_nltk_resources():
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    nltk.download('punkt', quiet=True)

def preprocess_text(text: str) -> str:
    return " ".join(text.lower().split())

def wordnet_similarity(text1: str, text2: str) -> float:
    text1_proc = preprocess_text(text1)
    text2_proc = preprocess_text(text2)
    
    if text1_proc in text2_proc or text2_proc in text1_proc:
        return 1.0
        
    synsets1 = wn.synsets(text1_proc)
    synsets2 = wn.synsets(text2_proc)
    
    if not synsets1 or not synsets2:
        return 0.0
        
    max_sim = 0.0
    for syn1 in synsets1:
        for syn2 in synsets2:
            sim = syn1.wup_similarity(syn2) or 0.0
            if sim > max_sim:
                max_sim = sim
    return max_sim