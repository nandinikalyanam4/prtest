# Example: Failing PR

This document demonstrates what happens when a PR fails PR Agent validation.

## PR Details

- **Branch:** `feature/PROJ-1234-add-user-auth`
- **PR Title:** `Add user authentication feature`
- **Author:** Developer

---

## ❌ PR Agent Review Results

### Step 1: Secret Scanning ❌ FAILED

**Gitleaks Detection:**
```
❌ Found AWS Access Key: AKIAIOSFODNN7EXAMPLE
   File: src/config.py, Line: 42
```

**Custom Secret Scanner:**
```
❌ Found hardcoded API key
   File: src/api/client.py, Line: 15
   Code: api_key = "sk_live_51H3ll0W0rld1234567890"
```

**Result:** PR BLOCKED - Secrets detected

---

### Step 2: Static Code Analysis ❌ FAILED

**Issues Found:**
```
❌ Debug statement found
   File: src/auth.py, Line: 78
   Code: console.log("User logged in:", user.id)

❌ TODO comment found
   File: src/auth.py, Line: 95
   Code: // TODO: Add rate limiting

❌ FIXME comment found
   File: src/database.py, Line: 23
   Code: # FIXME: This query is slow, optimize later
```

**Result:** PR BLOCKED - Debug code and TODOs found

---

### Step 3: Jira Validation ❌ FAILED

**Issues:**
```
❌ Jira Ticket Status Not Allowed

Ticket PROJ-1234 is in status "Backlog", 
but must be in one of: In Progress, Ready for Review, In Review, Code Review

Current Status: Backlog
Required Status: In Progress or Ready for Review
```

**Result:** PR BLOCKED - Jira ticket not in valid status

---

### Step 4: AI Review ❌ FAILED

**PR-Guardian Analysis:**

```json
{
  "decision": "FAIL",
  "severity": "HIGH",
  "risk_level": "CRITICAL",
  "issues": [
    {
      "type": "SECURITY",
      "severity": "HIGH",
      "file": "src/auth.py",
      "line": 45,
      "description": "SQL injection vulnerability detected in user query",
      "code_snippet": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
      "impact": "Critical security vulnerability - allows arbitrary SQL execution"
    },
    {
      "type": "PRODUCTION_READINESS",
      "severity": "HIGH",
      "file": "src/config.py",
      "line": 12,
      "description": "Hardcoded credentials in production code",
      "code_snippet": "password = 'admin123'",
      "impact": "Security risk - credentials exposed in codebase"
    },
    {
      "type": "QUALITY",
      "severity": "MEDIUM",
      "file": "src/auth.py",
      "line": 78,
      "description": "Missing error handling for authentication failure",
      "code_snippet": "user = authenticate(username, password)",
      "impact": "Application may crash on invalid credentials"
    }
  ],
  "suggestions": [
    "Use parameterized queries to prevent SQL injection",
    "Move credentials to environment variables",
    "Add try-catch blocks for error handling",
    "Remove debug console.log statements",
    "Address TODO/FIXME comments before merging"
  ],
  "summary": "Critical security vulnerabilities and production readiness issues detected. PR must not be merged until all HIGH severity issues are resolved."
}
```

**Result:** PR BLOCKED - High-severity issues detected

---

## 📊 Summary

| Check | Status | Issues Found |
|-------|--------|--------------|
| Secret Scanning | ❌ FAIL | 2 secrets detected |
| Static Analysis | ❌ FAIL | 3 debug/TODO issues |
| Jira Validation | ❌ FAIL | Ticket in wrong status |
| AI Review | ❌ FAIL | 3 high-severity issues |
| **Overall** | **❌ BLOCKED** | **PR cannot be merged** |

---

## 💬 PR Comments Posted

### Comment 1: Secret Scanning Results
```
❌ Secret Scanning Failed

Found 2 high-severity secrets:
- src/config.py:42 - AWS Access Key detected
- src/api/client.py:15 - Hardcoded API key detected

Please remove all secrets and use environment variables or secrets management.
```

### Comment 2: Static Analysis Results
```
❌ Static Analysis Failed

Found 3 issues:
- src/auth.py:78 - Debug console.log statement
- src/auth.py:95 - TODO comment
- src/database.py:23 - FIXME comment

Please remove debug code and address TODOs before merging.
```

### Comment 3: Jira Validation Results
```
❌ Jira Validation Failed

Ticket PROJ-1234 is in status "Backlog".
Required status: "In Progress" or "Ready for Review"

Please update the Jira ticket status before merging.
```

### Comment 4: AI Review Results
```
❌ AI Code Review Results

Decision: FAIL
Severity: HIGH
Risk Level: CRITICAL

## 🔍 Issues Found

### 🔴 High Severity
- src/auth.py:45 - SQL injection vulnerability detected
- src/config.py:12 - Hardcoded credentials in production code

### 🟡 Medium Severity
- src/auth.py:78 - Missing error handling for authentication failure

## 💡 Suggestions
- Use parameterized queries to prevent SQL injection
- Move credentials to environment variables
- Add try-catch blocks for error handling
```

---

## 🚫 Final Status

**PR Status:** ❌ **FAILED - BLOCKED FROM MERGE**

**Required Actions:**
1. Remove all secrets and use environment variables
2. Remove debug code (console.log, TODO, FIXME)
3. Update Jira ticket status to "In Progress"
4. Fix SQL injection vulnerability
5. Add proper error handling
6. Address all high-severity issues

**Next Steps:**
- Developer must fix all issues
- Resubmit PR for review
- All checks must pass before merge

