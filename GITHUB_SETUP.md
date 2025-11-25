# GitHub Setup Guide for Elefante

This guide will help you push the Elefante project to GitHub.

---

## Prerequisites

- Git installed and configured
- GitHub account
- Git credentials configured (SSH or HTTPS)

---

## Step 1: Create GitHub Repository

### Option A: Via GitHub Web Interface (Recommended)

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name**: `elefante`
   - **Description**: "Local AI Memory System with Vector and Graph Storage"
   - **Visibility**: Public (or Private if preferred)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

### Option B: Via GitHub CLI

```bash
gh repo create elefante --public --description "Local AI Memory System with Vector and Graph Storage"
```

---

## Step 2: Configure Git User (If Needed)

If you saw the warning about username/email, configure them:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Then amend the commit:

```bash
cd Elefante
git commit --amend --reset-author --no-edit
```

---

## Step 3: Add GitHub Remote

Replace `YOUR_USERNAME` with your GitHub username:

```bash
cd Elefante
git remote add origin https://github.com/YOUR_USERNAME/elefante.git
```

Or if using SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/elefante.git
```

Verify the remote:

```bash
git remote -v
```

---

## Step 4: Push to GitHub

### First Push (Main Branch)

```bash
git branch -M main
git push -u origin main
```

If you encounter authentication issues:

**For HTTPS:**
- You may need a Personal Access Token (PAT)
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate a token with `repo` scope
- Use the token as your password when prompted

**For SSH:**
- Ensure your SSH key is added to GitHub
- Test with: `ssh -T git@github.com`

---

## Step 5: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/elefante`
2. Verify all files are present:
   - ✅ ARCHITECTURE.md
   - ✅ README.md
   - ✅ IMPLEMENTATION_PLAN.md
   - ✅ LICENSE
   - ✅ requirements.txt
   - ✅ config.yaml
   - ✅ setup.py
   - ✅ src/ directory with models

---

## Step 6: Set Up Repository Settings (Optional)

### Add Topics/Tags
Go to repository settings and add topics:
- `ai`
- `memory-system`
- `vector-database`
- `knowledge-graph`
- `chromadb`
- `kuzu`
- `mcp`
- `local-first`

### Enable Issues
- Go to Settings → Features
- Enable Issues for bug tracking and feature requests

### Add Repository Description
Update the "About" section with:
- Description: "🐘 Local AI Memory System with Vector and Graph Storage"
- Website: (if you have one)
- Topics: (as listed above)

---

## Step 7: Create Development Branch

For ongoing development:

```bash
git checkout -b develop
git push -u origin develop
```

---

## Ongoing Development Workflow

### Making Changes

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes
# ... edit files ...

# 3. Stage and commit
git add .
git commit -m "feat: description of your changes"

# 4. Push to GitHub
git push -u origin feature/your-feature-name

# 5. Create Pull Request on GitHub
# Go to your repository and click "Compare & pull request"
```

### Commit Message Convention

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```bash
git commit -m "feat: implement ChromaDB vector store"
git commit -m "fix: resolve embedding generation timeout"
git commit -m "docs: update API documentation"
```

---

## Step 8: Protect Main Branch (Recommended)

1. Go to Settings → Branches
2. Add branch protection rule for `main`:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

---

## Step 9: Add GitHub Actions (Optional)

Create `.github/workflows/tests.yml` for automated testing:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
```

---

## Troubleshooting

### "Permission denied (publickey)"
- Your SSH key is not configured
- Solution: Use HTTPS or add SSH key to GitHub

### "Authentication failed"
- For HTTPS: Use Personal Access Token instead of password
- For SSH: Verify SSH key is added to GitHub account

### "Remote origin already exists"
- Remove existing remote: `git remote remove origin`
- Then add the correct one

### "Failed to push some refs"
- Pull first: `git pull origin main --rebase`
- Then push: `git push origin main`

---

## Quick Reference Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# View remotes
git remote -v

# Pull latest changes
git pull origin main

# Push changes
git push origin main

# Create and switch to new branch
git checkout -b branch-name

# Switch branches
git checkout branch-name

# Delete branch
git branch -d branch-name

# View all branches
git branch -a
```

---

## Next Steps After GitHub Setup

1. ✅ Repository is on GitHub
2. ✅ Initial architecture is committed
3. 🔄 Switch to Code mode to begin implementation
4. 🔄 Follow IMPLEMENTATION_PLAN.md
5. 🔄 Commit and push as you implement each component
6. 🔄 Create pull requests for major features
7. 🔄 Tag releases when milestones are reached

---

**Ready to push to GitHub? Follow the steps above!**
