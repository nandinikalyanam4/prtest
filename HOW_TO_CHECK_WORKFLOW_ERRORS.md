# How to Check Workflow Errors - Step by Step

## 🔍 Why You're Not Seeing AI Suggestions

The workflow is **failing before it can post comments**. We need to see the actual error.

## 📋 Step-by-Step: Check the Error

### Step 1: Go to Actions Tab
1. Go to: **https://github.com/nandinikalyanam4/prtest/actions**
2. You should see a list of workflow runs (all showing "Failure")

### Step 2: Click on Latest Failed Run
1. Click on the **most recent failed run** (should be at the top)
2. It will say something like "Fix: Add PYTHONPATH..." or similar

### Step 3: Click on the Job
1. You'll see a job called **"PR Agent Review"**
2. Click on it (it will have a red X)

### Step 4: Expand Each Step
1. You'll see a list of steps:
   - ✅ Checkout code
   - ✅ Set up Python
   - ✅ Install dependencies
   - ✅ Set environment variables
   - ✅ Install Gitleaks
   - ✅ Secret Scanning (Gitleaks)
   - ✅ Custom Secret Scanning
   - etc.

2. **Click on each step** to expand it
3. Look for steps with **red X** or error messages
4. **The first step that fails is the problem!**

### Step 5: Read the Error Message
Look for error messages like:
- `ModuleNotFoundError: No module named 'scripts'`
- `ImportError: cannot import name 'GitHubAPI'`
- `FileNotFoundError: scripts/secrets_check.py`
- `AttributeError`
- Any Python traceback

## 🎯 Common Errors and Fixes

### Error: `ModuleNotFoundError: No module named 'scripts'`
**Fix:** PYTHONPATH issue - already fixed, but verify it's set

### Error: `ModuleNotFoundError: No module named 'requests'`
**Fix:** Dependencies not installing - check requirements.txt

### Error: `FileNotFoundError`
**Fix:** File path issue - check file exists

### Error: `401 Unauthorized` or `403 Forbidden`
**Fix:** GitHub token permissions issue

### Error: `Missing required environment variables`
**Fix:** Secrets not configured in GitHub

## 📸 What to Share

When you check the logs, please share:
1. **Which step failed** (first red X)
2. **The error message** (copy the full error)
3. **Any Python traceback**

This will help me fix it immediately!

## 🚀 Quick Test

After checking the error, we can:
1. Fix the specific issue
2. Test the workflow again
3. See AI suggestions appear on your PR!

---

**Go check the workflow logs now and share the error message!** 🔍

