#!/bin/bash

# This will remove all .git in the subfolder
set -e

TARGET_DIR="$(pwd)"

echo "⚠️ WARNING: This will remove all nested .git folders inside: $TARGET_DIR"
read -p "Are you sure you want to continue? (y/n): " confirm

if [[ "$confirm" != "y" ]]; then
    echo "❌ Aborted."
    exit 1
fi

# Find and remove all nested .git directories, except the root .git
find "$TARGET_DIR" -mindepth 2 -type d -name ".git" -exec rm -rf {} +

echo "✅ All nested .git folders removed!"
