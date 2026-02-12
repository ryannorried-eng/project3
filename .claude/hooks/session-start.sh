#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Install Python dependencies
pip install -r requirements.txt

# Install dev tooling (linter, formatter, type checker, test runner)
pip install ruff mypy pytest types-requests pandas-stubs

# Install GitHub CLI if not present
if ! command -v gh &> /dev/null; then
  GH_VERSION="2.86.0"
  curl -fsSL "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_amd64.tar.gz" -o /tmp/gh.tar.gz
  tar -xzf /tmp/gh.tar.gz -C /tmp
  cp /tmp/gh_*/bin/gh /usr/local/bin/gh
  rm -rf /tmp/gh*
fi
