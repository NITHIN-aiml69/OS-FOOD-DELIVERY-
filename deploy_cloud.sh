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
echo "Target Repository: https://github.com/NITHIN-aiml69/os-food-delivery-platform"
echo "================================================================================"

echo ""
echo "[Step 1/2] Pushing to GitHub..."
echo "If you haven't created the repository on GitHub yet, create it now (empty):"
echo "👉 https://github.com/new?name=os-food-delivery-platform&description=OS+Experimental+Lab+-+Food+Delivery+Platform+(25BTRPW066)&public=true"
echo ""
read -p "Press [Enter] after creating the repository on GitHub to push..."

git push -u origin main

echo ""
echo "================================================================================"
echo "✅ GitHub Push Succeeded!"
echo "Repository: https://github.com/NITHIN-aiml69/os-food-delivery-platform"
echo "================================================================================"

echo ""
echo "[Step 2/2] Deploying to Vercel..."
echo "Vercel automatically detects api/index.py, vercel.json, and requirements.txt."
echo ""
echo "Option A (Recommended - Automated CI/CD via GitHub):"
echo "  1. Visit: https://vercel.com/new"
echo "  2. Connect your GitHub account and click 'Import' on 'os-food-delivery-platform'."
echo "  3. Click 'Deploy'."
echo "  -> Your live URL will be: https://os-food-delivery-platform.vercel.app"
echo ""
echo "Option B (Deploy directly via Vercel CLI):"
echo "  Running 'npx vercel' now..."
npx vercel --prod
