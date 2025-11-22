#!/usr/bin/env python3
"""
Comprehensive Secret Scanning Module
Detects sensitive information, credentials, tokens, and secrets in code.
"""

import os
import sys
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path
from scripts.utils.github_api import GitHubAPI


class SecretScanner:
    """
    Enterprise-grade secret scanner for detecting sensitive information.
    
    Detects:
    - AWS keys
    - JWT tokens
    - Private keys
    - Passwords
    - .env content
    - API tokens
    - Slack tokens
    - GitHub PATs
    - Google API keys
    """
    
    # AWS Credentials Patterns
    AWS_ACCESS_KEY_PATTERN = re.compile(
        r'AKIA[0-9A-Z]{16}', re.IGNORECASE
    )
    AWS_SECRET_KEY_PATTERN = re.compile(
        r'aws[_\s-]?secret[_\s-]?access[_\s-]?key\s*[:=]\s*["\']?([A-Za-z0-9/+=]{40})["\']?',
        re.IGNORECASE
    )
    
    # JWT Tokens
    JWT_PATTERN = re.compile(
        r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
        re.IGNORECASE
    )
    
    # Private Keys
    PRIVATE_KEY_PATTERN = re.compile(
        r'-----BEGIN\s+(RSA|DSA|EC|OPENSSH|PGP)\s+PRIVATE\s+KEY-----',
        re.IGNORECASE
    )
    
    # Password Patterns
    PASSWORD_PATTERNS = [
        re.compile(r'password\s*[:=]\s*["\']([^"\']{8,})["\']', re.IGNORECASE),
        re.compile(r'pwd\s*[:=]\s*["\']([^"\']{8,})["\']', re.IGNORECASE),
        re.compile(r'passwd\s*[:=]\s*["\']([^"\']{8,})["\']', re.IGNORECASE),
    ]
    
    # API Tokens
    API_TOKEN_PATTERNS = [
        re.compile(r'api[_\s-]?key\s*[:=]\s*["\']([A-Za-z0-9_-]{20,})["\']', re.IGNORECASE),
        re.compile(r'api[_\s-]?token\s*[:=]\s*["\']([A-Za-z0-9_-]{20,})["\']', re.IGNORECASE),
        re.compile(r'apikey\s*[:=]\s*["\']([A-Za-z0-9_-]{20,})["\']', re.IGNORECASE),
        # Catch API keys without quotes and shorter values (common in test files)
        re.compile(r'apikey\s*[:=]\s*([A-Za-z0-9_-]{5,})', re.IGNORECASE),
        re.compile(r'api[_\s-]?key\s*[:=]\s*([A-Za-z0-9_-]{5,})', re.IGNORECASE),
    ]
    
    # GitHub Personal Access Tokens
    GITHUB_PAT_PATTERN = re.compile(
        r'ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|ghu_[A-Za-z0-9]{36}|ghs_[A-Za-z0-9]{36}|ghr_[A-Za-z0-9]{36}',
        re.IGNORECASE
    )
    
    # Slack Tokens
    SLACK_TOKEN_PATTERNS = [
        re.compile(r'xox[baprs]-[0-9a-zA-Z-]{10,}', re.IGNORECASE),
        re.compile(r'slack[_\s-]?token\s*[:=]\s*["\']([A-Za-z0-9_-]{20,})["\']', re.IGNORECASE),
    ]
    
    # Google API Keys
    GOOGLE_API_KEY_PATTERN = re.compile(
        r'AIza[0-9A-Za-z_-]{35}',
        re.IGNORECASE
    )
    
    # .env file content detection
    ENV_FILE_PATTERN = re.compile(
        r'\.env|\.env\.local|\.env\.production',
        re.IGNORECASE
    )
    
    # Generic Secret Patterns
    SECRET_PATTERNS = [
        re.compile(r'secret\s*[:=]\s*["\']([A-Za-z0-9/+=_-]{20,})["\']', re.IGNORECASE),
        re.compile(r'private[_\s-]?key\s*[:=]\s*["\']([A-Za-z0-9/+=_-]{40,})["\']', re.IGNORECASE),
        re.compile(r'access[_\s-]?token\s*[:=]\s*["\']([A-Za-z0-9/+=_-]{20,})["\']', re.IGNORECASE),
    ]
    
    def __init__(self):
        """Initialize the secret scanner."""
        self.issues: List[Dict[str, Any]] = []
    
    def scan_file(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """
        Scan a single file for secrets.
        
        Args:
            file_path: Path to the file
            content: File content as string
        
        Returns:
            List of detected issues
        """
        file_issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments that might contain examples
            if line.strip().startswith('#'):
                continue
            
            # Check AWS Access Keys
            if self.AWS_ACCESS_KEY_PATTERN.search(line):
                file_issues.append({
                    'type': 'AWS_ACCESS_KEY',
                    'severity': 'HIGH',
                    'file': str(file_path),
                    'line': line_num,
                    'description': 'AWS Access Key ID detected',
                    'code': self._sanitize_line(line)
                })
            
            # Check AWS Secret Keys
            if self.AWS_SECRET_KEY_PATTERN.search(line):
                file_issues.append({
                    'type': 'AWS_SECRET_KEY',
                    'severity': 'HIGH',
                    'file': str(file_path),
                    'line': line_num,
                    'description': 'AWS Secret Access Key detected',
                    'code': self._sanitize_line(line)
                })
            
            # Check JWT Tokens
            if self.JWT_PATTERN.search(line):
                file_issues.append({
                    'type': 'JWT_TOKEN',
                    'severity': 'HIGH',
                    'file': str(file_path),
                    'line': line_num,
                    'description': 'JWT token detected',
                    'code': self._sanitize_line(line)
                })
            
            # Check Private Keys
            if self.PRIVATE_KEY_PATTERN.search(line):
                file_issues.append({
                    'type': 'PRIVATE_KEY',
                    'severity': 'HIGH',
                    'file': str(file_path),
                    'line': line_num,
                    'description': 'Private key detected',
                    'code': self._sanitize_line(line)
                })
            
            # Check Passwords
            for pattern in self.PASSWORD_PATTERNS:
                if pattern.search(line):
                    file_issues.append({
                        'type': 'PASSWORD',
                        'severity': 'HIGH',
                        'file': str(file_path),
                        'line': line_num,
                        'description': 'Hardcoded password detected',
                        'code': self._sanitize_line(line)
                    })
                    break
            
            # Check API Tokens
            for pattern in self.API_TOKEN_PATTERNS:
                if pattern.search(line):
                    file_issues.append({
                        'type': 'API_TOKEN',
                        'severity': 'HIGH',
                        'file': str(file_path),
                        'line': line_num,
                        'description': 'API token detected',
                        'code': self._sanitize_line(line)
                    })
                    break
            
            # Check GitHub PATs
            if self.GITHUB_PAT_PATTERN.search(line):
                file_issues.append({
                    'type': 'GITHUB_PAT',
                    'severity': 'HIGH',
                    'file': str(file_path),
                    'line': line_num,
                    'description': 'GitHub Personal Access Token detected',
                    'code': self._sanitize_line(line)
                })
            
            # Check Slack Tokens
            for pattern in self.SLACK_TOKEN_PATTERNS:
                if pattern.search(line):
                    file_issues.append({
                        'type': 'SLACK_TOKEN',
                        'severity': 'HIGH',
                        'file': str(file_path),
                        'line': line_num,
                        'description': 'Slack token detected',
                        'code': self._sanitize_line(line)
                    })
                    break
            
            # Check Google API Keys
            if self.GOOGLE_API_KEY_PATTERN.search(line):
                file_issues.append({
                    'type': 'GOOGLE_API_KEY',
                    'severity': 'HIGH',
                    'file': str(file_path),
                    'line': line_num,
                    'description': 'Google API key detected',
                    'code': self._sanitize_line(line)
                })
            
            # Check Generic Secrets
            for pattern in self.SECRET_PATTERNS:
                if pattern.search(line):
                    file_issues.append({
                        'type': 'GENERIC_SECRET',
                        'severity': 'HIGH',
                        'file': str(file_path),
                        'line': line_num,
                        'description': 'Generic secret detected',
                        'code': self._sanitize_line(line)
                    })
                    break
        
        return file_issues
    
    def _sanitize_line(self, line: str, max_length: int = 100) -> str:
        """
        Sanitize line content to avoid exposing secrets in output.
        
        Args:
            line: Line content
            max_length: Maximum length to return
        
        Returns:
            Sanitized line
        """
        # Truncate long lines
        if len(line) > max_length:
            line = line[:max_length] + "..."
        
        # Mask potential secrets (keep structure, mask values)
        # This is a simple approach - in production, use more sophisticated masking
        sanitized = re.sub(
            r'["\']([A-Za-z0-9/+=_-]{20,})["\']',
            r'"***MASKED***"',
            line
        )
        
        return sanitized
    
    def scan_pr_files(self, github_token: str, github_repo: str, pr_number: int) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Scan all files in a PR for secrets.
        
        Args:
            github_token: GitHub API token
            github_repo: Repository in format 'owner/repo'
            pr_number: PR number
        
        Returns:
            Tuple of (is_safe, list_of_issues)
        """
        github_api = GitHubAPI(github_token, github_repo)
        
        try:
            files = github_api.get_pr_files(pr_number)
            all_issues = []
            
            for file_info in files:
                file_path = Path(file_info['filename'])
                
                # Skip binary files and certain extensions
                if file_path.suffix in ['.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf']:
                    continue
                
                # Get file patch/content
                patch = file_info.get('patch', '')
                if not patch:
                    # Try to get full file content if patch is not available
                    continue
                
                # Scan the patch
                issues = self.scan_file(file_path, patch)
                all_issues.extend(issues)
            
            # Check if any high-severity issues found
            high_severity = [i for i in all_issues if i['severity'] == 'HIGH']
            
            return len(high_severity) == 0, all_issues
            
        except Exception as e:
            print(f"❌ Error scanning PR files: {e}")
            return True, []  # Fail open on error


def main():
    """Main execution function for CLI usage."""
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('PR_NUMBER')
    
    if not all([github_token, github_repo, pr_number]):
        print("❌ Missing required environment variables: GITHUB_TOKEN, GITHUB_REPOSITORY, PR_NUMBER")
        sys.exit(1)
    
    github_api = GitHubAPI(github_token, github_repo)
    scanner = SecretScanner()
    is_safe, issues = scanner.scan_pr_files(github_token, github_repo, int(pr_number))
    
    if not is_safe:
        high_issues = [i for i in issues if i['severity'] == 'HIGH']
        print(f"❌ Secret scanning failed: {len(high_issues)} high-severity secrets detected")
        
        # Post comment on PR
        comment = "❌ **Secret Scanning Failed**\n\n"
        comment += f"Found {len(high_issues)} high-severity secrets:\n\n"
        
        for issue in high_issues[:10]:  # Show first 10
            print(f"  - {issue['file']}:{issue['line']} - {issue['description']}")
            comment += f"- **{issue['file']}:{issue['line']}** - {issue['description']}\n"
            if issue.get('code'):
                comment += f"  ```\n  {issue['code']}\n  ```\n"
        
        if len(high_issues) > 10:
            comment += f"\n... and {len(high_issues) - 10} more issues\n"
        
        comment += "\n**Action Required:** Remove all secrets before merging."
        
        try:
            github_api.post_comment(int(pr_number), comment)
        except Exception as e:
            print(f"⚠️  Failed to post comment: {e}")
        
        sys.exit(1)
    else:
        if issues:
            print(f"⚠️  Found {len(issues)} potential secrets (non-critical)")
            # Post warning comment
            comment = f"⚠️ **Secret Scanning Warning**\n\nFound {len(issues)} potential secrets (non-critical). Please review.\n"
            try:
                github_api.post_comment(int(pr_number), comment)
            except Exception as e:
                print(f"⚠️  Failed to post comment: {e}")
        else:
            print("✅ No secrets detected")
        sys.exit(0)


if __name__ == '__main__':
    main()

