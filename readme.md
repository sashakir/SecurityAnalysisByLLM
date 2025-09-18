# LLMTest

A small workspace demonstrating:
- Minimal examples of calling LLMs (via LiteLLM/OpenAI-compatible clients)
- An LLM-driven security review script that analyzes Java files and compares JSON outputs against expected results
- A shell-based security scan runner that delegates to an external tool, parses SARIF, and compares plain-text results
- Prompt templates for guiding both approaches

This repository is meant for experimentation and prompt iteration to align tool outputs with desired expectations.

## Contents

- hello.py — Tiny OpenAI-compatible example using a LiteLLM proxy
- sample_litellm.py — Direct usage of the litellm library with streaming and non-streaming examples
- security_scan.py — LLM (OpenAI-compatible) driven analysis producing/consuming JSON (-actual.json / -expected.json)
- shell_security_scan.py — Invokes an external script to analyze code, parses SARIF, and writes plain text (-actual.txt / -expected.txt)
- prompts/ — Prompt templates for both JSON- and text-based analyzers
- tests/ — Java test suites and expected results used for comparison
- run_shell_security_scan.sh — MAIN ENTRY POINT: convenience runner that wires env vars and forwards optional arguments

## Main entry point (recommended): run_shell_security_scan.sh

This script is the primary way to run the shell-based security scan.

Usage:

  run_shell_security_scan.sh <API_KEY> <SCRIPT_PATH> [PROMPT_FILE] [TEST_ROOT]

Parameters:
- API_KEY — token for the external tool
- SCRIPT_PATH — path to run-security-review.sh (absolute or relative)
- PROMPT_FILE — optional; defaults to claude_security_prompt.md (may be absolute or a filename under prompts/)
- TEST_ROOT — optional; path to the test data root to scan; forwarded to shell_security_scan.py

## Prerequisites

- Python 3.9+
- Recommended packages:
  - pip install openai litellm
- For shell-based scan (shell_security_scan.py):
  - Access to an external tool/runner script, e.g. /Users/sashakir/Qodana/hktn25-sec-review/run-security-review.sh
  - An API key/token for that external tool

## Security notice

The simple example files currently include hardcoded API keys for demonstration. Before running in any real environment, replace them with environment variables.
- hello.py: replace inline api_key with environment-provided key.
- sample_litellm.py: remove or override the inline OPENAI_API_KEY assignment.

Never commit real credentials.

## Environment variables

Common variables used across scripts:
- OPENAI_API_KEY — API key for OpenAI-compatible clients (security_scan.py, hello.py)
- OPENAI_BASE_URL — Base URL for an OpenAI-compatible endpoint (default: https://litellm.labs.jb.gg/)
- MODEL — Default model for security_scan.py (default: gpt-4o-mini)
- PROMPTS_DIR — Directory containing prompt files (defaults to prompts/)

Shell-based scan specific:
- API_KEY — Token for the external security review tool
- SCRIPT_PATH — Path to the external runner script (e.g., run-security-review.sh)
- PROMPT_FILE — Prompt file name within PROMPTS_DIR or an absolute path (default: claude_security_prompt.md)

## Usage

### Hello (OpenAI-compatible via LiteLLM proxy)

This is a minimal example showing a single chat request.

- Ensure OPENAI_API_KEY is set for your provider, or edit hello.py to point to your proxy.
- Run:

  python hello.py

### sample_litellm.py (direct LiteLLM API)

- Install: pip install litellm
- Optionally set MODEL (default gpt-4o-mini):

  export MODEL="gpt-4o-mini"

- Provide a compatible provider key (e.g., OPENAI_API_KEY) and run:

  python sample_litellm.py "Write a haiku about the sea"

This script also demonstrates a streaming response mode.

### security_scan.py (LLM-driven JSON analysis)

This script reads prompt templates from prompts/system_security_prompt.txt and prompts/user_security_prompt.txt, builds a line-numbered code view, and requests a structured JSON response.

Key behaviors:
- Produces per-file -actual.json next to each .java file.
- If -expected.json is missing, it writes the actual result as -expected.json and counts it as a created/missing expected.
- Compares actual vs expected JSON; reports pass/fail summary and total time.

Run:

  export OPENAI_API_KEY=...               # required
  export OPENAI_BASE_URL=https://litellm.labs.jb.gg/   # optional
  export MODEL=gpt-4o-mini                # optional
  python security_scan.py                 # scans tests/ recursively

You can also pass a single file path to analyze only that file:

  python security_scan.py tests/java/BenchmarkTest00001.java

### shell_security_scan.py (external tool + SARIF parsing)

Instead of calling an LLM API, this script runs an external review tool and parses its SARIF output into a simple plain-text list of file:line entries. It then compares only the FIRST LINE of actual vs expected text files.

Key behaviors:
- Recursively scans the test root for .java files
- Writes -actual.txt for each source; if -expected.txt is missing, creates it from actual
- Compares only the first line between actual and expected
- Suppresses stdout of the external tool; shows stderr on failure
- Includes total running time in the summary

Environment:
- SCRIPT_PATH (path to external runner)
- API_KEY (tool token)
- PROMPT_FILE (defaults to claude_security_prompt.md; can be absolute or a basename inside prompts/)
- PROMPTS_DIR (optional overrides of prompt directory)

Run directly:

  export API_KEY=...
  export SCRIPT_PATH=/absolute/path/to/run-security-review.sh
  export PROMPT_FILE=claude_security_prompt.md
  python shell_security_scan.py [TEST_ROOT]

If TEST_ROOT is omitted, it prefers tests/fraunhofer-suite, then test/fraunhofer-suite, then tests.

### tools/run_shell_security_scan.sh (convenience wrapper)

This bash script sets environment variables and calls the Python runner. Usage:

  tools/run_shell_security_scan.sh <API_KEY> <SCRIPT_PATH> [PROMPT_FILE] [TEST_ROOT]

- API_KEY: token for the external tool
- SCRIPT_PATH: path to run-security-review.sh
- PROMPT_FILE: optional; defaults to claude_security_prompt.md
- TEST_ROOT: optional; forwarded to shell_security_scan.py

Examples:

  tools/run_shell_security_scan.sh "$API_KEY" /path/run-security-review.sh
  tools/run_shell_security_scan.sh "$API_KEY" /path/run-security-review.sh prompts/claude_security_prompt.md tests/fraunhofer-suite

## Prompts

- prompts/system_security_prompt.txt + prompts/user_security_prompt.txt — for JSON-based security_scan.py
- prompts/claude_security_prompt.md — for the shell-based scanner; contains strict formatting rules and extra notes/examples appended over time to steer results

You can override PROMPTS_DIR to point to a different prompt set.

## Test data

- tests/java, tests/owasp1, tests/owasp2, tests/fraunhofer-suite/** — Java sources and expected outputs
- JSON flow: files pair with -expected.json and -actual.json
- Shell flow: files pair with -expected.txt and -actual.txt

The runners will create expected files when missing (from actual results) and compare on subsequent runs.

## Troubleshooting

- Missing prompt files: security_scan.py and shell_security_scan.py will exit with an error if required prompts are not found. Ensure PROMPTS_DIR and PROMPT_FILE are correct.
- No API key: security_scan.py warns if OPENAI_API_KEY is not set; requests will fail against real endpoints.
- External runner failures: shell_security_scan.py shows stderr and non-zero exit codes. Verify SCRIPT_PATH and permissions.
- SARIF parsing: shell_security_scan.py expects security-review.sarif inside the tool’s result directory; verify the external tool’s flags (--result directory, --shouldProduceSarif=true).

## License / Use

This repository is for testing and demonstration purposes. Review licenses of any third-party tools you integrate (e.g., external security review runner) and ensure you have permission to use prompts and test data.
