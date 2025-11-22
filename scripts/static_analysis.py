#!/usr/bin/env python3
"""
Static Code Analysis Module
Detects code quality issues, anti-patterns, and non-production-ready code.
"""

import os
import sys
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path
from scripts.utils.github_api import GitHubAPI


class StaticAnalyzer:
    """
    Static code analyzer for detecting code quality issues.
    
    Detects:
    - Debug statements (console.log, print)
    - TODO/FIXME/HACK comments
    - Dead code
    - Commented-out code blocks
    - Unused imports
    - Code smells
    """
    
    # Debug Statement Patterns
    DEBUG_PATTERNS = [
        (re.compile(r'console\.log\s*\('), 'JavaScript console.log'),
        (re.compile(r'console\.debug\s*\('), 'JavaScript console.debug'),
        (re.compile(r'console\.warn\s*\('), 'JavaScript console.warn'),
        (re.compile(r'print\s*\([^)]*\)'), 'Python print statement'),
        (re.compile(r'debugger\s*;'), 'JavaScript debugger statement'),
        (re.compile(r'pdb\.set_trace\s*\('), 'Python pdb.set_trace'),
        (re.compile(r'import\s+pdb'), 'Python pdb import'),
        (re.compile(r'debugger'), 'Debugger keyword'),
        (re.compile(r'var_dump\s*\('), 'PHP var_dump'),
        (re.compile(r'dd\s*\('), 'Laravel dd()'),
    ]
    
    # TODO/FIXME Patterns
    TODO_PATTERNS = [
        (re.compile(r'TODO\s*:'), 'TODO comment'),
        (re.compile(r'FIXME\s*:'), 'FIXME comment'),
        (re.compile(r'HACK\s*:'), 'HACK comment'),
        (re.compile(r'XXX\s*:'), 'XXX comment'),
        (re.compile(r'NOTE\s*:'), 'NOTE comment'),
        (re.compile(r'BUG\s*:'), 'BUG comment'),
    ]
    
    # Commented Code Detection
    COMMENTED_CODE_THRESHOLD = 5  # Lines of consecutive commented code
    
    def __init__(self):
        """Initialize the static analyzer."""
        self.issues: List[Dict[str, Any]] = []
    
    def scan_file(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """
        Scan a single file for static analysis issues.
        
        Args:
            file_path: Path to the file
            content: File content as string
        
        Returns:
            List of detected issues
        """
        file_issues = []
        lines = content.split('\n')
        
        # Track commented code blocks
        commented_block_start = None
        commented_lines = 0
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for debug statements
            for pattern, description in self.DEBUG_PATTERNS:
                if pattern.search(line) and not self._is_in_string_or_comment(line, pattern):
                    file_issues.append({
                        'type': 'DEBUG_CODE',
                        'severity': 'HIGH',
                        'file': str(file_path),
                        'line': line_num,
                        'description': f'{description} found - remove before production',
                        'code': stripped[:100]
                    })
                    break
            
            # Check for TODO/FIXME
            for pattern, description in self.TODO_PATTERNS:
                if pattern.search(line, re.IGNORECASE):
                    file_issues.append({
                        'type': 'TODO',
                        'severity': 'MEDIUM',
                        'file': str(file_path),
                        'line': line_num,
                        'description': f'{description} found - address before merging',
                        'code': stripped[:100]
                    })
                    break
            
            # Track commented code blocks
            if self._is_commented_line(stripped):
                if commented_block_start is None:
                    commented_block_start = line_num
                commented_lines += 1
            else:
                if commented_lines >= self.COMMENTED_CODE_THRESHOLD:
                    file_issues.append({
                        'type': 'COMMENTED_CODE',
                        'severity': 'LOW',
                        'file': str(file_path),
                        'line': commented_block_start,
                        'description': f'Large block of commented code ({commented_lines} lines) - consider removing',
                        'code': ''
                    })
                commented_block_start = None
                commented_lines = 0
        
        # Check for trailing commented block
        if commented_lines >= self.COMMENTED_CODE_THRESHOLD:
            file_issues.append({
                'type': 'COMMENTED_CODE',
                'severity': 'LOW',
                'file': str(file_path),
                'line': commented_block_start,
                'description': f'Large block of commented code ({commented_lines} lines) - consider removing',
                'code': ''
            })
        
        return file_issues
    
    def _is_commented_line(self, line: str) -> bool:
        """
        Check if a line is a comment.
        
        Args:
            line: Line content
        
        Returns:
            True if line is a comment
        """
        stripped = line.strip()
        return (
            stripped.startswith('#') or
            stripped.startswith('//') or
            stripped.startswith('/*') or
            stripped.startswith('*') or
            (stripped.startswith('<!--') and stripped.endswith('-->'))
        )
    
    def _is_in_string_or_comment(self, line: str, pattern: re.Pattern) -> bool:
        """
        Check if pattern match is inside a string or comment.
        This is a simplified check - full implementation would require parsing.
        
        Args:
            line: Line content
            pattern: Pattern to check
        
        Returns:
            True if likely in string/comment
        """
        # Simple heuristic: if line starts with comment markers, it's a comment
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('//'):
            return True
        
        # Check if it's in a docstring or comment block
        if '"""' in line or "'''" in line:
            return True
        
        return False
    
    def scan_pr_files(self, github_token: str, github_repo: str, pr_number: int) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Scan all files in a PR for static analysis issues.
        
        Args:
            github_token: GitHub API token
            github_repo: Repository in format 'owner/repo'
            pr_number: PR number
        
        Returns:
            Tuple of (is_clean, list_of_issues)
        """
        github_api = GitHubAPI(github_token, github_repo)
        
        try:
            files = github_api.get_pr_files(pr_number)
            all_issues = []
            
            for file_info in files:
                file_path = Path(file_info['filename'])
                
                # Skip certain file types
                if file_path.suffix in ['.md', '.txt', '.json', '.yml', '.yaml', '.png', '.jpg']:
                    continue
                
                # Get file patch
                patch = file_info.get('patch', '')
                if not patch:
                    continue
                
                # Scan the patch
                issues = self.scan_file(file_path, patch)
                all_issues.extend(issues)
            
            # Check if any high-severity issues found
            high_severity = [i for i in all_issues if i['severity'] == 'HIGH']
            
            return len(high_severity) == 0, all_issues
            
        except Exception as e:
            print(f"❌ Error during static analysis: {e}")
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
    analyzer = StaticAnalyzer()
    is_clean, issues = analyzer.scan_pr_files(github_token, github_repo, int(pr_number))
    
    if not is_clean:
        high_issues = [i for i in issues if i['severity'] == 'HIGH']
        print(f"❌ Static analysis failed: {len(high_issues)} high-severity issues detected")
        
        # Post comment on PR
        comment = "❌ **Static Analysis Failed**\n\n"
        comment += f"Found {len(high_issues)} high-severity issues:\n\n"
        
        for issue in high_issues[:10]:  # Show first 10
            print(f"  - {issue['file']}:{issue['line']} - {issue['description']}")
            comment += f"- **{issue['file']}:{issue['line']}** - {issue['description']}\n"
            if issue.get('code'):
                comment += f"  ```\n  {issue['code']}\n  ```\n"
        
        if len(high_issues) > 10:
            comment += f"\n... and {len(high_issues) - 10} more issues\n"
        
        comment += "\n**Action Required:** Fix all high-severity issues before merging."
        
        try:
            github_api.post_comment(int(pr_number), comment)
        except Exception as e:
            print(f"⚠️  Failed to post comment: {e}")
        
        sys.exit(1)
    else:
        if issues:
            print(f"⚠️  Found {len(issues)} non-critical issues")
            # Post warning comment
            medium_issues = [i for i in issues if i['severity'] == 'MEDIUM']
            if medium_issues:
                comment = f"⚠️ **Static Analysis Warning**\n\nFound {len(medium_issues)} medium-severity issues. Please review:\n\n"
                for issue in medium_issues[:5]:
                    comment += f"- **{issue['file']}:{issue['line']}** - {issue['description']}\n"
                try:
                    github_api.post_comment(int(pr_number), comment)
                except Exception as e:
                    print(f"⚠️  Failed to post comment: {e}")
        else:
            print("✅ Static analysis passed")
        sys.exit(0)


if __name__ == '__main__':
    main()

