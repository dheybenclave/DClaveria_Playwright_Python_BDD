import os
import platform
import sys
from pathlib import Path


REQUIRED_MODULES = [
    "pytest",
    "playwright",
    "pytest_bdd",
    "dotenv",
]

REQUIRED_ENV_KEYS = ["BASE_URL", "HEADLESS"]
OPTIONAL_ENV_KEYS = ["RECORD_VIDEO", "ADMIN_EMAIL", "ADMIN_PASSWORD", "LIST_OF_CREDENTIALS"]


def check_python() -> bool:
    version = sys.version_info
    ok = (version.major, version.minor) >= (3, 8)
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] Python version: {platform.python_version()} (requires >= 3.8)")
    return ok


def check_venv() -> bool:
    in_venv = sys.prefix != sys.base_prefix or bool(os.environ.get("VIRTUAL_ENV"))
    status = "PASS" if in_venv else "WARN"
    print(f"[{status}] Virtual environment active: {in_venv}")
    return in_venv


def check_modules() -> bool:
    all_ok = True
    for module_name in REQUIRED_MODULES:
        try:
            __import__(module_name)
            print(f"[PASS] Import module: {module_name}")
        except Exception:
            all_ok = False
            print(f"[FAIL] Import module: {module_name}")
    return all_ok


def parse_env_file(env_path: Path) -> dict:
    data = {}
    if not env_path.exists():
        return data

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def mask_value(value: str) -> str:
    if not value:
        return "(empty)"
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}***{value[-2:]}"


def check_env_file() -> bool:
    env_path = Path(".env")
    if not env_path.exists():
        print("[WARN] .env file not found")
        return False

    print("[PASS] .env file found")
    values = parse_env_file(env_path)
    required_ok = True

    for key in REQUIRED_ENV_KEYS:
        if key in values and values[key] != "":
            print(f"[PASS] .env key present: {key}")
        else:
            required_ok = False
            print(f"[FAIL] .env key missing/empty: {key}")

    for key in OPTIONAL_ENV_KEYS:
        if key in values and values[key] != "":
            print(f"[INFO] .env optional key present: {key}={mask_value(values[key])}")

    return required_ok


def main() -> int:
    print("=== Init Environment Verification ===")
    python_ok = check_python()
    check_venv()
    modules_ok = check_modules()
    env_ok = check_env_file()

    print("=== Summary ===")
    print(f"Python: {'PASS' if python_ok else 'FAIL'}")
    print(f"Dependencies: {'PASS' if modules_ok else 'FAIL'}")
    print(f"Env file: {'PASS' if env_ok else 'FAIL'}")

    return 0 if python_ok and modules_ok and env_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
