#!/bin/bash
set -e

# List of repos. You can add multiple repos following the format. Separated by new line.
repos=(
    "git@github.com:YOURGITHUBUSERNAME/YOURREPO.git"
)

# Target folder where all repos will be cloned
TARGET_DIR="all-downloads"
mkdir -p "$TARGET_DIR"

# Clone all repos
cd "$TARGET_DIR"
for repo in "${repos[@]}"; do
    name=$(basename "$repo" .git)
    if [ -d "$name" ]; then
        echo "⚠️ Repo $name already exists, skipping..."
    else
        echo "⬇️ Cloning $repo ..."
        git clone "$repo"
    fi
done

echo "✅ All repos downloaded into: $TARGET_DIR"
