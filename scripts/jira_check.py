#!/usr/bin/env python3
"""
Jira Validation Script
Validates that PR branch/title contains a valid Jira ticket and checks ticket status.
"""

import os
import sys
import re
import requests
from typing import Optional, Dict, Any, Tuple
from scripts.utils.github_api import GitHubAPI
from scripts.utils.jira_api import JiraAPI


def extract_jira_ticket(branch_name: str, pr_title: str, project_key: str) -> Optional[str]:
    """
    Extract Jira ticket ID from branch name or PR title.
    Expected format: PROJ-1234 or feature/PROJ-1234-description
    """
    # Pattern to match JIRA ticket format: PROJECT-1234
    pattern = rf'({project_key}-\d+)'
    
    # Try branch name first
    match = re.search(pattern, branch_name, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    # Try PR title
    match = re.search(pattern, pr_title, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    return None


def validate_branch_naming(branch_name: str, project_key: str) -> Tuple[bool, str]:
    """
    Validate branch name contains Jira ticket.
    
    Flexible naming: Only requires the Jira ticket ID (e.g., SCRUM-123) to be present.
    Examples:
    - feature/SCRUM-123-description
    - bugfix/SCRUM-123-fix
    - SCRUM-123-my-feature
    - my-feature/SCRUM-123
    - personal/SCRUM-123-interest
    """
    # Remove refs/heads/ prefix if present
    branch_name = branch_name.replace('refs/heads/', '')
    
    # Check if it contains Jira ticket (this is the only requirement)
    pattern = rf'{project_key}-\d+'
    if not re.search(pattern, branch_name, re.IGNORECASE):
        return False, f"Branch name must contain Jira ticket ({project_key}-1234). Got: {branch_name}"
    
    return True, "Branch naming is valid"


def main():
    """Main execution function"""
    # Get environment variables
    jira_base_url = os.getenv('JIRA_BASE_URL')
    jira_username = os.getenv('JIRA_USER')  # Changed from JIRA_USERNAME to JIRA_USER
    jira_api_token = os.getenv('JIRA_API_TOKEN')
    jira_project_key = os.getenv('JIRA_PROJECT_KEY')
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('PR_NUMBER')
    github_ref = os.getenv('GITHUB_REF', '')
    
    # Validate required environment variables
    missing_vars = []
    if not jira_base_url:
        missing_vars.append('JIRA_BASE_URL')
    if not jira_username:
        missing_vars.append('JIRA_USER')
    if not jira_api_token:
        missing_vars.append('JIRA_API_TOKEN')
    if not jira_project_key:
        missing_vars.append('JIRA_PROJECT_KEY')
    if not github_token:
        missing_vars.append('GITHUB_TOKEN')
    if not github_repo:
        missing_vars.append('GITHUB_REPOSITORY')
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Normalize Jira base URL - add https:// if missing
    if jira_base_url and not jira_base_url.startswith('http'):
        jira_base_url = f"https://{jira_base_url}"
    
    # Initialize APIs
    github_api = GitHubAPI(github_token, github_repo)
    jira_api = JiraAPI(jira_base_url, jira_username, jira_api_token)
    
    # Get PR information
    if not pr_number:
        print("❌ PR_NUMBER not set. This script should run in PR context.")
        sys.exit(1)
    
    try:
        pr_data = github_api.get_pull_request(int(pr_number))
        branch_name = pr_data.get('head', {}).get('ref', '')
        pr_title = pr_data.get('title', '')
        pr_body = pr_data.get('body', '')
        
        print(f"📋 PR Title: {pr_title}")
        print(f"🌿 Branch: {branch_name}")
        
        # Validate branch naming
        branch_valid, branch_msg = validate_branch_naming(branch_name, jira_project_key)
        if not branch_valid:
            github_api.post_comment(
                int(pr_number),
                f"❌ **Branch Naming Validation Failed**\n\n{branch_msg}\n\n"
                f"**Required:** Branch name must contain Jira ticket ID ({jira_project_key}-1234)\n"
                f"**Examples:** `feature/{jira_project_key}-1234-description`, `{jira_project_key}-1234-my-feature`, `personal/{jira_project_key}-1234-interest`"
            )
            print(f"❌ {branch_msg}")
            sys.exit(1)
        
        # Extract Jira ticket
        ticket_id = extract_jira_ticket(branch_name, pr_title, jira_project_key)
        
        if not ticket_id:
            error_msg = (
                f"❌ **Jira Ticket Not Found**\n\n"
                f"Branch name or PR title must contain a Jira ticket ID ({jira_project_key}-1234).\n\n"
                f"- Branch: `{branch_name}`\n"
                f"- PR Title: `{pr_title}`"
            )
            github_api.post_comment(int(pr_number), error_msg)
            print(error_msg)
            sys.exit(1)
        
        print(f"🎫 Found Jira ticket: {ticket_id}")
        
        # Validate ticket exists and get status
        try:
            ticket = jira_api.get_ticket(ticket_id)
            ticket_status = ticket.get('fields', {}).get('status', {}).get('name', '')
            ticket_summary = ticket.get('fields', {}).get('summary', '')
            ticket_project = ticket.get('fields', {}).get('project', {}).get('key', '')
            
            print(f"📊 Ticket Status: {ticket_status}")
            print(f"📝 Ticket Summary: {ticket_summary}")
            
            # Validate project key matches
            if ticket_project.upper() != jira_project_key.upper():
                error_msg = (
                    f"❌ **Jira Project Mismatch**\n\n"
                    f"Ticket {ticket_id} belongs to project {ticket_project}, "
                    f"but expected project is {jira_project_key}."
                )
                github_api.post_comment(int(pr_number), error_msg)
                print(error_msg)
                sys.exit(1)
            
            # Check if status is allowed (case-insensitive)
            allowed_statuses = [
                'In Progress', 'IN PROGRESS', 'In Progress',
                'Ready for Review', 'READY FOR REVIEW',
                'In Review', 'IN REVIEW',
                'Code Review', 'CODE REVIEW',
                'To Do', 'TO DO', 'To Do',
                'Done', 'DONE'
            ]
            # Normalize status for comparison (case-insensitive)
            ticket_status_normalized = ticket_status.upper().strip()
            allowed_statuses_normalized = [s.upper().strip() for s in allowed_statuses]
            
            if ticket_status_normalized not in allowed_statuses_normalized:
                error_msg = (
                    f"❌ **Jira Ticket Status Not Allowed**\n\n"
                    f"Ticket {ticket_id} is in status '{ticket_status}', "
                    f"but must be in one of: TO DO, IN PROGRESS, IN REVIEW, READY FOR REVIEW, CODE REVIEW, or DONE.\n\n"
                    f"**Ticket Summary:** {ticket_summary}\n\n"
                    f"**Current Status:** {ticket_status}"
                )
                github_api.post_comment(int(pr_number), error_msg)
                print(error_msg)
                sys.exit(1)
            
            # Success - post positive comment
            success_msg = (
                f"✅ **Jira Validation Passed**\n\n"
                f"- **Ticket:** [{ticket_id}]({jira_api.get_ticket_url(ticket_id)}) - {ticket_summary}\n"
                f"- **Status:** {ticket_status}\n"
                f"- **Branch:** `{branch_name}`"
            )
            github_api.post_comment(int(pr_number), success_msg)
            print("✅ Jira validation passed")
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                error_msg = (
                    f"❌ **Jira Ticket Not Found**\n\n"
                    f"Ticket {ticket_id} does not exist in Jira."
                )
                github_api.post_comment(int(pr_number), error_msg)
                print(error_msg)
                sys.exit(1)
            else:
                error_msg = f"❌ Error accessing Jira API: {str(e)}"
                github_api.post_comment(int(pr_number), error_msg)
                print(error_msg)
                sys.exit(1)
        except Exception as e:
            error_msg = f"❌ Unexpected error during Jira validation: {str(e)}"
            github_api.post_comment(int(pr_number), error_msg)
            print(error_msg)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

