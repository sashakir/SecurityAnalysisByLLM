"""
Security scan script: sends source code to an LLM to check for common vulnerabilities
(taint analysis themes: SQL injection, XSS, command injection, path traversal, SSRF,
insecure deserialization, hardcoded secrets, etc.).

Usage:
  python security_scan.py [PATH_TO_SOURCE_FILE]

Defaults:
  - If no path is given, scans tests/java/BenchmarkTest00001.java
  - Model can be configured via env var MODEL (default: gpt-4o-mini)
  - OpenAI-compatible endpoint:
      * API key via env var OPENAI_API_KEY
      * Base URL via env var OPENAI_BASE_URL (default: https://litellm.labs.jb.gg/)

This script uses the OpenAI-compatible client, so it can work with a LiteLLM Proxy.
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict

try:
    import openai
except Exception as e:
    print("The 'openai' package is required. Install with: pip install openai", file=sys.stderr)
    raise


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def read_prompt_file(path: str) -> str | None:
    """Try to read a prompt template file; return None if missing or unreadable."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def build_messages(code: str, filename: str) -> list[Dict[str, Any]]:
    # Resolve prompts directory (can be overridden via PROMPTS_DIR env var)
    prompts_dir = os.getenv("PROMPTS_DIR", os.path.join(os.path.dirname(__file__), "prompts"))
    system_prompt_path = os.path.join(prompts_dir, "system_security_prompt.txt")
    user_prompt_path = os.path.join(prompts_dir, "user_security_prompt.txt")

    # Prompts must be provided via files; no fallbacks are used.

    # Prepare a line-numbered version of the code so the model can reference exact lines
    numbered_lines = []
    for idx, line in enumerate(code.splitlines(), start=1):
        numbered_lines.append(f"{idx}: {line}")
    numbered_code = "\n".join(numbered_lines)

    # Load prompts strictly from files; exit if missing/unreadable
    system_prompt = read_prompt_file(system_prompt_path)
    if not system_prompt:
        print(f"Error: prompt file missing or unreadable: {system_prompt_path}", file=sys.stderr)
        sys.exit(1)
    user_template = read_prompt_file(user_prompt_path)
    if not user_template:
        print(f"Error: prompt file missing or unreadable: {user_prompt_path}", file=sys.stderr)
        sys.exit(1)

    # System message defines assistant behavior and scope of analysis
    system = {
        "role": "system",
        "content": system_prompt,
    }

    # User message contains the concrete instruction and the code to analyze
    try:
        # Safely substitute only our two placeholders, leaving JSON braces intact
        user_content = (
            user_template.replace("{filename}", filename)
            .replace("{numbered_code}", numbered_code)
        )
    except Exception as e:
        print(f"Error formatting user prompt template: {e}", file=sys.stderr)
        sys.exit(1)

    user = {
        "role": "user",
        "content": user_content,
    }
    return [system, user]


def parse_assistant_content(resp: Any) -> str:
    # Try OpenAI SDK style first
    try:
        return resp.choices[0].message.content  # type: ignore[attr-defined]
    except Exception:
        pass
    # Fallback dict-like
    try:
        return resp.choices[0].message["content"]  # type: ignore[index]
    except Exception:
        return str(resp)


def extract_json_block(text: str) -> Dict[str, Any] | None:
    """Attempt to extract the first top-level JSON object from the text."""
    start = text.find("{")
    if start == -1:
        return None
    # naive brace-matching to find end of top-level object
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i+1])
                except Exception:
                    return None
    return None


def analyze_file(filename: str, client: Any, model: str) -> tuple[Dict[str, Any] | None, str]:
    """Run the LLM on a single file and return (parsed_json_or_none, raw_text)."""
    try:
        code = read_file(filename)
    except FileNotFoundError:
        print(f"Error: file not found: {filename}", file=sys.stderr)
        return None, ""

    messages = build_messages(code, filename)
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    content = parse_assistant_content(resp)
    data = extract_json_block(content)
    return data, content


def expected_path_for(src_path: str) -> str:
    in_dir = os.path.dirname(src_path)
    base = os.path.splitext(os.path.basename(src_path))[0]
    return os.path.join(in_dir, f"{base}-expected.json")


def actual_path_for(src_path: str) -> str:
    in_dir = os.path.dirname(src_path)
    base = os.path.splitext(os.path.basename(src_path))[0]
    return os.path.join(in_dir, f"{base}-actual.json")


def load_json(path: str) -> Dict[str, Any] | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def write_json(path: str, data: Dict[str, Any]) -> bool:
    try:
        parent = os.path.dirname(path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error writing JSON to {path}: {e}", file=sys.stderr)
        return False


def compare_results(actual: Dict[str, Any] | None, expected: Dict[str, Any] | None) -> tuple[bool, str]:
    if expected is None:
        return False, "Expected result file missing or unreadable"
    if actual is None:
        return False, "LLM response missing or not valid JSON"
    if actual == expected:
        return True, "Exact match"
    # Build a light diff summary
    def issues_info(d: Dict[str, Any]) -> tuple[int, set]:
        issues = d.get("issues")
        if isinstance(issues, list):
            types = set()
            for it in issues:
                if isinstance(it, dict) and "type" in it:
                    types.add(str(it.get("type")))
            return len(issues), types
        return 0, set()

    a_count, a_types = issues_info(actual)
    e_count, e_types = issues_info(expected)
    msg = (
        f"Mismatch: issues count actual={a_count} expected={e_count}; "
        f"types actual={sorted(a_types)} expected={sorted(e_types)}"
    )
    return False, msg


def find_test_dir() -> str:
    """Return the root tests directory, preferring 'tests' then 'test'."""
    candidates = ["tests", "test"]
    for p in candidates:
        if os.path.isdir(p):
            return p
    return candidates[0]


def iter_source_files(root: str):
    """Yield .java source files under root recursively, skipping expected JSON files."""
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith("-expected.json"):
                continue
            if name.lower().endswith(".java"):
                yield os.path.join(dirpath, name)


def main() -> None:
    model = os.getenv("MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://litellm.labs.jb.gg/")

    if not api_key:
        print("Warning: OPENAI_API_KEY is not set; requests will likely fail.", file=sys.stderr)

    client = openai.OpenAI(api_key=api_key, base_url=base_url)

    # Batch mode: iterate all files in tests/java (or test/java)
    test_dir = find_test_dir()
    print(f"Scanning directory: {test_dir}")
    start_time = time.time()
    total = 0
    passed = 0
    failed = 0
    missing = 0

    for src in iter_source_files(test_dir):
        total += 1
        print(f"\n=== Analyzing: {src} ===")
        actual, raw = analyze_file(src, client, model)
        # Always write the actual result for each file
        actual_path = actual_path_for(src)
        actual_to_write: Dict[str, Any]
        if actual is not None:
            actual_to_write = actual
        else:
            actual_to_write = {"file": src, "issues": [], "raw": raw}
        if write_json(actual_path, actual_to_write):
            print(f"Wrote actual result: {actual_path}")
        else:
            print(f"Failed to write actual result: {actual_path}", file=sys.stderr)

        expected_path = expected_path_for(src)
        expected = load_json(expected_path)

        if expected is None:
            # Create expected file from LLM output
            to_write: Dict[str, Any]
            if actual is not None:
                to_write = actual
            else:
                to_write = {"file": src, "issues": [], "raw": raw}
            if write_json(expected_path, to_write):
                missing += 1  # count how many were created
                ok, note = True, "Expected missing: created from LLM output"
            else:
                ok, note = False, "Failed to create expected result file"
            if ok:
                passed += 1
            else:
                failed += 1
            print(note)
            print(f"Expected file: {expected_path}")
            print(f"Result: {'PASS' if ok else 'FAIL'}")
            continue

        ok, note = compare_results(actual, expected)
        if ok:
            passed += 1
        else:
            failed += 1
        print(note)
        print(f"Expected file: {expected_path}")
        print(f"Result: {'PASS' if ok else 'FAIL'}")

    print("\n===== Summary =====")
    elapsed = time.time() - start_time
    print(f"Total files: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Missing expected: {missing}")
    print(f"Total time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
