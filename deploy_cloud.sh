#!/usr/bin/env bash
# Cloud Deployment Script for GitHub & Vercel
# Student: NITHIN N | Roll Number: 25BTRPW066

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "================================================================================"
echo "DEPLOYMENT SUITE: GITHUB & VERCEL CLOUD"
echo "Student: NITHIN N | Roll Number: 25BTRPW066"
echo "GitHub Account: NITHIN-aiml69"
echo "Repository: https://github.com/NITHIN-aiml69/OS-FOOD-DELIVERY-"
echo "================================================================================"

echo ""
echo "[Step 1/2] Syncing to GitHub..."
git push origin main

echo ""
echo "================================================================================"
echo "✅ GitHub Push Succeeded!"
echo "Repository: https://github.com/NITHIN-aiml69/OS-FOOD-DELIVERY-"
echo "================================================================================"

echo ""
echo "[Step 2/2] Deploying to Vercel..."
echo "To finish deployment in your browser:"
echo "1. On the open Vercel tab, click 'Continue with GitHub'."
echo "2. Authorize Vercel to access your 'OS-FOOD-DELIVERY-' repository."
echo "3. Click 'Deploy'."
echo ""
echo "Or deploy directly from terminal via:"
echo "npx vercel --prod"
