"""GitHub fetcher to dynamically ingest repos from GitHub API."""

import httpx
from typing import List, Dict, Any, Optional
from config import settings


class GitHubFetcher:
    """Fetch repository data from GitHub API."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    def fetch_repo(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Fetch a single repository's data."""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "full_name": data["full_name"],
                    "name": data["name"],
                    "description": data.get("description") or "",
                    "stars": data["stargazers_count"],
                    "forks": data["forks_count"],
                    "language": data.get("language") or "Unknown",
                    "url": data["html_url"],
                    "owner": data["owner"]["login"],
                    "topics": data.get("topics", [])
                }
            else:
                print(f"Failed to fetch {owner}/{repo}: {response.status_code}")
                return None
    
    def fetch_readme(self, owner: str, repo: str) -> str:
        """Fetch repository README content."""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"
        
        with httpx.Client() as client:
            response = client.get(url, headers={**self.headers, "Accept": "application/vnd.github.raw"})
            
            if response.status_code == 200:
                return response.text[:2000]  # Limit to first 2000 chars
            else:
                return ""
    
    def fetch_dependencies(self, owner: str, repo: str) -> List[str]:
        """Fetch dependencies from requirements.txt or pyproject.toml."""
        deps = []
        
        # Try requirements.txt
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/requirements.txt"
        with httpx.Client() as client:
            response = client.get(url, headers={**self.headers, "Accept": "application/vnd.github.raw"})
            
            if response.status_code == 200:
                for line in response.text.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Extract package name (before ==, >=, etc)
                        pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split("[")[0].strip()
                        if pkg:
                            deps.append(pkg.lower())
        
        return deps[:20]  # Limit to 20 dependencies
    
    def fetch_awesome_list(self, list_url: str) -> List[str]:
        """Fetch repos from an awesome list."""
        repos = []
        
        # Parse owner/repo from URL
        parts = list_url.replace("https://github.com/", "").split("/")
        if len(parts) >= 2:
            owner, repo = parts[0], parts[1]
            
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"
            with httpx.Client() as client:
                response = client.get(url, headers={**self.headers, "Accept": "application/vnd.github.raw"})
                
                if response.status_code == 200:
                    # Extract GitHub repo links from README
                    import re
                    pattern = r'github\.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)'
                    matches = re.findall(pattern, response.text)
                    repos = list(set(matches))[:50]  # Limit to 50 repos
        
        return repos
    
    def search_repos(self, query: str, language: str = "python", limit: int = 30) -> List[str]:
        """Search for repos on GitHub."""
        url = f"{self.BASE_URL}/search/repositories"
        params = {
            "q": f"{query} language:{language}",
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }
        
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return [item["full_name"] for item in data.get("items", [])]
            else:
                print(f"Search failed: {response.status_code}")
                return []


github_fetcher = GitHubFetcher()
