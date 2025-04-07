from pathlib import Path
from fastapi import UploadFile
import json
from typing import Dict, List

async def save_uploaded_file(file: UploadFile, directory: Path) -> Path:
    try:
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / file.filename
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
            
        return file_path
    except Exception as e:
        raise RuntimeError(f"File save failed: {str(e)}")

def load_jsonl(file_path: Path) -> List[Dict]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    except Exception as e:
        raise RuntimeError(f"JSONL load failed: {str(e)}")