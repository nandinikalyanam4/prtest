#!/usr/bin/env python3
"""
GitHub API Utility
Handles GitHub API interactions for PR operations.
"""

import os
import requests
from typing import Dict, Any, Optional, List


class GitHubAPI:
    """GitHub API client for PR operations"""
    
    def __init__(self, token: str, repository: str):
        """
        Initialize GitHub API client.
        
        Args:
            token: GitHub personal access token
            repository: Repository in format 'owner/repo'
        """
        self.token = token
        self.repository = repository
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request to GitHub API"""
        url = f"{self.base_url}/repos/{self.repository}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response
    
    def get_pull_request(self, pr_number: int) -> Dict[str, Any]:
        """Get PR details"""
        response = self._make_request("GET", f"pulls/{pr_number}")
        return response.json()
    
    def get_pr_diff(self, pr_number: int) -> str:
        """Get PR diff as text"""
        response = self._make_request(
            "GET",
            f"pulls/{pr_number}",
            headers={**self.headers, "Accept": "application/vnd.github.v3.diff"}
        )
        return response.text
    
    def get_pr_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """Get list of files changed in PR"""
        response = self._make_request("GET", f"pulls/{pr_number}/files")
        return response.json()
    
    def post_comment(self, pr_number: int, body: str) -> Dict[str, Any]:
        """Post a comment on PR"""
        data = {"body": body}
        response = self._make_request("POST", f"issues/{pr_number}/comments", json=data)
        return response.json()
    
    def create_review(self, pr_number: int, event: str, body: str, comments: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Create a PR review.
        
        Args:
            pr_number: PR number
            event: 'APPROVE', 'REQUEST_CHANGES', or 'COMMENT'
            body: Review body text
            comments: Optional list of inline comments
        """
        data = {
            "event": event,
            "body": body
        }
        if comments:
            data["comments"] = comments
        
        response = self._make_request("POST", f"pulls/{pr_number}/reviews", json=data)
        return response.json()
    
    def get_pr_commits(self, pr_number: int) -> List[Dict[str, Any]]:
        """Get commits in PR"""
        response = self._make_request("GET", f"pulls/{pr_number}/commits")
        return response.json()
    
    def get_branch(self, branch_name: str) -> Dict[str, Any]:
        """Get branch information"""
        response = self._make_request("GET", f"branches/{branch_name}")
        return response.json()

