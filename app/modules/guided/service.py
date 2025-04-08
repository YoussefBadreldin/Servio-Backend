# app/modules/guided/service.py
from typing import List, Dict
from pathlib import Path
from app.utils.nlp_utils import expand_query
from app.utils.file_handlers import load_registry
from app.core.exceptions import NotFoundException
from app.modules.guided.models import GuidedRequest, GuidedResponse

class GuidedProcessor:
    def __init__(self):
        self.registry_file = "app/data/service_registry.json"
    
    def process(self, request: 'GuidedRequest') -> Dict:  # Using string type hint
        registry = load_registry(self.registry_file)
        
        expanded = expand_query(request.query) if request.expand_query else request.query
        
        results = []
        for entry in registry[:request.top_n]:
            if 'description' in entry:
                results.append({
                    "name": entry.get("name", "Unnamed"),
                    "description": entry.get("description", ""),
                    "url": entry.get("url", ""),
                    "score": 0.9
                })
        
        suggestions = [
            "Try more specific keywords",
            "Filter by language or framework"
        ]
        
        return {
            "query": request.query,
            "expanded_query": expanded,
            "results": results,
            "format": request.format,
            "suggestions": suggestions
        }