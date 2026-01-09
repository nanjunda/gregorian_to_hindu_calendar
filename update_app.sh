#!/bin/bash

# =================================================================
# Hindu Panchanga V5.5 - Incremental Update Orchestrator
# =================================================================

# Exit on any error
set -e

echo "🌌 Starting Incremental Update of Hindu Panchanga..."

# 1. Pull the latest code from GitHub
echo "🏎️  Fetching latest changes from origin/main..."
git pull origin main

# 2. Check if we need a full deploy or a fast sync
# If requirements.txt or deploy.sh changed, we might want a full check
# But for now, we default to --fast for speed
DEPLOY_FLAGS="--fast"

# 3. Launch the deployment engine
echo "🚀 Launching Fast-Sync Deployment..."
sudo bash ./deploy.sh $DEPLOY_FLAGS

echo "================================================================="
echo "✅ UPDATE SUCCESSFUL!"
echo "📘 All new features are live."
echo "================================================================="
