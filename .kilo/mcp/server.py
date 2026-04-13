"""
Test Automation MCP Server

Provides tools for running and managing Playwright Python BDD tests via MCP protocol.
"""

import subprocess
import os
from pathlib import Path
from typing import Optional

# Character limit for responses
CHARACTER_LIMIT = 25000


def _run_pytest(args: list[str], timeout: int = 300) -> dict:
    """Run pytest with given arguments and return parsed results."""
    env = os.environ.copy()
    env["AUTO_GENERATE_ALLURE"] = "false"
    env["AUTO_OPEN_ALLURE"] = "false"
    
    # Use --no-header to reduce output noise
    cmd = ["pytest"] + args + ["--tb=line", "-q", "-p", "no:allure"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd(),
            env=env
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout[:CHARACTER_LIMIT],
            "stderr": result.stderr[:2000]
        }
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": "Test execution timed out"}
    except Exception as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e)}


def collect_tests() -> dict:
    """Collect all tests without running them."""
    return _run_pytest(["--collect-only", "-q"], timeout=60)


def run_tests_by_marker(marker: str) -> dict:
    """Run tests matching a specific marker (e.g., TC6, regression, api)."""
    return _run_pytest(["-m", marker])


def run_tests_by_keyword(keyword: str) -> dict:
    """Run tests matching a keyword in test name."""
    return _run_pytest(["-k", keyword])


def get_test_status() -> dict:
    """Get summary of last test run status."""
    result = collect_tests()
    return {
        "status": "ready" if result["returncode"] == 0 else "error",
        "message": result.get("stderr", "")
    }


def list_test_markers() -> list:
    """List available pytest markers from pytest.ini."""
    pytest_ini = Path("pytest.ini")
    if not pytest_ini.exists():
        return ["api", "ui", "regression", "TC"]
    
    content = pytest_ini.read_text()
    markers = []
    in_markers = False
    for line in content.split("\n"):
        if line.strip().startswith("markers"):
            in_markers = True
            continue
        if in_markers and line.strip().startswith("["):
            break
        if in_markers and line.strip():
            markers.append(line.strip().split(":")[0])
    return markers


def list_test_files() -> list:
    """List all feature files in the test suite."""
    features_dir = Path("tests/features")
    if not features_dir.exists():
        return []
    
    files = []
    for f in features_dir.rglob("*.feature"):
        rel = f.relative_to(features_dir)
        files.append(str(rel))
    return sorted(files)


def get_test_results() -> dict:
    """Get summary of test results from last run."""
    results = _run_pytest(["--tb=no", "-q"])
    
    # Parse summary from output
    stdout = results.get("stdout", "")
    passed = failed = 0
    
    if "passed" in stdout:
        import re
        match = re.search(r"(\d+)\s+passed", stdout)
        if match:
            passed = int(match.group(1))
        match = re.search(r"(\d+)\s+failed", stdout)
        if match:
            failed = int(match.group(1))
    
    return {
        "passed": results["returncode"] == 0,
        "passed_count": passed,
        "failed_count": failed,
        "output": stdout[:3000]
    }


# Export available functions
__all__ = [
    "collect_tests",
    "run_tests_by_marker", 
    "run_tests_by_keyword",
    "get_test_status",
    "list_test_markers",
    "list_test_files",
    "get_test_results"
]
