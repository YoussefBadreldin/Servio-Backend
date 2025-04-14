# servio-backend/app/modules/registry_builder/service.py
import os
import json
import github3
from typing import List, Dict, Optional
from pathlib import Path
from ...shared.exceptions import RegistryBuilderError
from .models import RepositoryInfo

class RegistryBuilderService:
    def __init__(self):
        self.gh = self.initialize_github_client()
        self.registry_dir = "data/custom_registries"
        self.ensure_directory_exists()

    def initialize_github_client(self):
        """Initialize GitHub client with token from environment"""
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise RegistryBuilderError("GitHub token not found in environment variables")
            return github3.login(token=token)
        except Exception as e:
            raise RegistryBuilderError(f"Failed to initialize GitHub client: {str(e)}")

    def ensure_directory_exists(self):
        """Ensure the custom registry directory exists"""
        try:
            Path(self.registry_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RegistryBuilderError(f"Failed to create registry directory: {str(e)}")

    def fetch_readme(self, repo) -> Optional[str]:
        """Fetch README content from a repository"""
        try:
            readme_content = repo.get_readme().decoded_content.decode("utf-8")
            return readme_content[:500]  # Limit characters
        except:
            return None

    def fetch_repositories(self, query: str, limit: int = 10) -> List[Dict]:
        """Fetch repositories from GitHub based on search query"""
        try:
            repos_data = []
            result = self.gh.search_repositories(query=query, sort="stars", order="desc")
            
            for repo in list(result)[:limit]:
                repo_data = RepositoryInfo(
                    name=repo.name,
                    full_name=repo.full_name,
                    description=repo.description,
                    url=repo.html_url,
                    stars=repo.stargazers_count,
                    forks=repo.forks_count,
                    language=repo.language,
                    license=repo.license['name'] if repo.license and 'name' in repo.license else None,
                    readme=self.fetch_readme(repo))
                repos_data.append(repo_data.dict())
            return repos_data
        except Exception as e:
            raise RegistryBuilderError(f"Failed to fetch repositories: {str(e)}")

    def save_registry(self, registry_data: List[Dict], filename: str = None) -> str:
        """Save registry to a JSON file"""
        try:
            if not filename:
                filename = f"registry_{len(os.listdir(self.registry_dir)) + 1}.json"
            
            filepath = os.path.join(self.registry_dir, filename)
            
            with open(filepath, "w") as f:
                json.dump(registry_data, f, indent=4)
            
            return filename
        except Exception as e:
            raise RegistryBuilderError(f"Failed to save registry: {str(e)}")

    def build_registry(self, query: str, limit: int = 10) -> Dict:
        """Main method to build and save a registry"""
        try:
            repositories = self.fetch_repositories(query, limit)
            filename = self.save_registry(repositories)
            
            return {
                "success": True,
                "message": "Registry built successfully",
                "filename": filename,
                "repositories": repositories
            }
        except RegistryBuilderError as e:
            return {
                "success": False,
                "message": str(e),
                "filename": None,
                "repositories": None
            }