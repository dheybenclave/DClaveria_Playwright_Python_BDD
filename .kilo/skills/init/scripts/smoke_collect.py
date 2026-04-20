import subprocess
import sys


def run_collect() -> int:
    command = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    print(f"Running: {' '.join(command)}")
    completed = subprocess.run(command, check=False)
    if completed.returncode == 0:
        print("[PASS] pytest collection succeeded")
    else:
        print(f"[FAIL] pytest collection failed with exit code {completed.returncode}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(run_collect())
