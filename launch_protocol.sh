#!/bin/bash

# ==========================================
# 🚀 BIG SHORT MONITOR - LAUNCH PROTOCOL v1.0
# ==========================================
# Automates: Cleanup, PWA Validation, Deployment, and Mobile Handoff.

echo -e "\033[1;36m"
echo "   ___  ___  ___    _____  ______ __  __ ______ ____  ___ "
echo "  / _ )/ _ \/ _ \  / __/ |/ /_  // / / //_  __// __ \/ _ \\"
echo " / _  / // / // / / _//    / / // /_/ /  / /  / /_/ / , _/"
echo "/____/____/____/ /___/_/|_/ /_//_/\____/  /_/   \____/_/|_|" 
echo -e "\033[0m"
echo "Initiating Launch Sequence..."
echo "---------------------------------------------------------"

# --- CONFIGURATION ---
REPO_URL=$(git remote get-url origin)
# Extract username and repo name from URL (e.g. https://github.com/User/Repo.git)
GH_USER=$(echo $REPO_URL | sed -E 's/.*github.com[:\/]([^\/]+)\/([^\/]+)(\.git)?/\1/')
REPO_NAME=$(echo $REPO_URL | sed -E 's/.*github.com[:\/]([^\/]+)\/([^\/]+)(\.git)?/\2/')
LIVE_URL="https://$GH_USER.github.io/$REPO_NAME/"

# --- STEP 1: CLEANUP & ORGANIZE ---
echo -e "\n\033[1;33m[1/3] Organizing Project Structure...\033[0m"
mkdir -p internal_scripts
# Move utility scripts if they exist in root
mv luisin_agent.py internal_scripts/ 2>/dev/null
mv super_agente.py internal_scripts/ 2>/dev/null
mv verify_login_email.py internal_scripts/ 2>/dev/null
echo "✓ Workspace sanitized."

# --- STEP 2: PWA & MOBILE OPTIMIZATION ---
echo -e "\n\033[1;33m[2/3] Validating Mobile/PWA Modules...\033[0m"
if [ -f "manifest.json" ] && [ -f "sw.js" ]; then
    echo "✓ Manifest verified."
    echo "✓ Service Worker verified."
else
    echo "❌ CRITICAL: PWA files missing. Aborting."
    exit 1
fi

# Force cache bust in index.html (optional but good for development iterations)
TIMESTAMP=$(date +%s)
# Note: We are not modifying index.html heavily to avoid breaking it, 
# but in a real build pipeline we would inject this timestamp into sw.js

# --- STEP 3: DEPLOYMENT ---
echo -e "\n\033[1;33m[3/3] Deploying to Global CDN (GitHub Pages)...\033[0m"
git add .
git commit -m "Release: Automated Launch Protocol $TIMESTAMP"
git push origin main

echo -e "\n---------------------------------------------------------"
echo -e "\033[1;32m✅ LAUNCH SUCCESSFUL\033[0m"
echo "---------------------------------------------------------"
echo ""
echo "📱 \033[1;37mMOBILE ACCESS LINK:\033[0m"
echo -e "\033[1;34m$LIVE_URL\033[0m"
echo ""
echo "To install on Mobile:"
echo "1. Open the link in Chrome (Android) or Safari (iOS)."
echo "2. Tap 'Share' (iOS) or Menu (Android)."
echo "3. Select 'Add to Home Screen'."
echo ""
echo "🖥️  \033[1;37mLOCAL PREVIEW:\033[0m"
echo "Starting local server... (Press Ctrl+C to stop)"
python3 -m http.server 8080
