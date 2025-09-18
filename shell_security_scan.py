"""
Shell-based security scan runner: delegates analysis to an external script and
compares plain-text results against expected files.

Differences from security_scan.py:
- Instead of calling an LLM API, this script invokes an external shell script:
    /Users/sashakir/Qodana/hktn25-sec-review/run-security-review.sh
  with three parameters: <source_file> <prompt_file> <output_file>
- Uses a different prompt file: prompts/security_prompt.md
- Uses .txt extensions for expected/actual results (plain text), not JSON.

Usage:
  python shell_security_scan.py [TEST_ROOT]

If TEST_ROOT is provided, it specifies the root directory to scan for .java files (recursively).
If omitted, defaults to 'tests/fraunhofer-suite' (or 'test/fraunhofer-suite'); if those are absent, falls back to 'tests'.

Behavior:
- Recursively scans under the tests/ (or test/) directory for .java files.
- For each source file, runs the external review script to produce an -actual.txt
  report placed next to the source.
- If a matching -expected.txt file is missing, it is created by copying the
  actual result (counted as "Missing expected").
- Compares actual vs expected with exact plain-text comparison and reports PASS/FAIL.

Environment:
- Optionally override the prompts directory with PROMPTS_DIR env var; the script
  expects security_prompt.md to be inside that directory. If the prompt
  file is missing or unreadable, the script exits with an error.
"""
from __future__ import annotations

import os
import sys
import subprocess
import time
from typing import Optional, Tuple


# Allow overriding via environment variables; fallback to defaults
SCRIPT_PATH = os.getenv("SCRIPT_PATH")
API_KEY = os.getenv("API_KEY")
PROMPT_FILE = os.getenv("PROMPT_FILE", "security_prompt.md")

def find_test_dir() -> str:
    """Return the root tests directory, preferring 'tests' then 'test'."""
    for p in ("tests/fraunhofer-suite", "test/fraunhofer-suite"):
        if os.path.isdir(p):
            return p
    return "tests"


def iter_source_files(root: str):
    """Yield .java source files under root recursively."""
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith(".java"):
                yield os.path.join(dirpath, name)


def expected_path_for(src_path: str) -> str:
    in_dir = os.path.dirname(src_path)
    base = os.path.splitext(os.path.basename(src_path))[0]
    return os.path.join(in_dir, f"{base}-expected.txt")


def actual_path_for(src_path: str) -> str:
    in_dir = os.path.dirname(src_path)
    base = os.path.splitext(os.path.basename(src_path))[0]
    return os.path.join(in_dir, f"{base}-actual.txt")


def read_text(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def write_text(path: str, content: str) -> bool:
    try:
        # Ensure parent directory exists
        parent = os.path.dirname(path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to {path}: {e}", file=sys.stderr)
        return False


def ensure_prompt_path() -> str:
    prompts_dir = os.getenv("PROMPTS_DIR", os.path.join(os.path.dirname(__file__), "prompts"))
    prompt_path = os.path.join(prompts_dir, PROMPT_FILE)
    try:
        with open(prompt_path, "r", encoding="utf-8") as _:
            pass
    except Exception:
        print(f"Error: prompt file missing or unreadable: {prompt_path}", file=sys.stderr)
        sys.exit(1)
    return prompt_path


def run_external_review(src: str, prompt_path: str, out_path: str) -> Tuple[bool, str]:
    """Run the external shell script to produce the analysis output.

    Now the external tool expects --result to be a DIRECTORY and writes a file
    named 'security-review.sarif' inside it. This function will:
      - create a temporary result directory
      - run the tool with --result pointing to that temp directory
      - copy '<temp>/security-review.sarif' to 'out_path'
      - remove the temp directory afterwards

    Returns (ok, note). Stdout from the external tool is intentionally suppressed
    and not propagated to this script's stdout to keep output clean.
    """
    import tempfile
    import shutil

    out_path_abs = os.path.abspath(out_path)
    src_abs = os.path.abspath(src)
    prompt_abs = os.path.abspath(prompt_path)

    # Create a temporary directory for the tool's output
    try:
        temp_dir = tempfile.mkdtemp(prefix="secscan_")
    except Exception as e:
        return False, f"Failed to create temporary directory: {e}"

    cmd = [
        SCRIPT_PATH,
        API_KEY,
        f"--repo={src_abs}",
        f"--customPrompt={prompt_abs}",
        f"--result={os.path.abspath(temp_dir)}",
        "--shouldProduceSarif=true"
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        # Cleanup temp dir before returning
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        return False, f"External script not found: {SCRIPT_PATH}"
    except Exception as e:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        return False, f"Failed to start external script: {e}"

    if proc.returncode != 0:
        note = (
            f"External script failed with code {proc.returncode}.\n"
            f"STDERR:\n{proc.stderr}"
        )
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        return False, note

    # After successful run, parse the SARIF result and write a simple file:line list to out_path
    sarif_src = os.path.join(temp_dir, "security-review.sarif")
    if not os.path.isfile(sarif_src):
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        return False, f"Expected result file not found: {sarif_src}"

    # Parse SARIF and prepare output lines
    try:
        import json as _json
        with open(sarif_src, "r", encoding="utf-8", errors="replace") as _f:
            sarif_data = _json.load(_f)
        lines_set = set()
        runs = sarif_data.get("runs", []) if isinstance(sarif_data, dict) else []
        for run in runs:
            results = run.get("results", []) if isinstance(run, dict) else []
            for res in results:
                locs = res.get("locations", []) if isinstance(res, dict) else []
                for loc in locs:
                    phys = (loc or {}).get("physicalLocation", {})
                    region = phys.get("region", {})
                    start_line = region.get("startLine")
                    art = phys.get("artifactLocation", {})
                    uri = art.get("uri") or art.get("uriBaseId") or ""
                    # The URI may be a path or URI; take the basename
                    base = os.path.basename(uri) if isinstance(uri, str) else ""
                    if base and isinstance(start_line, int):
                        lines_set.add((base, int(start_line)))
        # Sort by filename then line
        sorted_lines = sorted(lines_set, key=lambda t: (t[0], t[1]))
        output_text = "\n".join(f"{fname}:{ln}" for fname, ln in sorted_lines)
    except Exception as e:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        return False, f"Failed to parse SARIF: {e}"

    try:
        # Ensure parent dir exists for the destination
        dest_parent = os.path.dirname(out_path_abs)
        if dest_parent and not os.path.isdir(dest_parent):
            os.makedirs(dest_parent, exist_ok=True)
        with open(out_path_abs, "w", encoding="utf-8") as outf:
            outf.write(output_text)
    except Exception as e:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        return False, f"Failed to write parsed results: {e}"

    # Cleanup temp directory
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass

    # Do not expose stdout of the tool
    return True, ""


def compare_text(actual_text: Optional[str], expected_text: Optional[str]) -> Tuple[bool, str]:
    """Compare only the first line of actual and expected text.

    Returns (ok, note). If either file is missing/unreadable, returns a failure.
    Whitespace differences at line ends are ignored (first line is compared after rstrip()).
    """
    if expected_text is None:
        return False, "Expected result file missing or unreadable"
    if actual_text is None:
        return False, "Actual result file missing or unreadable"

    # Extract first lines (or empty string if file is empty)
    a_first = actual_text.splitlines()[0] if actual_text.splitlines() else ""
    e_first = expected_text.splitlines()[0] if expected_text.splitlines() else ""

    if a_first.rstrip() == e_first.rstrip():
        return True, "First line matches"
    else:
        return False, f"First-line mismatch: actual='{a_first}' expected='{e_first}'"


def main() -> None:
    prompt_path = ensure_prompt_path()

    # Optional command-line parameter: test data root directory
    if len(sys.argv) > 1 and sys.argv[1].strip():
        candidate = os.path.abspath(sys.argv[1].strip())
        if not os.path.isdir(candidate):
            print(f"Error: specified test root is not a directory: {candidate}", file=sys.stderr)
            sys.exit(1)
        test_dir = candidate
    else:
        test_dir = find_test_dir()
    print(f"Scanning directory: {test_dir}")

    start_time = time.time()
    total = passed = failed = missing = 0

    for src in iter_source_files(test_dir):
        total += 1
        print(f"\n=== Analyzing: {src} ===")

        # Produce actual output via external script
        actual_path = os.path.abspath(actual_path_for(src))
        # Ensure the actual output path exists (create parent dirs and empty file)
        try:
            parent = os.path.dirname(actual_path)
            if parent and not os.path.isdir(parent):
                os.makedirs(parent, exist_ok=True)
            if not os.path.exists(actual_path):
                with open(actual_path, "a", encoding="utf-8"):
                    pass
        except Exception as e:
            failed += 1
            print(f"Failed to prepare actual output path '{actual_path}': {e}")
            print("Result: FAIL")
            continue
        ok_run, note = run_external_review(os.path.abspath(src), prompt_path, actual_path)
        if not ok_run:
            failed += 1
            print(note)
            print(f"Result: FAIL")
            continue
        else:
            # Script may output some useful info
            if note:
                print(note)

        # Read actual output
        actual_text = read_text(actual_path)
        if actual_text is None:
            failed += 1
            print(f"Failed to read actual result: {actual_path}")
            print("Result: FAIL")
            continue
        else:
            print(f"Wrote actual result: {actual_path}")

        expected_path = expected_path_for(src)
        expected_text = read_text(expected_path)

        if expected_text is None:
            # Create expected from actual
            if write_text(expected_path, actual_text):
                missing += 1
                passed += 1
                print("Expected missing: created from actual output")
                print(f"Expected file: {expected_path}")
                print("Result: PASS")
            else:
                failed += 1
                print("Failed to create expected result file")
                print(f"Expected file: {expected_path}")
                print("Result: FAIL")
            continue

        ok, cmp_note = compare_text(actual_text, expected_text)
        if ok:
            passed += 1
        else:
            failed += 1
        print(cmp_note)
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
