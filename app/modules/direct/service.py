# app/modules/direct/service.py
from typing import List, Dict
from pathlib import Path
import json
from app.core.exceptions import NotFoundException
from app.utils.nlp_utils import enhanced_similarity
from .models import DirectRequest, DirectResponse, AspectMatch  # This import must come first

class DirectProcessor:
    def __init__(self):
        self.registry_file = "app/data/servio_data.json"
        self.all_aspects = {
            "func_name", "repo", "path", "docstring", 
            "code", "url", "language", "partition"
        }
    
    def load_registry(self) -> List[Dict]:
        path = Path(self.registry_file)
        if not path.exists():
            raise NotFoundException("Service registry")
        
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    
    def get_available_aspects(self) -> List[str]:
        return sorted(self.all_aspects)
    
    def process(self, request: 'DirectRequest') -> 'DirectResponse':
        registry = self.load_registry()
        
        # Process overall matches
        overall_matches = self._match_services(
            request.query, registry, request.min_threshold, request.top_n
        )
        
        # Process individual aspects
        aspect_matches = []
        for aspect, value in request.aspects.items():
            matches = self._match_services_per_aspect(
                aspect, value, registry, request.min_threshold, request.top_n
            )
            if matches:
                avg_score = sum(m['score'] for m in matches) / len(matches)
                aspect_matches.append({
                    "aspect": aspect,
                    "value": value,
                    "score": avg_score,
                    "matched_services": matches
                })
        
        # Suggest missing aspects
        suggested_aspects = list(self.all_aspects - set(request.aspects.keys()))
        
        return {
            "query": request.query,
            "overall_matches": overall_matches,
            "aspect_matches": aspect_matches,
            "suggested_aspects": suggested_aspects
        }
    
    def _match_services(self, query: str, registry: List[Dict], 
                       min_threshold: float, top_n: int) -> List[Dict]:
        scored = []
        for entry in registry:
            score = 0.0
            if 'description' in entry:
                score = enhanced_similarity(query, entry['description'])
            if score >= min_threshold:
                scored.append((score, entry))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"entry": entry, "score": score} for score, entry in scored[:top_n]]
    
    def _match_services_per_aspect(self, aspect: str, value: str, 
                                  registry: List[Dict], min_threshold: float, 
                                  top_n: int) -> List[Dict]:
        scored = []
        for entry in registry:
            if aspect in entry:
                score = enhanced_similarity(value, str(entry[aspect]))
                if score >= min_threshold:
                    scored.append((score, entry))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"entry": entry, "score": score} for score, entry in scored[:top_n]]