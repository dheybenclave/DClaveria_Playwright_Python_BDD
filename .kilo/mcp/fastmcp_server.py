"""
FastMCP Test Automation Server

MCP server that provides test automation tools for the Playwright Python BDD framework.
Uses FastMCP to expose test runner functions as MCP tools.
"""

import subprocess
import os
from pathlib import Path

from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("TestAutomationServer")


def run_pytest(args: list[str], timeout: int = 300) -> dict:
    """Run pytest with given arguments and return parsed results."""
    cmd = ["pytest"] + args + ["--tb=short", "-q"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout[:5000],
            "stderr": result.stderr[:2000]
        }
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": "Test execution timed out"}
    except Exception as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e)}


@mcp.tool()
def run_collect() -> str:
    """
    Collect all tests without running them.
    
    Use this to discover available tests and verify test discovery works.
    Returns the list of collected tests.
    """
    result = run_pytest(["--collect-only", "-q"])
    output = result.get("stdout", "")
    if result["returncode"] == 0:
        return f"Test collection successful.\n\n{output}"
    return f"Collection failed: {result.get('stderr', output)}"


@mcp.tool()
def run_by_marker(marker: str) -> str:
    """
    Run tests matching a specific pytest marker.
    
    Args:
        marker: Test marker to filter by (e.g., 'TC6', 'regression', 'api', 'ui')
    
    Returns:
        Test execution results for matching tests.
    """
    result = run_pytest(["-m", marker])
    output = result.get("stdout", "")
    if result["returncode"] == 0:
        return f"Tests for marker '{marker}' passed.\n\n{output}"
    return f"Tests for marker '{marker}' failed.\n\n{output}"


@mcp.tool()
def run_by_keyword(keyword: str) -> str:
    """
    Run tests matching a keyword in test name.
    
    Args:
        keyword: Keyword to filter test names (e.g., 'login', 'products', 'checkout')
    
    Returns:
        Test execution results for matching tests.
    """
    result = run_pytest(["-k", keyword])
    output = result.get("stdout", "")
    if result["returncode"] == 0:
        return f"Tests matching '{keyword}' passed.\n\n{output}"
    return f"Tests matching '{keyword}' failed.\n\n{output}"


@mcp.tool()
def list_markers() -> str:
    """
    List all available pytest markers.
    
    Returns a list of markers defined in pytest.ini for filtering tests.
    """
    pytest_ini = Path("pytest.ini")
    if not pytest_ini.exists():
        return "Available markers: api, ui, regression, TC"
    
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
    
    if markers:
        return "Available markers:\n" + "\n".join(f"  - {m}" for m in markers)
    return "Available markers: api, ui, regression, TC"


@mcp.tool()
def list_features() -> str:
    """
    List all available feature files.
    
    Returns the list of .feature files available for test execution.
    """
    features_dir = Path("tests/features")
    if not features_dir.exists():
        return "No feature files found."
    
    files = []
    for f in features_dir.rglob("*.feature"):
        rel = f.relative_to(features_dir)
        files.append(str(rel))
    
    if files:
        return "Available feature files:\n" + "\n".join(f"  - {f}" for f in sorted(files))
    return "No feature files found."


@mcp.tool()
def run_smoke() -> str:
    """
    Run smoke tests (typically marked with @smoke or @regression).
    
    Returns execution results for the smoke test suite.
    """
    result = run_pytest(["-m", "regression"])
    output = result.get("stdout", "")
    if result["returncode"] == 0:
        return f"Smoke tests passed.\n\n{output}"
    return f"Smoke tests failed.\n\n{output}"


def main():
    """Entry point for running the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
