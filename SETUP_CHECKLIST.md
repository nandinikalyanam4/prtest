# PR Agent Setup Checklist

Use this checklist to ensure your PR Agent is properly configured.

## ✅ Pre-Setup

- [ ] Repository is initialized with Git
- [ ] You have admin access to the repository
- [ ] You have access to Jira instance
- [ ] You have an OpenAI API key

## ✅ GitHub Secrets Configuration

Go to: **Repository Settings → Secrets and variables → Actions**

- [ ] `JIRA_BASE_URL` - Your Jira instance domain (e.g., `yourcompany.atlassian.net` or `https://yourcompany.atlassian.net`)
- [ ] `JIRA_USER` - Your Jira username/email (e.g., `user@company.com`)
- [ ] `JIRA_API_TOKEN` - Your Jira API token
- [ ] `JIRA_PROJECT_KEY` - Your Jira project key (e.g., `PROJ` or `SCRUM`)
- [ ] `OPENAI_API_KEY` - Your OpenAI API key

**Note:** 
- `GITHUB_TOKEN` is automatically provided by GitHub Actions
- `JIRA_BASE_URL` can be just the domain (e.g., `yourcompany.atlassian.net`) - the workflow will add `https://` automatically

## ✅ Jira API Token Setup

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label (e.g., "PR Agent")
4. Copy the token and add it to GitHub Secrets as `JIRA_API_TOKEN`

## ✅ Verify File Structure

Ensure these files exist:

```
.github/workflows/pr-agent.yml
scripts/jira_check.py
scripts/ai_review.py
scripts/utils/github_api.py
scripts/utils/jira_api.py
scripts/utils/analysis_helpers.py
requirements.txt
README.md
```

## ✅ Test the Setup

1. Create a test branch: `feature/PROJ-1234-test-pr-agent`
2. Create a test PR
3. Verify the workflow runs in GitHub Actions
4. Check that comments are posted on the PR

## ✅ Customization (Optional)

- [ ] Adjust allowed Jira statuses in `scripts/jira_check.py`
- [ ] Modify AI review prompt in `scripts/ai_review.py`
- [ ] Add custom checks in `scripts/utils/analysis_helpers.py`
- [ ] Update branch naming convention if needed

## ✅ Troubleshooting

If the workflow fails:

1. Check GitHub Actions logs
2. Verify all secrets are set correctly
3. Ensure Jira ticket exists and is accessible
4. Verify OpenAI API key is valid and has credits
5. Check branch naming follows convention

## 🎉 You're Done!

Once all items are checked, your PR Agent is ready to review PRs automatically!

