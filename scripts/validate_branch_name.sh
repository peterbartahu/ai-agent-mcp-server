#!/usr/bin/env bash

set -e

BRANCH_NAME="$1"

echo "🔍 $USER Started validating branch name: $BRANCH_NAME"

if [[ "$BRANCH_NAME" =~ ^(feature|bugfix|hotfix|subtask)/ ]]; then
  echo "📌 Ticket-based branch detected"

  if [[ ! "$BRANCH_NAME" =~ ^(feature|bugfix|hotfix|subtask)/[0-9]+-.*$ ]]; then
    echo "❌ Invalid branch name!"
    echo
    echo "Expected format:"
    echo "  feature/000-description"
    echo "  bugfix/000-description"
    echo "  hotfix/000-description"
    echo "  subtask/000-description"
    exit 1
  fi

  echo "✅ Branch name is valid"
else
  echo "ℹ️ Non ticket-based branch, skipping validation"
fi
