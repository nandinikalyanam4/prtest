#!/usr/bin/env python3
"""
Jira API Utility
Handles Jira API interactions for ticket validation.
"""

import requests
from typing import Dict, Any, Optional, List
from requests.auth import HTTPBasicAuth


class JiraAPI:
    """Jira API client for ticket operations"""
    
    def __init__(self, base_url: str, username: str, api_token: str):
        """
        Initialize Jira API client.
        
        Args:
            base_url: Jira base URL (e.g., https://yourcompany.atlassian.net)
            username: Jira username/email
            api_token: Jira API token
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_token = api_token
        self.auth = HTTPBasicAuth(username, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request to Jira API"""
        url = f"{self.base_url}/rest/api/3/{endpoint}"
        response = requests.request(
            method,
            url,
            auth=self.auth,
            headers=self.headers,
            **kwargs
        )
        response.raise_for_status()
        return response
    
    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """
        Get Jira ticket details.
        
        Args:
            ticket_id: Jira ticket ID (e.g., PROJ-1234)
        
        Returns:
            Ticket data as dictionary
        """
        response = self._make_request("GET", f"issue/{ticket_id}")
        return response.json()
    
    def get_ticket_status(self, ticket_id: str) -> str:
        """Get ticket status name"""
        ticket = self.get_ticket(ticket_id)
        return ticket.get('fields', {}).get('status', {}).get('name', '')
    
    def get_ticket_url(self, ticket_id: str) -> str:
        """Get web URL for ticket"""
        return f"{self.base_url}/browse/{ticket_id}"
    
    def search_tickets(self, jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search tickets using JQL.
        
        Args:
            jql: Jira Query Language query
            max_results: Maximum number of results
        
        Returns:
            List of tickets
        """
        data = {
            "jql": jql,
            "maxResults": max_results
        }
        response = self._make_request("POST", "search", json=data)
        return response.json().get('issues', [])
    
    def update_ticket_status(self, ticket_id: str, transition_id: str) -> Dict[str, Any]:
        """
        Update ticket status using transition.
        
        Args:
            ticket_id: Jira ticket ID
            transition_id: Transition ID (get from /transitions endpoint)
        """
        data = {"transition": {"id": transition_id}}
        response = self._make_request("POST", f"issue/{ticket_id}/transitions", json=data)
        return response.json()
    
    def get_transitions(self, ticket_id: str) -> List[Dict[str, Any]]:
        """Get available transitions for a ticket"""
        response = self._make_request("GET", f"issue/{ticket_id}/transitions")
        return response.json().get('transitions', [])

