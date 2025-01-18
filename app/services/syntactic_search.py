from typing import List, Dict

def syntactic_search(query: str, registry: List[Dict], field: str = "func_name", top_n: int = 5) -> List[Dict]:
    results = [
        entry for entry in registry
        if query.lower() in entry.get(field, "").lower()
    ]
    return results[:top_n]
