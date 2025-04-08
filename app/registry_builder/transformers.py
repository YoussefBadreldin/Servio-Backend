import json
from typing import List, Dict
import os

class RegistryTransformer:
    @staticmethod
    def to_jsonl(data: List[Dict], output_path: str):
        """Convert registry data to JSONL format"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            for item in data:
                f.write(json.dumps(item) + "\n")
                
        return output_path
        
    @staticmethod
    def to_servio_format(data: List[Dict]) -> List[Dict]:
        """Transform GitHub data to Serv.io schema"""
        transformed = []
        for repo in data:
            transformed.append({
                "func_name": repo["func_name"],
                "docstring": repo["docstring"],
                "repo": repo["repo"],
                "url": repo["url"],
                "language": repo["language"],
                "metadata": {
                    "stars": repo["stars"],
                    "license": repo["license"],
                    "readme_excerpt": repo["readme"]
                }
            })
        return transformed