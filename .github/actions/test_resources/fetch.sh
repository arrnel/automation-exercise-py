#!/usr/bin/env bash
set -euo pipefail

BRANCH=$1
RESOURCE=$2
TARGET=$3

git fetch origin "$BRANCH"

if git show-ref --verify --quiet refs/remotes/origin/"$BRANCH"; then
  git checkout origin/"$BRANCH" -- "$RESOURCE" || true
  mkdir -p "$TARGET"
  cp -r "$RESOURCE/." "$TARGET/" || true
fi
