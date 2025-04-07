import json
import github3
from typing import List, Dict, Optional
from fastapi import HTTPException
from ...config.settings import settings
from ...utils.github_api import GitHubAPI
from .models import GitHubSearchParams, Repository

class RegistryService:
    def __init__(self):
        self.gh = GitHubAPI(settings.GITHUB_TOKEN)
    
    async def fetch_repositories(self, params: GitHubSearchParams) -> List[Repository]:
        try:
            results = self.gh.search_repositories(
                query=params.query,
                sort=params.sort,
                order=params.order,
                limit=params.limit
            )
            
            repos = []
            for repo in results:
                repos.append(Repository(
                    name=repo.name,
                    full_name=repo.full_name,
                    description=repo.description,
                    url=repo.html_url,
                    stars=repo.stargazers_count,
                    forks=repo.forks_count,
                    language=repo.language,
                    license=getattr(repo.license, 'name', 'N/A'),
                    readme=self._fetch_readme(repo)
                ))
            
            self._save_registry(repos)
            return repos
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"GitHub API error: {str(e)}"
            )
    
    def _fetch_readme(self, repo) -> str:
        try:
            readme = repo.get_readme()
            return readme.decoded_content.decode("utf-8")[:500]
        except:
            return "No README available"
    
    def _save_registry(self, repos: List[Repository]):
        with open(settings.SERVICE_REGISTRY_PATH, "w") as f:
            json.dump([repo.dict() for repo in repos], f, indent=4)
    
    async def get_registry(self) -> List[Repository]:
        try:
            with open(settings.SERVICE_REGISTRY_PATH, "r") as f:
                return [Repository(**repo) for repo in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []