# servio-backend/app/modules/registry_builder/service.py

import os
import json
import github3
from typing import List, Dict, Optional
from pathlib import Path
from ...shared.exceptions import RegistryBuilderError
from .models import RepositoryInfo
import re

class RegistryBuilderService:
    def __init__(self):
        self.gh = self.initialize_github_client()
        self.registry_dir = "data/custom_registries"
        self.ensure_directory_exists()

    def _generate_registry_name(self, query: str) -> str:
        """Generate a filename based on the query (sanitized)"""
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', query.lower())  # Sanitize query
        return f"{sanitized}.jsonl"  # Use query as the filename

    def get_existing_registries(self) -> List[Dict]:
        """Get list of existing registries with their queries"""
        registries = []
        try:
            for filename in os.listdir(self.registry_dir):
                if filename.endswith('.jsonl'):
                    # Extract query from filename
                    query_part = filename[:-6]  # Remove '.jsonl'
                    query = query_part.replace('_', ' ')
                    registries.append({
                        'filename': filename,
                        'query': query,
                        'path': os.path.join(self.registry_dir, filename)
                    })
        except Exception:
            pass
        return registries

    def build_registry(self, query: str, limit: int = 5) -> Dict:
        try:
            # Check if registry already exists
            existing = self.get_existing_registries()
            for reg in existing:
                if reg['query'].lower() == query.lower():
                    return {
                        'success': True,
                        'message': "Using existing registry",
                        'registry_path': reg['path'],
                        'repositories': self._load_registry_repos(reg['path'])
                    }

            # Build new registry
            filename = self._generate_registry_name(query)
            repositories = self.fetch_repositories(query, limit)
            registry_path = self.save_registry(repositories, filename)
            
            return {
                'success': True,
                'message': "Registry built successfully",
                'registry_path': registry_path,
                'repositories': repositories
            }
        except RegistryBuilderError as e:
            return {
                'success': False,
                'message': str(e),
                'registry_path': None,
                'repositories': None
            }

    def _load_registry_repos(self, path: str) -> List[Dict]:
        """Load repositories from existing registry file"""
        repos = []
        try:
            with open(path, 'r') as f:
                for line in f:
                    if line.strip():
                        repos.append(json.loads(line))
        except Exception:
            pass
        return repos
    
    def initialize_github_client(self):
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise RegistryBuilderError("GitHub token not found in environment variables")
            return github3.login(token=token)
        except Exception as e:
            raise RegistryBuilderError(f"Failed to initialize GitHub client: {str(e)}")

    def ensure_directory_exists(self):
        try:
            Path(self.registry_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RegistryBuilderError(f"Failed to create registry directory: {str(e)}")

    def fetch_readme(self, repo) -> Optional[str]:
        try:
            readme_content = repo.get_readme().decoded_content.decode("utf-8")
            return readme_content[:500]
        except:
            return None

    def fetch_repositories(self, query: str, limit: int = 5) -> List[Dict]:
        try:
            repos_data = []
            result = self.gh.search_repositories(query=query, sort="stars", order="desc")
            
            for repo in list(result)[:limit]:
                repo_data = RepositoryInfo(
                    func_name=repo.name,
                    full_name=repo.full_name,
                    docstring=repo.description,
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
        try:
            if not filename:
                filename = f"{len(os.listdir(self.registry_dir)) + 1}.jsonl"  # Fallback filename

            filepath = os.path.join(self.registry_dir, filename)
            
            with open(filepath, "w") as f:
                for item in registry_data:
                    f.write(json.dumps(item) + "\n")
            
            return filepath
        except Exception as e:
            raise RegistryBuilderError(f"Failed to save registry: {str(e)}")
