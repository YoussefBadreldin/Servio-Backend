# app/utils/file_handlers.py
import json
from typing import List, Dict
from pathlib import Path

def load_registry(file_path: str) -> List[Dict]:
    """Load service registry from JSON file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Registry file not found: {file_path}")
    
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in file: {file_path}")

def save_registry(data: List[Dict], file_path: str):
    """Save data to registry file"""
    path = Path(file_path)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)