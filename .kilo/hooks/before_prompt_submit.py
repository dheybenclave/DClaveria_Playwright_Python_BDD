import os
import re


def main() -> int:
    prompt = os.environ.get("KILO_PROMPT", "") or os.environ.get("prompt", "")
    if not prompt:
        return 0

    patterns = [r"sk-[a-zA-Z0-9]{20,}", r"ghp_[a-zA-Z0-9]{20,}", r"AKIA[0-9A-Z]{16}"]
    for pattern in patterns:
        if re.search(pattern, prompt):
            print("[Kilo QA Agentic] Possible secret detected in prompt. Remove sensitive values.")
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
