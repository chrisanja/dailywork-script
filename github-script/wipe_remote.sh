#!/bin/bash
# wipe_remote.sh
# This script wipes the remote repo branch completely

set -e

REMOTE="origin"
BRANCH="main"

echo "⚠️ WARNING: This will WIPE the remote branch '$BRANCH' on '$REMOTE'."
read -p "Are you sure you want to continue? (yes/no): " confirm

if [[ "$confirm" != "yes" ]]; then
  echo "Aborted."
  exit 1
fi

echo "Creating temporary orphan branch..."
git checkout --orphan temp-empty-branch

echo "Removing all files locally (safe, only Git tracked)..."
git rm -rf . > /dev/null 2>&1 || true

echo "Committing empty state..."
git commit --allow-empty -m "Wipe remote branch"

echo "Force pushing empty state to remote '$BRANCH'..."
git push $REMOTE temp-empty-branch:$BRANCH --force

echo "✅ Remote branch '$BRANCH' has been wiped clean."
echo "You are now on branch 'temp-empty-branch'."
echo "If you want, you can recreate 'main' locally with:"
echo "  git checkout -b main origin/main"
