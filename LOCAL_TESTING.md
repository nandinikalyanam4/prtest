# Local Testing Guide

You can test some components locally before pushing to GitHub, but the full PR Agent workflow requires GitHub Actions.

## What Needs to Be Pushed to GitHub

**Yes, you need to push the code to GitHub** because:

1. **GitHub Actions Workflow** - The `.github/workflows/pr-agent.yml` file must be in your repository for the workflow to run
2. **All Scripts** - The scripts need to be in the repo for GitHub Actions to execute them
3. **Workflow Triggers** - The workflow triggers on pull requests, which requires the code to be on GitHub

## What You Can Test Locally First

Before pushing, you can test individual components:

### 1. Test Jira Validation Locally

```bash
# Set environment variables
export JIRA_BASE_URL="kalyanamnandini.atlassian.net"
export JIRA_USER="kalyanamnandini786.gmail.com"
export JIRA_API_TOKEN="your-jira-token"
export JIRA_PROJECT_KEY="SCRUM"
export GITHUB_TOKEN="your-github-token"  # For testing only
export GITHUB_REPOSITORY="your-username/PRAgent"  # Your repo
export PR_NUMBER="1"  # A test PR number

# Test Jira check
python scripts/jira_check.py
```

### 2. Test Secret Scanning Locally

```bash
# Create a test file with a secret (for testing only!)
echo 'api_key = "test-key-12345"' > test_secret.py

# Test secret scanner
python scripts/secrets_check.py
# This will scan the current PR if PR_NUMBER is set
```

### 3. Test Static Analysis Locally

```bash
# Create a test file with issues
cat > test_debug.py << 'EOF'
def test():
    print("Debug statement")  # Will be flagged
    # TODO: Fix this
    return True
EOF

# Test static analysis
python scripts/static_analysis.py
```

### 4. Test AI Review Locally

```bash
export OPENAI_API_KEY="your-openai-key"
export GITHUB_TOKEN="your-github-token"
export GITHUB_REPOSITORY="your-username/PRAgent"
export PR_NUMBER="1"

python scripts/ai_review.py
```

## Quick Push and Test Workflow

### Step 1: Push Initial Code

```bash
# Make sure you're in the PRAgent directory
cd /Users/nandinikalyanam/projects/PRAgent

# Check git status
git status

# Add all files
git add .

# Commit
git commit -m "Add PR Agent workflow and scripts"

# Push to GitHub (assuming you have a remote set up)
git push origin main  # or master, or your default branch
```

### Step 2: Verify Files Are on GitHub

1. Go to your GitHub repository
2. Check that these exist:
   - `.github/workflows/pr-agent.yml` ✓
   - `scripts/` directory with all scripts ✓
   - `requirements.txt` ✓

### Step 3: Configure Secrets

1. Go to: **Settings → Secrets and variables → Actions**
2. Add all required secrets (see SETUP_CHECKLIST.md)

### Step 4: Create Test PR

```bash
# Create a test branch
git checkout -b SCRUM-123-test-pr-agent

# Make a small change
echo "# Test" >> test.md
git add test.md
git commit -m "Test PR Agent"
git push origin SCRUM-123-test-pr-agent
```

Then create a PR on GitHub - the workflow will run automatically!

## What Happens When You Push

1. **First Push**: The workflow file is added to your repo
2. **GitHub Actions**: Automatically detects the workflow file
3. **Next PR**: When you create a PR, the workflow triggers automatically
4. **No Manual Trigger Needed**: The workflow runs on every PR automatically

## Troubleshooting: Workflow Not Running

If the workflow doesn't run after pushing:

1. **Check Actions Tab**: Go to your repo → "Actions" tab
2. **Verify Workflow File**: Ensure `.github/workflows/pr-agent.yml` exists
3. **Check Permissions**: Go to Settings → Actions → General
   - Ensure "Allow all actions and reusable workflows" is enabled
4. **Check Branch**: The workflow file must be on the default branch (main/master)

## Recommended Approach

**Option 1: Quick Test (Recommended)**
1. Push all code to GitHub
2. Configure secrets
3. Create a test PR
4. Watch it work!

**Option 2: Local Testing First**
1. Test individual scripts locally (as shown above)
2. Fix any issues
3. Push to GitHub
4. Create test PR

## Summary

- ✅ **Push code to GitHub** - Required for workflow to run
- ✅ **Test locally first** - Optional, but helps catch issues early
- ✅ **Workflow auto-runs** - No manual trigger needed after setup
- ✅ **Secrets in GitHub** - Must be configured in repository settings

---

**Bottom Line**: Yes, push the code to GitHub to test the full PR Agent workflow! 🚀

