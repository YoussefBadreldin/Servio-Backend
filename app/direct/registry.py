import json
import os
from typing import List, Dict

class RegistryLoader:
    @staticmethod
    def load(file_path: str) -> List[Dict]:
        """Load registry from JSONL file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Registry file not found: {file_path}")
            
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
                    
        return data

    @staticmethod
    def suggest_aspects(existing: Dict[str, str]) -> List[str]:
        """Suggest additional aspect keys"""
        all_aspects = {
            "repo", "path", "func_name", "docstring",
            "code", "url", "language", "partition"
        }
        return list(all_aspects - set(existing.keys()))