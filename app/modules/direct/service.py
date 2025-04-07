import json
import os
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException
from nltk.corpus import wordnet as wn
from ...config.settings import settings
from ...utils.nlp_utils import preprocess_text, wordnet_similarity
from .models import SearchRequest, AspectMatchRequest, ServiceMatch

class DirectDiscoveryService:
    def __init__(self):
        self.registry = self._load_registry()
        self._download_nltk_resources()
    
    def _download_nltk_resources(self):
        import nltk
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
    
    def _load_registry(self) -> List[Dict]:
        try:
            with open(settings.SERVIO_DATA_PATH, 'r', encoding='utf-8') as f:
                return [json.loads(line) for line in f if line.strip()]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise HTTPException(
                status_code=500,
                detail=f"Registry loading failed: {str(e)}"
            )
    
    async def search_services(self, request: SearchRequest) -> List[ServiceMatch]:
        try:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(
                    lambda entry: self._score_entry(entry, request.aspects),
                    self.registry
                ))
            
            filtered = [r for r in results if r[0] >= request.min_threshold]
            filtered.sort(key=lambda x: x[0], reverse=True)
            
            return [
                ServiceMatch(
                    func_name=entry.get("func_name", "Unknown"),
                    repo=entry.get("repo", "Unknown"),
                    path=entry.get("path", "Unknown"),
                    docstring=entry.get("docstring", "No description"),
                    url=entry.get("url", ""),
                    score=score
                )
                for score, entry in filtered[:request.top_n]
            ]
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Search failed: {str(e)}"
            )
    
    async def match_aspect(self, request: AspectMatchRequest) -> List[ServiceMatch]:
        try:
            matches = []
            for entry in self.registry:
                if request.aspect_key in entry:
                    sim = wordnet_similarity(
                        request.aspect_value, 
                        entry[request.aspect_key]
                    )
                    if sim >= request.min_threshold:
                        matches.append((
                            sim,
                            ServiceMatch(
                                func_name=entry.get("func_name", "Unknown"),
                                repo=entry.get("repo", "Unknown"),
                                path=entry.get("path", "Unknown"),
                                docstring=entry.get("docstring", "No description"),
                                url=entry.get("url", ""),
                                score=sim
                            )
                        ))
            
            matches.sort(key=lambda x: x[0], reverse=True)
            return [match[1] for match in matches[:request.top_n]]
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Aspect matching failed: {str(e)}"
            )
    
    def _score_entry(self, entry: Dict, aspects: Dict[str, str]) -> Tuple[float, Dict]:
        total_score = 0.0
        matched_aspects = 0
        
        for aspect_key, aspect_value in aspects.items():
            if aspect_key in entry:
                sim = wordnet_similarity(aspect_value, entry[aspect_key])
                if sim >= 0.3:  # Default threshold
                    total_score += sim
                    matched_aspects += 1
        
        return (total_score, entry) if matched_aspects >= 1 else (0.0, entry)