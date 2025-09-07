#!/bin/bash
set -e

# List of repos to delete. You can add multiple repo to delete, following the format. Separated by new line.
repos=(
    "YOURREPONAME"
)

echo "⚠️ WARNING: This will permanently DELETE the listed repositories under 'chrisanja'."
read -p "Are you sure? Type 'yes' to continue: " confirm

if [[ "$confirm" != "yes" ]]; then
    echo "❌ Aborted."
    exit 1
fi

for repo in "${repos[@]}"; do
    echo "🗑 Deleting $repo ..."
    gh repo delete "YOURGITHUBUSERNAME/$repo" --confirm
done

echo "✅ All selected repos deleted."
