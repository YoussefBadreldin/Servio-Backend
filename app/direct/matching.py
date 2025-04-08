# SERVIO-BACKEND/app/direct/matching.py
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict, Tuple
import json

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

class DirectMatcher:
    def __init__(self, min_threshold: float = 0.3):
        self.min_threshold = min_threshold
        
    def preprocess_text(self, text: str) -> str:
        """Normalize text for comparison"""
        return " ".join(text.lower().split())

    def enhanced_similarity(self, aspect: str, field_value: str) -> float:
        """Combined substring and WordNet similarity"""
        aspect_proc = self.preprocess_text(aspect)
        field_proc = self.preprocess_text(str(field_value))
        
        # Exact substring match
        if aspect_proc in field_proc:
            return 1.0
            
        # WordNet semantic similarity
        synsets_aspect = wn.synsets(aspect_proc)
        synsets_field = wn.synsets(field_proc)
        max_sim = 0.0
        
        if synsets_aspect and synsets_field:
            for syn1 in synsets_aspect:
                for syn2 in synsets_field:
                    sim = syn1.wup_similarity(syn2) or 0.0
                    max_sim = max(max_sim, sim)
                    
        return max_sim

    def match_services(
        self, 
        query: str,
        registry: List[Dict],
        aspects: Dict[str, str],
        top_n: int = 5
    ) -> List[Dict]:
        """Main matching function"""
        scored_entries = []
        
        for entry in registry:
            total_score = 0.0
            matched_aspects = 0
            
            for aspect_key, aspect_value in aspects.items():
                if aspect_key in entry:
                    sim = self.enhanced_similarity(
                        aspect_value, 
                        entry[aspect_key]
                    )
                    if sim >= self.min_threshold:
                        total_score += sim
                        matched_aspects += 1
            
            if matched_aspects >= 1:  # At least one aspect match
                scored_entries.append((total_score, entry))
                
        # Sort by score and return top N
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        return [entry for score, entry in scored_entries[:top_n]]

    def match_per_aspect(
        self,
        registry: List[Dict],
        aspect_key: str,
        aspect_value: str,
        top_n: int = 3
    ) -> List[Dict]:
        """Match services for a single aspect"""
        scored = []
        
        for entry in registry:
            if aspect_key in entry:
                sim = self.enhanced_similarity(
                    aspect_value,
                    entry[aspect_key]
                )
                if sim >= self.min_threshold:
                    scored.append((sim, entry))
                    
        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for sim, entry in scored[:top_n]]