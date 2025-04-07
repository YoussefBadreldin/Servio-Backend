import json
import os
from typing import List, Dict, Optional
import github3
from github3.exceptions import NotFoundError
from datetime import datetime

class RegistryBuilder:
    def __init__(self, github_token: str = None):
        """Initialize the registry builder with GitHub API credentials."""
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError("GitHub token is required")
        self.gh = github3.login(token=self.github_token)

    def fetch_repositories(
        self,
        search_query: str,
        max_results: int = 10,
        sort: str = "stars",
        order: str = "desc"
    ) -> List[Dict]:
        """Fetch repositories from GitHub based on search query."""
        repos_data = []
        try:
            result = self.gh.search_repositories(
                query=search_query,
                sort=sort,
                order=order
            )
            
            for repo in list(result)[:max_results]:
                repo_data = {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "url": repo.html_url,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "language": repo.language,
                    "license": repo.license['name'] if repo.license and 'name' in repo.license else "N/A",
                    "readme": self._fetch_readme(repo),
                    "created_at": repo.created_at.isoformat() if repo.created_at else None,
                    "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                    "topics": self._fetch_topics(repo),
                    "metadata": {
                        "fetched_at": datetime.utcnow().isoformat(),
                        "search_query": search_query
                    }
                }
                repos_data.append(repo_data)
                
        except Exception as e:
            raise RuntimeError(f"Error fetching repositories: {str(e)}")
        
        return repos_data

    def _fetch_readme(self, repo) -> str:
        """Fetch README content for a repository."""
        try:
            readme = repo.get_readme()
            return readme.decoded_content.decode("utf-8")[:2000]  # Limit size
        except NotFoundError:
            return "No README found"
        except Exception:
            return "Error fetching README"

    def _fetch_topics(self, repo) -> List[str]:
        """Fetch repository topics."""
        try:
            # Requires repository permissions
            return list(repo.topics())
        except Exception:
            return []

    def save_registry(
        self,
        repositories: List[Dict],
        output_path: str,
        format: str = "json"
    ) -> str:
        """Save the registry to a file in specified format."""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if format == "json":
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(repositories, f, indent=2)
            elif format == "jsonl":
                with open(output_path, "w", encoding="utf-8") as f:
                    for repo in repositories:
                        f.write(json.dumps(repo) + "\n")
            else:
                raise ValueError(f"Unsupported format: {format}")
                
            return output_path
        except Exception as e:
            raise RuntimeError(f"Error saving registry: {str(e)}")

    def build_registry(
        self,
        search_query: str,
        output_path: str,
        max_results: int = 10,
        format: str = "json"
    ) -> Dict:
        """Complete registry building workflow."""
        repos = self.fetch_repositories(search_query, max_results)
        saved_path = self.save_registry(repos, output_path, format)
        
        return {
            "status": "success",
            "repository_count": len(repos),
            "output_path": saved_path,
            "search_query": search_query
        }