#!/usr/bin/env python3
"""
Analysis Helper Utilities
Contains helper functions for code analysis and production readiness checks.
"""

import os
import sys
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path
from scripts.utils.github_api import GitHubAPI


# Patterns to detect issues
DEBUG_PATTERNS = [
    (r'console\.log\(', 'JavaScript console.log'),
    (r'print\s*\(', 'Python print statement'),
    (r'debugger\s*;', 'JavaScript debugger statement'),
    (r'pdb\.set_trace\(', 'Python pdb debugger'),
    (r'import pdb', 'Python pdb import'),
    (r'debugger', 'Debugger keyword'),
]

TODO_PATTERNS = [
    (r'TODO:', 'TODO comment'),
    (r'FIXME:', 'FIXME comment'),
    (r'HACK:', 'HACK comment'),
    (r'XXX:', 'XXX comment'),
    (r'NOTE:', 'NOTE comment'),
]

SECRET_PATTERNS = [
    (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
    (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
    (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret'),
    (r'token\s*=\s*["\'][^"\']+["\']', 'Hardcoded token'),
    (r'aws[_-]?access[_-]?key', 'AWS access key'),
    (r'aws[_-]?secret[_-]?key', 'AWS secret key'),
    (r'BEGIN\s+(RSA|DSA|EC|OPENSSH)\s+PRIVATE\s+KEY', 'Private key'),
]

COMMENTED_CODE_THRESHOLD = 10  # Lines of consecutive commented code


def check_branch_name() -> Tuple[bool, str]:
    """
    Check if branch name contains Jira ticket.
    
    Flexible naming: Only requires the Jira ticket ID to be present.
    Examples: feature/PROJ-1234-description, PROJ-1234-my-feature, personal/PROJ-1234-interest
    """
    github_ref = os.getenv('GITHUB_REF', '')
    if not github_ref:
        return False, "GITHUB_REF not set"
    
    # Remove refs/heads/ prefix
    branch_name = github_ref.replace('refs/heads/', '')
    
    # Check if it contains a ticket pattern (PROJ-1234)
    ticket_pattern = r'[A-Z]+-\d+'
    if not re.search(ticket_pattern, branch_name):
        return False, f"Branch name must contain a ticket ID (e.g., SCRUM-1234). Got: {branch_name}"
    
    return True, "Branch naming is valid"


def scan_file_for_issues(file_path: Path, content: str) -> List[Dict[str, Any]]:
    """
    Scan a file for production readiness issues.
    
    Returns:
        List of issues found
    """
    issues = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # Check for debug patterns
        for pattern, description in DEBUG_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append({
                    'type': 'DEBUG_CODE',
                    'severity': 'HIGH',
                    'file': str(file_path),
                    'line': line_num,
                    'description': f'{description} found',
                    'code': line.strip()
                })
        
        # Check for TODO/FIXME patterns
        for pattern, description in TODO_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append({
                    'type': 'TODO',
                    'severity': 'MEDIUM',
                    'file': str(file_path),
                    'line': line_num,
                    'description': f'{description} found',
                    'code': line.strip()
                })
        
        # Check for secret patterns
        for pattern, description in SECRET_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append({
                    'type': 'SECRET',
                    'severity': 'HIGH',
                    'file': str(file_path),
                    'line': line_num,
                    'description': f'{description} found',
                    'code': line.strip()[:100]  # Truncate for security
                })
    
    # Check for large commented code blocks
    commented_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
            commented_lines += 1
        else:
            commented_lines = 0
        
        if commented_lines >= COMMENTED_CODE_THRESHOLD:
            issues.append({
                'type': 'COMMENTED_CODE',
                'severity': 'LOW',
                'file': str(file_path),
                'line': line_num,
                'description': f'Large block of commented code ({commented_lines} lines)',
                'code': ''
            })
            commented_lines = 0
    
    return issues


def check_production_ready() -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Check if code is production-ready by scanning changed files.
    
    Returns:
        Tuple of (is_ready, list_of_issues)
    """
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('PR_NUMBER')
    
    if not all([github_token, github_repo, pr_number]):
        print("⚠️  Missing GitHub environment variables, skipping production checks")
        return True, []
    
    github_api = GitHubAPI(github_token, github_repo)
    
    try:
        # Get changed files
        files = github_api.get_pr_files(int(pr_number))
        all_issues = []
        
        for file_info in files:
            file_path = Path(file_info['filename'])
            
            # Skip certain file types
            if file_path.suffix in ['.md', '.txt', '.json', '.yml', '.yaml']:
                continue
            
            # Get file content (patch)
            patch = file_info.get('patch', '')
            if not patch:
                continue
            
            # Scan patch for issues
            issues = scan_file_for_issues(file_path, patch)
            all_issues.extend(issues)
        
        # Check for high-severity issues
        high_severity = [i for i in all_issues if i['severity'] == 'HIGH']
        
        if high_severity:
            return False, all_issues
        else:
            return True, all_issues
            
    except Exception as e:
        print(f"⚠️  Error during production checks: {e}")
        return True, []  # Fail open on error


def aggregate_results() -> None:
    """Aggregate all check results and post summary comment"""
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('PR_NUMBER')
    
    if not all([github_token, github_repo, pr_number]):
        return
    
    github_api = GitHubAPI(github_token, github_repo)
    
    # Get results from environment
    results = {
        'gitleaks': os.getenv('GITLEAKS_RESULT', 'unknown'),
        'linting': os.getenv('LINTING_RESULT', 'unknown'),
        'semgrep': os.getenv('SEMGREP_RESULT', 'unknown'),
        'jira': os.getenv('JIRA_RESULT', 'unknown'),
        'ai_review': os.getenv('AI_REVIEW_RESULT', 'unknown'),
        'production_checks': os.getenv('PRODUCTION_CHECKS_RESULT', 'unknown'),
    }
    
    # Build summary comment
    comment = "## 📊 PR Agent Review Summary\n\n"
    
    status_emoji = {
        'success': '✅',
        'failure': '❌',
        'unknown': '⚠️'
    }
    
    for check_name, result in results.items():
        emoji = status_emoji.get(result, '⚠️')
        status = result.upper()
        comment += f"{emoji} **{check_name.replace('_', ' ').title()}**: {status}\n"
    
    comment += "\n---\n*Review completed by PR Agent*"
    
    try:
        github_api.post_comment(int(pr_number), comment)
    except Exception as e:
        print(f"⚠️  Failed to post summary comment: {e}")


def main():
    """Main entry point for CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PR Agent Analysis Helpers')
    parser.add_argument('--check-branch-name', action='store_true', help='Check branch naming')
    parser.add_argument('--check-production-ready', action='store_true', help='Check production readiness')
    parser.add_argument('--aggregate-results', action='store_true', help='Aggregate and post results')
    
    args = parser.parse_args()
    
    if args.check_branch_name:
        is_valid, message = check_branch_name()
        if is_valid:
            print(f"✅ {message}")
            sys.exit(0)
        else:
            print(f"❌ {message}")
            sys.exit(1)
    
    elif args.check_production_ready:
        is_ready, issues = check_production_ready()
        if is_ready:
            print("✅ Production readiness checks passed")
            if issues:
                print(f"⚠️  Found {len(issues)} non-critical issues")
            sys.exit(0)
        else:
            high_issues = [i for i in issues if i['severity'] == 'HIGH']
            print(f"❌ Production readiness checks failed: {len(high_issues)} high-severity issues found")
            for issue in high_issues[:5]:  # Show first 5
                print(f"  - {issue['file']}:{issue['line']} - {issue['description']}")
            sys.exit(1)
    
    elif args.aggregate_results:
        aggregate_results()
        sys.exit(0)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()

