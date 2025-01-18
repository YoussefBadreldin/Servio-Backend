from typing import List, Dict
from app.utils.logging_utils import log_execution, track_performance

@log_execution
@track_performance
def syntactic_search(query: str, registry: List[Dict], field: str = "func_name", top_n: int = 5) -> List[Dict]:
    """
    Performs syntactic search on the service registry.
    """
    if field not in registry[0]:
        raise ValueError(f"Field '{field}' does not exist in the service registry.")

    results = []

    for entry in registry:
        target_value = entry.get(field, "")
        if query.lower() in target_value.lower():
            results.append(entry)

    return results[:top_n]