#!/bin/bash

# Big Short Monitor - Deployment Automation Script
# Developed by Senior Dev & DevOps Team

echo "------------------------------------------------"
echo "🚀 BIG SHORT MONITOR DEPLOYMENT KERNEL"
echo "------------------------------------------------"

# 1. Initialize Local Repository
if [ ! -d ".git" ]; then
    echo "[*] Initializing local git repository..."
    git init
    git add .
    git commit -m "Initial commit: Big Short Monitor v1.0"
else
    echo "[!] Git repository already exists."
fi

# 2. Get GitHub Username
echo ""
read -p "👤 Enter your GitHub username: " GH_USER

if [ -z "$GH_USER" ]; then
    echo "❌ Error: Username is required."
    exit 1
fi

REPO_NAME="big-short-monitor"

# 3. Handle Repository Creation
echo ""
echo "[*] Checking for GitHub CLI (gh)..."
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found. Attempting to create repository..."
    gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
    gh pages create --source="main" --path="/" # Attempt to enable GH Pages
else
    echo "⚠️ GitHub CLI (gh) not found or not authenticated."
    echo "Manual injection required. Run these commands:"
    echo ""
    echo "git remote add origin https://github.com/$GH_USER/$REPO_NAME.git"
    echo "git branch -M main"
    echo "git push -u origin main"
    echo ""
    echo "NOTE: You must create the repo '$REPO_NAME' on GitHub first!"
fi

# 4. Final Instructions
echo ""
echo "------------------------------------------------"
echo "✅ DEPLOYMENT PROTOCOL COMPLETE"
echo "------------------------------------------------"
echo "URL will be: https://$GH_USER.github.io/$REPO_NAME/"
echo ""
echo "IF GITHUB PAGES IS NOT ACTIVE:"
echo "1. Go to: https://github.com/$GH_USER/$REPO_NAME/settings/pages"
echo "2. Select 'Deploy from a branch'"
echo "3. Choose 'main' and '/(root)'"
echo "4. Click Save."
echo "------------------------------------------------"
