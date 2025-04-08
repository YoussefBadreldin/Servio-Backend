import github3
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from app.registry_builder.readme import fetch_readme

load_dotenv()

class GitHubRegistryBuilder:
    def __init__(self):
        self.gh = github3.login(
            token=os.getenv("GITHUB_TOKEN")
        )
        self.default_query = "microservice language:python"
        
    def fetch_repositories(
        self,
        query: Optional[str] = None,
        limit: int = 10,
        min_stars: int = 10
    ) -> List[Dict]:
        """Fetch repositories from GitHub matching criteria"""
        search_query = query or self.default_query
        repos_data = []
        
        try:
            results = self.gh.search_repositories(
                query=search_query,
                sort="stars",
                order="desc"
            )
            
            for repo in results:
                if repo.stargazers_count < min_stars:
                    continue
                    
                repos_data.append(self._format_repo(repo))
                if len(repos_data) >= limit:
                    break
                    
        except Exception as e:
            print(f"GitHub API error: {e}")
            
        return repos_data
        
    def _format_repo(self, repo) -> Dict:
        """Standardize repository data format"""
        return {
            "func_name": repo.name,
            "full_name": repo.full_name,
            "docstring": repo.description or "",
            "url": repo.html_url,
            "repo": [repo.full_name.split('/')[0]],
            "stars": repo.stargazers_count,
            "language": repo.language,
            "license": repo.license['name'] if repo.license else "N/A",
            "readme": fetch_readme(repo)
        }