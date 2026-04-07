import os
import re
import sys


def main() -> int:
    # Best-effort extraction; hooks can vary by host/runtime.
    cmd = os.environ.get("CURSOR_COMMAND", "") or os.environ.get("command", "")
    command = cmd.lower()

    blocked_patterns = [
        r"git\s+reset\s+--hard",
        r"git\s+checkout\s+--\s",
        r"git\s+clean\s+-fd",
        r"git\s+push\s+--force",
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, command):
            print(
                "[QA Agentic] Blocked unsafe git command for project safety. "
                "Use a safer alternative."
            )
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
