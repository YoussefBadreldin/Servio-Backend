# app/utils/file_handlers.py
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any

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

def extract_zip(zip_path: str, extract_to: str) -> List[str]:
    """Extract ZIP file and return extracted paths"""
    path = Path(extract_to)
    path.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        return zip_ref.namelist()

def parse_xml(xml_path: str) -> Dict[str, str]:
    """Parse XML file to dictionary"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    aspects = {}
    for aspect in root.findall("Aspect"):
        key = aspect.find("Key").text.strip()
        value = aspect.find("Value").text.strip()
        aspects[key] = value
    
    return aspects