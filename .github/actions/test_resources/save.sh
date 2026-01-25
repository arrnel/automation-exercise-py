#!/usr/bin/env bash
set -euo pipefail

BRANCH=$1
RESOURCE=$2
TARGET=$3
MAX_RETRIES=5

git config user.name "github-actions"
git config user.email "github-actions@github.com"

if git show-ref --verify --quiet refs/remotes/origin/"$BRANCH"; then
  git checkout "$BRANCH"
else
  git checkout -b "$BRANCH"
fi

rm -rf "$RESOURCE"
mkdir -p "$RESOURCE"
cp -r "$TARGET/." "$RESOURCE/" || true

git add "$RESOURCE"

if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi

git commit -m "Update $RESOURCE from CI"

for i in $(seq 1 $MAX_RETRIES); do
  if git pull --rebase origin "$BRANCH" && git push origin "$BRANCH"; then
    echo "Push succeeded"
    exit 0
  fi

  echo "Push failed, retry $i/$MAX_RETRIES"
  sleep $((RANDOM % 3 + 1))
done

echo "Failed to push after $MAX_RETRIES attempts"
exit 1
