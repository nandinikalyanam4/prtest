#!/usr/bin/env python3
"""
File Scanner Utility
Utility functions for scanning repository files for patterns.
"""

import os
import re
from typing import List, Dict, Any, Pattern, Optional
from pathlib import Path


class FileScanner:
    """
    Utility class for scanning files in a repository.
    """
    
    # Default file extensions to scan
    DEFAULT_SCAN_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs',
        '.cpp', '.c', '.h', '.hpp', '.cs', '.php', '.rb', '.swift',
        '.kt', '.scala', '.sh', '.bash', '.zsh', '.yaml', '.yml'
    }
    
    # Default files/directories to ignore
    DEFAULT_IGNORE_PATTERNS = {
        '__pycache__', '.git', '.venv', 'venv', 'node_modules',
        '.pytest_cache', '.mypy_cache', 'dist', 'build', '.idea',
        '.vscode', '*.pyc', '*.pyo', '.DS_Store'
    }
    
    def __init__(
        self,
        root_dir: str = '.',
        scan_extensions: Optional[set] = None,
        ignore_patterns: Optional[set] = None
    ):
        """
        Initialize file scanner.
        
        Args:
            root_dir: Root directory to scan
            scan_extensions: Set of file extensions to scan (default: common code extensions)
            ignore_patterns: Set of patterns to ignore (default: common ignore patterns)
        """
        self.root_dir = Path(root_dir)
        self.scan_extensions = scan_extensions or self.DEFAULT_SCAN_EXTENSIONS
        self.ignore_patterns = ignore_patterns or self.DEFAULT_IGNORE_PATTERNS
    
    def get_files(self) -> List[Path]:
        """
        Get all files to scan.
        
        Returns:
            List of file paths
        """
        files = []
        
        for root, dirs, filenames in os.walk(self.root_dir):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(d)]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Check if file should be ignored
                if self._should_ignore_file(file_path):
                    continue
                
                # Check if extension is in scan list
                if file_path.suffix in self.scan_extensions:
                    files.append(file_path)
        
        return files
    
    def _should_ignore(self, name: str) -> bool:
        """
        Check if a directory/file name should be ignored.
        
        Args:
            name: Directory or file name
        
        Returns:
            True if should be ignored
        """
        for pattern in self.ignore_patterns:
            if pattern in name or name.startswith('.'):
                return True
        return False
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """
        Check if a file should be ignored.
        
        Args:
            file_path: Path to file
        
        Returns:
            True if should be ignored
        """
        # Check if any part of the path matches ignore patterns
        for part in file_path.parts:
            if self._should_ignore(part):
                return True
        
        return False
    
    def scan_for_patterns(
        self,
        patterns: List[tuple[Pattern, str]],
        files: Optional[List[Path]] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan files for regex patterns.
        
        Args:
            patterns: List of (pattern, description) tuples
            files: Optional list of files to scan (default: all files)
        
        Returns:
            List of matches found
        """
        if files is None:
            files = self.get_files()
        
        matches = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        for pattern, description in patterns:
                            if pattern.search(line):
                                matches.append({
                                    'file': str(file_path),
                                    'line': line_num,
                                    'description': description,
                                    'code': line.strip()[:200]
                                })
                                break  # Only report first match per line
            except Exception as e:
                # Skip files that can't be read
                continue
        
        return matches
    
    def scan_for_strings(
        self,
        strings: List[str],
        case_sensitive: bool = False,
        files: Optional[List[Path]] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan files for specific strings.
        
        Args:
            strings: List of strings to search for
            files: Optional list of files to scan
            case_sensitive: Whether search should be case sensitive
        
        Returns:
            List of matches found
        """
        if files is None:
            files = self.get_files()
        
        matches = []
        flags = 0 if case_sensitive else re.IGNORECASE
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        for search_string in strings:
                            pattern = re.compile(re.escape(search_string), flags)
                            if pattern.search(line):
                                matches.append({
                                    'file': str(file_path),
                                    'line': line_num,
                                    'description': f'Found: {search_string}',
                                    'code': line.strip()[:200]
                                })
                                break
            except Exception as e:
                continue
        
        return matches


def scan_repository(
    root_dir: str = '.',
    patterns: Optional[List[tuple[Pattern, str]]] = None
) -> List[Dict[str, Any]]:
    """
    Convenience function to scan a repository.
    
    Args:
        root_dir: Root directory to scan
        patterns: Optional list of (pattern, description) tuples
    
    Returns:
        List of matches found
    """
    scanner = FileScanner(root_dir)
    
    if patterns:
        return scanner.scan_for_patterns(patterns)
    else:
        return []


if __name__ == '__main__':
    # Example usage
    scanner = FileScanner('.')
    files = scanner.get_files()
    print(f"Found {len(files)} files to scan")
    
    # Example: scan for TODO comments
    todo_pattern = re.compile(r'TODO\s*:', re.IGNORECASE)
    matches = scanner.scan_for_patterns([(todo_pattern, 'TODO comment')])
    print(f"Found {len(matches)} TODO comments")

