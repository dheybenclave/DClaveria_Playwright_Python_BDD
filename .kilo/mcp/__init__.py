"""
Test Automation MCP Server

Provides MCP tools for running Playwright Python BDD tests.
"""

from .server import (
    collect_tests,
    run_tests_by_marker,
    run_tests_by_keyword,
    get_test_status,
    list_test_markers,
    list_test_files,
    get_test_results
)

__version__ = "1.0.0"
__all__ = [
    "collect_tests",
    "run_tests_by_marker", 
    "run_tests_by_keyword",
    "get_test_status",
    "list_test_markers",
    "list_test_files",
    "get_test_results"
]
