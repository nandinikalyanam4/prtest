#!/usr/bin/env python3
"""
This file has LOTS of mistakes for testing PR Agent
"""

# Hardcoded secrets - BAD!
api_key = "sk_live_51H3ll0W0rld1234567890"
password = "super_secret_password_123"
aws_access_key = "AKIAIOSFODNN7EXAMPLE"
aws_secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# Debug statements - should not be in production
print("Debug: Starting authentication")
print(f"User ID: {user_id}")  # This will cause an error too
console.log("This is JavaScript but we're in Python!")
debugger  # Another debug statement

# TODO comments - unfinished work
# TODO: Add proper error handling
# TODO: Implement rate limiting
# FIXME: This function is broken
# HACK: Temporary workaround, needs proper fix
# XXX: This is dangerous code

def authenticate_user(username, password):
    """Authenticate user - but has security issues"""
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    # Missing input validation
    # No error handling
    return True

def process_payment(amount, card_number):
    """Process payment - has multiple issues"""
    print(f"Processing payment of ${amount}")  # Debug statement
    # TODO: Add encryption
    # Hardcoded API key
    stripe_key = "sk_test_1234567890abcdef"
    
    # No validation
    # No error handling
    # Logging sensitive data
    print(f"Card number: {card_number}")
    
    return True

# Large block of commented out code - should be removed
# def old_function():
#     """This function is no longer used"""
#     result = 0
#     for i in range(100):
#         result += i
#     return result
# 
# def another_old_function():
#     """Also not used"""
#     pass
# 
# def yet_another():
#     """Dead code"""
#     return None

# Missing error handling
def divide_numbers(a, b):
    """Divide two numbers - no error handling!"""
    return a / b  # Will crash if b is 0

# Hardcoded credentials
database_password = "admin123"
db_host = "localhost"
db_user = "root"
db_pass = "password"

# Exposed private key
private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdef
-----END RSA PRIVATE KEY-----"""

# Test data in production code
test_api_key = "test_key_12345"
mock_password = "test123"

# Insecure random
import random
session_token = random.randint(1000, 9999)  # Not cryptographically secure!

# Missing type hints
def process_data(data):
    # No type checking
    # No validation
    return data.upper()

# Unused imports (if we had them)
# import os
# import sys

# Bad variable names
x = 10
y = 20
z = x + y

# Missing docstrings for complex functions
def complex_calculation(a, b, c, d, e):
    result = (a * b) + (c / d) - e
    return result

# Swallowed exceptions
try:
    risky_operation()
except:
    pass  # Silently ignore errors - BAD!

# Generic error messages
try:
    another_risky_operation()
except Exception as e:
    print("Error occurred")  # Not helpful!

# Hardcoded URLs
api_endpoint = "http://api.example.com/v1/data"  # Should use environment variable

# Missing input sanitization
def search(query):
    """Search function - vulnerable to injection"""
    # No sanitization
    # Direct use of user input
    return f"Searching for: {query}"

if __name__ == "__main__":
    # More debug statements
    print("Application starting...")
    print("Debug mode enabled")
    
    # Call functions with issues
    authenticate_user("admin", "password")
    process_payment(100, "4111111111111111")
    divide_numbers(10, 0)  # Will crash!


