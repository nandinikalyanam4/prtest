# PR Agent Testing Guide

This guide will walk you through testing your PR Agent setup step by step.

## Prerequisites

Before testing, ensure you have:

- ✅ GitHub repository with Actions enabled
- ✅ All GitHub Secrets configured (see below)
- ✅ A valid Jira ticket in your project (e.g., `SCRUM-1`, `SCRUM-2`, etc.)
- ✅ The Jira ticket should be in status: "TO DO", "IN PROGRESS", "IN REVIEW", "READY FOR REVIEW", "CODE REVIEW", or "DONE" (case-insensitive)

## Step 1: Configure GitHub Secrets

Go to your repository: **Settings → Secrets and variables → Actions**

Add/verify these secrets:

| Secret Name | Value |
|------------|-------|
| `JIRA_BASE_URL` | `kalyanamnandini.atlassian.net` |
| `JIRA_USER` | `kalyanamnandini786.gmail.com` |
| `JIRA_API_TOKEN` | Your Jira API token (generate from Jira settings) |
| `JIRA_PROJECT_KEY` | `SCRUM` |
| `OPENAI_API_KEY` | Your OpenAI API key (starts with `sk-`) |

**Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions.

## Step 2: Create a Test Branch

Create a branch that follows the naming convention:

```bash
# Make sure you're on the main/master branch
git checkout main  # or master

# Create a new branch with Jira ticket in the name
# Replace SCRUM-123 with an actual ticket number from your Jira
git checkout -b feature/SCRUM-123-test-pr-agent
```

**Important:** 
- Branch name must contain a valid Jira ticket ID (e.g., `SCRUM-123`)
- You can use any naming format you prefer (e.g., `feature/SCRUM-123-description`, `SCRUM-123-my-feature`, `personal/SCRUM-123-interest`)
- The ticket must exist in Jira and be in an allowed status (TO DO, IN PROGRESS, IN REVIEW, READY FOR REVIEW, CODE REVIEW, or DONE)

## Step 3: Make Some Test Changes

Add some test code to trigger the PR Agent:

```bash
# Create a test file
cat > test_file.py << 'EOF'
#!/usr/bin/env python3
"""Test file for PR Agent"""

def hello_world():
    print("Hello, World!")  # This will be flagged by static analysis
    return "test"

# TODO: Add more functionality
# FIXME: This needs improvement
EOF

# Add and commit
git add test_file.py
git commit -m "Add test file for PR Agent validation"
```

## Step 4: Push and Create Pull Request

```bash
# Push the branch
git push origin feature/SCRUM-123-test-pr-agent
```

Then:
1. Go to your GitHub repository
2. Click **"Pull requests"** tab
3. Click **"New pull request"**
4. Select your branch: `feature/SCRUM-123-test-pr-agent`
5. **PR Title should include the Jira ticket**: `[SCRUM-123] Test PR Agent`
6. Add a description (optional)
7. Click **"Create pull request"**

## Step 5: Monitor the Workflow

1. After creating the PR, go to the **"Actions"** tab in your repository
2. You should see a workflow run: **"PR Agent - Automated Code Review"**
3. Click on it to see the progress
4. The workflow will run these checks in sequence:
   - ✅ Checkout code
   - 🔒 Secret Scanning (Gitleaks)
   - 🔒 Custom Secret Scanning
   - 📊 Static Code Analysis
   - 🎫 Jira Validation
   - 🤖 AI Code Review
   - 📊 Post Summary Comment

## Step 6: Check PR Comments

Go back to your Pull Request and check the comments section. You should see:

1. **Jira Validation Comment** - Confirms ticket is valid
2. **Static Analysis Comment** - Flags the `print()` statement and TODO/FIXME
3. **AI Review Comment** - AI-powered code review
4. **Summary Comment** - Overall status of all checks

### Expected Results

**What Should Happen:**

✅ **Jira Validation**: Should pass if ticket exists and is in correct status  
⚠️ **Static Analysis**: Should flag the `print()` statement and TODO/FIXME comments  
✅ **Secret Scanning**: Should pass (no secrets in test file)  
✅ **AI Review**: Should provide suggestions about the code quality issues  

**The PR might show as "failed"** because of the debug code (`print`) and TODO comments - this is expected! The PR Agent is working correctly.

## Step 7: Test with a Clean PR

To test a passing PR:

1. Create a new branch: `feature/SCRUM-124-clean-code`
2. Add clean code without debug statements:

```python
#!/usr/bin/env python3
"""Clean test file"""

def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b

def main():
    """Main function."""
    result = calculate_sum(5, 3)
    return result

if __name__ == "__main__":
    main()
```

3. Create PR with title: `[SCRUM-124] Add clean code example`
4. This should pass all checks!

## Troubleshooting

### Workflow Not Running

- Check that Actions are enabled: **Settings → Actions → General**
- Ensure the workflow file exists: `.github/workflows/pr-agent.yml`
- Check that you're creating a PR (not just pushing to a branch)

### Jira Validation Failing

- Verify the ticket exists: Go to `https://kalyanamnandini.atlassian.net/browse/SCRUM-123`
- Check ticket status is "In Progress" or "Ready for Review"
- Verify `JIRA_PROJECT_KEY` matches your ticket (should be `SCRUM`)
- Check that branch name or PR title contains the ticket ID

### Secret Scanning Failing

- This is expected if you have test secrets
- Remove any hardcoded credentials from your code
- Check `.gitleaks.toml` for allowlist patterns

### AI Review Not Working

- Verify `OPENAI_API_KEY` is set correctly
- Check OpenAI API has credits/usage available
- Review the Actions logs for error messages

### No Comments Appearing

- Check Actions logs for errors
- Verify `GITHUB_TOKEN` permissions (should be automatic)
- Ensure PR is not a draft (draft PRs have limited permissions)

## Quick Test Checklist

- [ ] All GitHub Secrets configured
- [ ] Created test branch: `feature/SCRUM-XXX-description`
- [ ] Branch name contains valid Jira ticket ID
- [ ] Jira ticket exists and is in correct status
- [ ] Created Pull Request
- [ ] Workflow appears in Actions tab
- [ ] Comments appear on PR
- [ ] All checks complete (some may fail intentionally)

## Next Steps

Once testing is successful:

1. Remove test files
2. Update branch naming convention if needed
3. Customize AI review prompt in `scripts/ai_prompt.py`
4. Adjust allowed Jira statuses in `scripts/jira_check.py`
5. Add custom checks in `scripts/utils/analysis_helpers.py`

## Need Help?

- Check GitHub Actions logs for detailed error messages
- Review the workflow file: `.github/workflows/pr-agent.yml`
- Check script logs in Actions output
- Verify all environment variables are set correctly

---

**Happy Testing! 🚀**

