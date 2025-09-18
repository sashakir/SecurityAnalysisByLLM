#!/usr/bin/env bash
set -euo pipefail

# Usage: run_shell_security_scan.sh <API_KEY> <SCRIPT_PATH> [PROMPT_FILE] [TEST_ROOT]
# - API_KEY: token for the external security review tool
# - SCRIPT_PATH: absolute or relative path to run-security-review.sh
# - PROMPT_FILE (optional): path to the prompt file to use (may be absolute, or a name under prompts/).
#   If omitted, defaults to "security_prompt.md" located under prompts/ or PROMPTS_DIR.
# - TEST_ROOT (optional): path to the test data root to scan; forwarded to shell_security_scan.py.
#
# This script sets the necessary environment variables and invokes the
# Python-based shell_security_scan.py runner from the repo root.

if [[ $# -lt 2 || $# -gt 4 ]]; then
  echo "Usage: $0 <API_KEY> <SCRIPT_PATH> [PROMPT_FILE] [TEST_ROOT]" >&2
  exit 1
fi

API_KEY="$1"
SCRIPT_PATH_INPUT="$2"
if [[ $# -ge 3 ]]; then
  PROMPT_INPUT="$3"
else
  PROMPT_INPUT="claude_security_prompt.md"
fi

# Optional 4th arg: test root to pass to the Python runner
TEST_ROOT=""
if [[ $# -ge 4 ]]; then
  TEST_ROOT="$4"
fi

# Resolve repository root as the parent of this script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}" && pwd)"

# Export variables consumed by shell_security_scan.py
export API_KEY
export SCRIPT_PATH="${SCRIPT_PATH_INPUT}"
export PROMPT_FILE="${PROMPT_INPUT}"

# Run the Python scanner (forward TEST_ROOT if provided)
if [[ -n "${TEST_ROOT}" ]]; then
  exec python3 "shell_security_scan.py" "${TEST_ROOT}"
else
  exec python3 "shell_security_scan.py"
fi