import os
import re
import sys


def main() -> int:
    prompt = os.environ.get("CLAUDE_USER_PROMPT", "")
    patterns = [r"sk-[a-zA-Z0-9]{20,}", r"ghp_[a-zA-Z0-9]{20,}", r"AKIA[0-9A-Z]{16}"]
    for pattern in patterns:
        if re.search(pattern, prompt):
            print("[Claude QA Agentic] Possible secret detected in prompt.")
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
