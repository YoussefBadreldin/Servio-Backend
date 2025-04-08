# SERVIO-BACKEND/app/cache.py
from datetime import datetime, timedelta
import hashlib
import json
import os
from typing import Any, Dict

class QueryCache:
    def __init__(self):
        self.cache_dir = "./data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _get_cache_path(self, query: str) -> str:
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return f"{self.cache_dir}/{query_hash}.json"
        
    def get(self, query: str) -> Dict[str, Any] | None:
        cache_path = self._get_cache_path(query)
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        return None
        
    def set(self, query: str, data: Dict[str, Any]) -> None:
        cache_path = self._get_cache_path(query)
        with open(cache_path, "w") as f:
            json.dump(data, f)

cache = QueryCache()