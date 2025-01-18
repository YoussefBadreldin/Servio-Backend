import zipfile
import json
from typing import List, Dict

def extract_zip(zip_file_path: str, extract_path: str = '.') -> None:
    """
    Extracts a zip file to the specified path.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def load_json(file_path: str) -> List[Dict]:
    """
    Loads JSON data from a file.
    """
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                json_object = json.loads(line)
                data.append(json_object)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON line: {line.strip()} - Error: {e}")
    return data