#!/usr/bin/env python3
"""
Test runner script for Workato SDK Documentation Mirror.

Usage:
    python tests/run_tests.py          # Run all tests
    python tests/run_tests.py unit     # Run only unit tests
    python tests/run_tests.py --cov    # Run with coverage report
"""

import subprocess
import sys


def run_command(cmd):
    """Run a command and return the result."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result


def main():
    """Main test runner function."""
    args = sys.argv[1:]

    # Base command
    base_cmd = "python -m pytest tests/"

    # Add coverage if requested
    if "--cov" in args or "--coverage" in args:
        base_cmd += " --cov=scripts --cov=workato_sdk_docs --cov-report=html --cov-report=term"

    # Filter tests if specific type requested
    test_types = {
        "unit": "test_unit_*.py",
        "integration": "test_integration_*.py",
        "regression": "test_regression_*.py",
        "performance": "test_performance.py",
    }

    for test_type, pattern in test_types.items():
        if test_type in args:
            base_cmd += f" -k '{pattern}'"
            break

    # Add verbose output
    base_cmd += " -v"

    print(f"Running: {base_cmd}")
    result = run_command(base_cmd)

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
