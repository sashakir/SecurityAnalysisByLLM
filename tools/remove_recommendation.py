#!/usr/bin/env python3
import json
import os
import sys
from typing import Any, Dict

ROOT = os.path.dirname(os.path.dirname(__file__))
TEST_DIR = os.path.join(ROOT, "tests", "java")


def strip_recommendation(obj: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        return obj
    issues = obj.get("issues")
    if isinstance(issues, list):
        for it in issues:
            if isinstance(it, dict) and "recommendation" in it:
                it.pop("recommendation", None)
    return obj


def process_file(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Skipping {path}: failed to read/parse JSON: {e}", file=sys.stderr)
        return False
    before = json.dumps(data, sort_keys=True)
    data = strip_recommendation(data)
    after = json.dumps(data, sort_keys=True)
    if before == after:
        # no change
        return True
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {path}")
        return True
    except Exception as e:
        print(f"Failed to write {path}: {e}", file=sys.stderr)
        return False


def main() -> int:
    if not os.path.isdir(TEST_DIR):
        print(f"Test dir not found: {TEST_DIR}", file=sys.stderr)
        return 1
    ok = True
    for name in os.listdir(TEST_DIR):
        if not (name.endswith("-expected.json") or name.endswith("-actual.json")):
            continue
        path = os.path.join(TEST_DIR, name)
        if not process_file(path):
            ok = False
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
