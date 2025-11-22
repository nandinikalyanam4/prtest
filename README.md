# PR Agent - Enterprise-Grade Automated Pull Request Review System

> **A sophisticated, AI-powered PR review system that enforces production-quality standards and prevents security vulnerabilities before code reaches production.**

[![PR Agent](https://img.shields.io/badge/PR%20Agent-Enterprise-blue)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-success)](https://github.com/features/actions)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple)](https://openai.com)

---

## 📋 Problem Statement

### The Challenge

In modern software development, ensuring code quality, security, and compliance before merging Pull Requests is critical but time-consuming. Manual code reviews are:

- **Inconsistent** - Different reviewers have different standards
- **Time-consuming** - Senior engineers spend hours on routine reviews
- **Error-prone** - Human reviewers miss security vulnerabilities and code smells
- **Scalable** - Doesn't scale with team growth
- **Compliance gaps** - Jira ticket tracking and process enforcement is manual

### The Solution

**PR Agent** is an enterprise-grade automated review system that:

✅ **Automatically reviews every PR** with zero human intervention  
✅ **Detects security vulnerabilities** before they reach production  
✅ **Enforces coding standards** and production readiness  
✅ **Validates process compliance** (Jira tickets, branch naming)  
✅ **Provides AI-powered insights** using advanced language models  
✅ **Blocks merges** when critical issues are detected  
✅ **Leaves actionable feedback** for developers  

**Result:** Higher code quality, faster development cycles, reduced security incidents, and consistent process enforcement.

---

## ✨ Features

### 🔒 Security & Secret Scanning

- ✅ **Gitleaks Integration** - Industry-standard secret detection
- ✅ **Custom Secret Scanner** - Detects AWS keys, JWT tokens, private keys, passwords, API tokens, GitHub PATs, Slack tokens, Google API keys
- ✅ **Hardcoded Credential Detection** - Prevents secrets in codebase
- ✅ **Pattern-Based Detection** - Regex patterns for comprehensive coverage

### 🤖 AI-Powered Code Review (PR-Guardian)

- ✅ **OpenAI GPT-4o Integration** - Advanced AI analysis
- ✅ **Security Vulnerability Detection** - SQL injection, XSS, insecure dependencies
- ✅ **Code Quality Analysis** - Anti-patterns, code smells, architecture issues
- ✅ **Production Readiness Assessment** - Debug code, TODOs, missing tests
- ✅ **Structured Feedback** - JSON-formatted results with severity levels
- ✅ **Actionable Suggestions** - Specific recommendations for fixes

### 📊 Static Code Analysis

- ✅ **Semgrep Integration** - Security-focused static analysis
- ✅ **Linting** - Flake8 and Pylint for Python code quality
- ✅ **Debug Code Detection** - console.log, print statements, debugger calls
- ✅ **TODO/FIXME Detection** - Ensures unfinished work doesn't reach production
- ✅ **Commented Code Detection** - Identifies large blocks of dead code

### 🎫 Jira Integration & Process Enforcement

- ✅ **Automatic Ticket Validation** - Extracts ticket ID from branch/PR title
- ✅ **Status Verification** - Ensures tickets are in "In Progress" or "Ready for Review"
- ✅ **Project Key Validation** - Verifies ticket belongs to correct project
- ✅ **Branch Naming Enforcement** - Requires `feature/PROJ-1234-description` format
- ✅ **REST API Integration** - Real-time Jira status checks

### 🚫 Auto-Fail CI Integration

- ✅ **Blocks Merges** - Automatically fails PRs with critical issues
- ✅ **GitHub Actions Integration** - Seamless CI/CD workflow
- ✅ **Structured Comments** - Posts detailed findings on PR
- ✅ **Summary Reports** - Aggregates all check results

### 💬 Intelligent PR Comments

- ✅ **Structured Feedback** - Organized by severity (HIGH/MEDIUM/LOW)
- ✅ **Code Snippets** - Shows exact lines with issues
- ✅ **Actionable Suggestions** - Specific steps to fix issues
- ✅ **Executive Summaries** - High-level overview for stakeholders

---

## 🏗️ Architecture

### System Overview

```
Developer → GitHub PR → GitHub Actions → PR Agent Pipeline
                                              ↓
                    ┌─────────────────────────────────────┐
                    │  1. Secret Scanning (Gitleaks +    │
                    │     Custom Scanner)                 │
                    ├─────────────────────────────────────┤
                    │  2. Static Analysis (Semgrep +     │
                    │     Linting + Pattern Detection)    │
                    ├─────────────────────────────────────┤
                    │  3. Jira Validation (Ticket Check) │
                    ├─────────────────────────────────────┤
                    │  4. AI Review (PR-Guardian)        │
                    ├─────────────────────────────────────┤
                    │  5. Production Readiness Checks     │
                    └─────────────────────────────────────┘
                                              ↓
                    ┌─────────────────────────────────────┐
                    │  Aggregate Results & Post Comments  │
                    └─────────────────────────────────────┘
                                              ↓
                                    Pass ✅ or Fail ❌
```

### Component Architecture

```
PRAgent/
├── .github/workflows/
│   └── pr-agent.yml              # GitHub Actions workflow
├── scripts/
│   ├── secrets_check.py          # Custom secret scanning
│   ├── static_analysis.py        # Static code analysis
│   ├── jira_check.py             # Jira ticket validation
│   ├── ai_review.py              # AI-powered review
│   ├── ai_prompt.py              # PR-Guardian prompt template
│   └── utils/
│       ├── github_api.py          # GitHub API wrapper
│       ├── jira_api.py            # Jira API wrapper
│       ├── file_scanner.py        # File pattern scanning
│       └── analysis_helpers.py    # Production readiness checks
├── architecture/
│   └── pr-agent-diagram.txt       # Architecture diagram
├── examples/
│   ├── example-pass.md            # Passing PR example
│   └── example-fail.md            # Failing PR example
└── requirements.txt               # Python dependencies
```

### Data Flow

1. **PR Created** → GitHub Actions triggered
2. **Checkout Code** → Fetch PR branch and metadata
3. **Secret Scanning** → Gitleaks + custom scanner detect secrets
4. **Static Analysis** → Semgrep + linting + pattern detection
5. **Jira Validation** → Extract ticket, validate status via REST API
6. **AI Review** → Fetch diff, send to OpenAI, analyze with PR-Guardian
7. **Production Checks** → Scan for debug code, TODOs, quality issues
8. **Aggregate Results** → Combine all findings
9. **Post Comments** → Format and post structured feedback
10. **Decision** → Pass or fail based on critical issues

---

## 🎬 Demo

### Example: Failing PR

**Scenario:** Developer submits PR with secrets, debug code, and invalid Jira ticket.

**Results:**
- ❌ **Secret Scanning:** AWS key detected in `config.py:42`
- ❌ **Static Analysis:** Debug `console.log` found in `auth.py:78`
- ❌ **Jira Validation:** Ticket PROJ-1234 in wrong status ("Backlog")
- ❌ **AI Review:** SQL injection vulnerability detected

**Outcome:** PR blocked from merge with detailed comments.

See [examples/example-fail.md](examples/example-fail.md) for full details.

### Example: Passing PR

**Scenario:** Senior developer submits well-structured PR with proper practices.

**Results:**
- ✅ **Secret Scanning:** No secrets detected
- ✅ **Static Analysis:** Clean code, no debug statements
- ✅ **Jira Validation:** Ticket PROJ-5678 in "In Progress" status
- ✅ **AI Review:** Minor suggestions, no blocking issues

**Outcome:** PR approved with suggestions for improvement.

See [examples/example-pass.md](examples/example-pass.md) for full details.

---

## 🚀 Setup Instructions

### Prerequisites

- GitHub repository with Actions enabled
- Jira instance with API access
- OpenAI API key (for AI reviews)
- Python 3.11+

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd PRAgent
```

### Step 2: Configure GitHub Secrets

Go to **Repository Settings → Secrets and variables → Actions** and add:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `JIRA_BASE_URL` | Your Jira instance domain | `company.atlassian.net` or `https://company.atlassian.net` |
| `JIRA_USER` | Jira username/email | `developer@company.com` |
| `JIRA_API_TOKEN` | Jira API token | `[Generate from Jira]` |
| `JIRA_PROJECT_KEY` | Jira project key | `PROJ` or `SCRUM` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |

**Note:** 
- `GITHUB_TOKEN` is automatically provided by GitHub Actions
- `JIRA_BASE_URL` can be just the domain (e.g., `company.atlassian.net`) - the workflow will add `https://` automatically

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Test Locally (Optional)

```bash
# Test Jira validation
export JIRA_BASE_URL="company.atlassian.net"
export JIRA_USER="your-email@company.com"
export JIRA_API_TOKEN="your-token"
export JIRA_PROJECT_KEY="PROJ"
export GITHUB_TOKEN="your-token"
export GITHUB_REPOSITORY="owner/repo"
export PR_NUMBER="123"

python scripts/jira_check.py
```

### Step 5: Create Test PR

1. Create a branch: `feature/PROJ-1234-test-pr-agent`
2. Make some changes
3. Open a Pull Request
4. Watch the PR Agent review automatically!

---

## 🔧 Configuration

### Branch Naming Convention

Branches are flexible - they only need to contain the Jira ticket ID. Examples:
- `feature/PROJ-1234-description` (traditional)
- `bugfix/PROJ-5678-description` (traditional)
- `PROJ-1234-my-feature` (simple)
- `personal/PROJ-1234-interest` (custom prefix)
- `my-feature/PROJ-1234` (any format)

**Only requirement:** Branch name must contain the Jira ticket ID (e.g., `SCRUM-123`).

Where `PROJ` is your Jira project key.

### Jira Ticket Status

PRs pass if ticket status is one of:
- `TO DO` / `To Do`
- `IN PROGRESS` / `In Progress`
- `IN REVIEW` / `In Review`
- `READY FOR REVIEW` / `Ready for Review`
- `CODE REVIEW` / `Code Review`
- `DONE` / `Done`

**Note:** Status check is case-insensitive, so it works with any capitalization.

Modify in `scripts/jira_check.py`:

```python
allowed_statuses = ['In Progress', 'Ready for Review', 'Your Status']
```

### AI Review Model

Default: `gpt-4o`. Change via `OPENAI_MODEL` environment variable.

---

## 💡 Why This Project Is Valuable

### For Engineering Leaders (CTO/VP Engineering)

**DevSecOps Excellence:**
- Automated security scanning prevents breaches
- Reduces mean time to detect (MTTD) security issues
- Enforces security best practices at scale
- Integrates security into CI/CD pipeline

**AI Engineering Innovation:**
- Demonstrates practical AI/ML application in software development
- Shows understanding of prompt engineering and LLM integration
- Leverages cutting-edge AI models (GPT-4o) for code analysis
- Balances automation with human oversight

**Enterprise Tooling:**
- Production-ready, scalable architecture
- Modular design for easy extension
- Comprehensive error handling and logging
- Integration with enterprise tools (Jira, GitHub)

**Process Automation:**
- Enforces development workflows automatically
- Reduces manual review overhead
- Ensures compliance with organizational standards
- Provides audit trail of code quality decisions

### Business Impact

- **Reduced Security Incidents** - Catch vulnerabilities before production
- **Faster Development** - Automated reviews free up senior engineers
- **Higher Code Quality** - Consistent standards across all PRs
- **Process Compliance** - Automatic Jira ticket validation
- **Cost Savings** - Prevent costly production bugs and security breaches

### Technical Excellence

- **Clean Architecture** - Modular, maintainable codebase
- **Enterprise Patterns** - Proper error handling, logging, configuration
- **API Integration** - GitHub REST API, Jira REST API, OpenAI API
- **CI/CD Integration** - Seamless GitHub Actions workflow
- **Documentation** - Comprehensive README, examples, architecture diagrams

---

## 📊 Workflow Steps

The PR Agent runs these checks on every PR:

1. ✅ **Checkout Code** - Fetch PR branch
2. 🔒 **Secret Scanning** - Gitleaks + custom scanner
3. 📊 **Static Analysis** - Semgrep + linting + pattern detection
4. 🎫 **Jira Validation** - Ticket existence and status check
5. 🤖 **AI Review** - PR-Guardian analysis
6. 🚫 **Production Checks** - Debug code, TODOs, quality
7. 💬 **Post Comments** - Structured feedback on PR
8. ✅/❌ **Decision** - Pass or fail based on critical issues

---

## 🧪 Testing

### Run Individual Checks

```bash
# Secret scanning
python scripts/secrets_check.py

# Static analysis
python scripts/static_analysis.py

# Jira validation
python scripts/jira_check.py

# AI review
python scripts/ai_review.py
```

### Run Production Checks

```bash
python scripts/utils/analysis_helpers.py --check-production-ready
```

---

## 📁 File Structure

```
PRAgent/
├── .github/
│   └── workflows/
│       └── pr-agent.yml              # GitHub Actions workflow
├── architecture/
│   └── pr-agent-diagram.txt          # Architecture diagram
├── examples/
│   ├── example-pass.md                # Passing PR example
│   └── example-fail.md                # Failing PR example
├── scripts/
│   ├── __init__.py
│   ├── secrets_check.py               # Secret scanning
│   ├── static_analysis.py             # Static code analysis
│   ├── jira_check.py                  # Jira validation
│   ├── ai_review.py                   # AI-powered review
│   ├── ai_prompt.py                   # PR-Guardian prompt
│   └── utils/
│       ├── __init__.py
│       ├── github_api.py              # GitHub API wrapper
│       ├── jira_api.py                # Jira API wrapper
│       ├── file_scanner.py            # File scanning utility
│       └── analysis_helpers.py        # Production checks
├── .gitignore
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── SETUP_CHECKLIST.md                 # Setup checklist
```

---

## 🎨 Customization

### Add Custom Secret Patterns

Edit `scripts/secrets_check.py`:

```python
CUSTOM_PATTERN = re.compile(r'your-pattern-here')
```

### Modify AI Review Prompt

Edit `scripts/ai_prompt.py` to customize PR-Guardian behavior.

### Add Custom Checks

Extend `scripts/utils/analysis_helpers.py` with your own validation logic.

---

## 🐛 Troubleshooting

### "Missing required environment variables"

Ensure all GitHub Secrets are configured in repository settings.

### "Jira ticket not found"

- Verify ticket ID format: `PROJ-1234`
- Check Jira credentials are correct
- Ensure ticket exists in specified project

### "AI review failed"

- Verify OpenAI API key is valid
- Check API credits/usage limits
- Review OpenAI API status

### "Gitleaks not found"

Gitleaks is automatically installed in GitHub Actions. For local testing:

```bash
brew install gitleaks  # macOS
```

---

## 📚 Examples

See detailed examples:
- [Passing PR](examples/example-pass.md) - Clean code that passes all checks
- [Failing PR](examples/example-fail.md) - Issues detected and blocked

---

## 🤝 Contributing

1. Create feature branch: `feature/PROJ-1234-description`
2. Make changes
3. Ensure all checks pass
4. Submit PR

---

## 📄 License

This project is provided as-is for use in your organization.

---

## 🔗 References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [Semgrep Documentation](https://semgrep.dev/docs/)

---

## 🎯 Key Takeaways

**PR Agent** demonstrates:

✅ **Enterprise-Grade Engineering** - Production-ready, scalable architecture  
✅ **DevSecOps Best Practices** - Security integrated into CI/CD  
✅ **AI/ML Application** - Practical use of LLMs for code analysis  
✅ **Process Automation** - Enforces organizational standards  
✅ **Tooling Excellence** - Clean, maintainable, well-documented code  

**Perfect for:** CTO/CEO presentations, engineering portfolio, interview demonstrations, internal tooling showcases.

---

**Built with ❤️ for enterprise engineering teams**
