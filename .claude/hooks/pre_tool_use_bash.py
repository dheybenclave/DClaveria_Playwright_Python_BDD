import os
import re
import sys


def main() -> int:
    payload = os.environ.get("CLAUDE_TOOL_INPUT", "")
    command = payload.lower()

    blocked_patterns = [
        r"git\s+reset\s+--hard",
        r"git\s+checkout\s+--\s",
        r"git\s+clean\s+-fd",
        r"git\s+push\s+--force",
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, command):
            print("[Claude QA Agentic] Blocked unsafe git command.")
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
