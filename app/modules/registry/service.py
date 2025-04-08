# app/modules/registry/service.py
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from app.core.config import settings
from app.core.exceptions import NotFoundException, ServioException
from .models import RepoInfo  # Add this import

class RegistryService:
    def __init__(self):
        self.cache_file = Path("app/data/service_registry.json")
        self.github_api = "https://api.github.com/search/repositories"
        self.cache = []
        self._load_cache()
    
    def _load_cache(self):
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                try:
                    self.cache = json.load(f)
                except json.JSONDecodeError:
                    self.cache = []
    
    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def fetch_from_cache(self, query: str, limit: int) -> Dict:
        if not self.cache:
            raise NotFoundException("Cached registry")
            
        filtered = [repo for repo in self.cache if query.lower() in repo['name'].lower()]
        return {
            "query": query,
            "repos": [self._to_repo_info(repo) for repo in filtered[:limit]],
            "count": len(filtered),
            "from_cache": True
        }
    
    def refresh_registry(self):
        """Refresh registry from GitHub API"""
        if not settings.GITHUB_TOKEN:
            raise ServioException("GitHub token not configured")
            
        headers = {
            "Authorization": f"token {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        params = {
            "q": "microservice language:python",
            "sort": "stars",
            "order": "desc",
            "per_page": 100
        }
        
        try:
            response = requests.get(self.github_api, headers=headers, params=params)
            response.raise_for_status()
            
            repos = []
            for item in response.json()['items'][:50]:  # Limit to top 50
                repos.append({
                    "name": item['name'],
                    "full_name": item['full_name'],
                    "description": item['description'],
                    "url": item['html_url'],
                    "stars": item['stargazers_count'],
                    "forks": item['forks_count'],
                    "language": item['language'],
                    "license": item['license']['name'] if item['license'] else None,
                    "readme_preview": self._fetch_readme_preview(item['full_name'], headers)
                })
            
            self.cache = repos
            self._save_cache()
            
        except Exception as e:
            raise ServioException(f"Failed to refresh registry: {str(e)}")
    
    def _fetch_readme_preview(self, repo_full_name: str, headers: Dict) -> str:
        try:
            url = f"https://api.github.com/repos/{repo_full_name}/readme"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            content = response.json().get('content', '')
            import base64
            decoded = base64.b64decode(content).decode('utf-8')
            return decoded[:500]  # Return first 500 chars
        except:
            return "No README preview available"
    
    def _to_repo_info(self, repo: Dict) -> RepoInfo:
        return RepoInfo(
            name=repo['name'],
            full_name=repo['full_name'],
            description=repo['description'],
            url=repo['url'],
            stars=repo['stars'],
            forks=repo['forks'],
            language=repo['language'],
            license=repo['license'],
            readme_preview=repo['readme_preview']
        )