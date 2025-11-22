#!/usr/bin/env python3
"""Test file for PR Agent validation"""

def calculate_sum(a, b):
    """Calculate sum of two numbers."""
    print(f"Calculating: {a} + {b}")  # Debug statement - will be flagged
    return a + b

# TODO: Add error handling
# FIXME: This needs optimization

def main():
    result = calculate_sum(5, 3)
    return result

if __name__ == "__main__":
    main()

