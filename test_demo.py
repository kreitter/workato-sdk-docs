#!/usr/bin/env python3
"""
Demonstration script showing how the testing suite works.

This script shows the testing integration in action and can be used
to verify that tests run correctly in the development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and show results."""
    print(f"\n🧪 {description}")
    print(f"Command: {cmd}")

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent
        )

        if result.stdout:
            print("Output:")
            print(result.stdout)

        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ PASSED")
        else:
            print(f"❌ FAILED (exit code: {result.returncode})")

        return result.returncode == 0

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Demonstrate the testing suite."""
    print("🚀 Workato SDK Documentation Mirror - Testing Suite Demo")
    print("=" * 60)

    project_root = Path(__file__).parent
    test_dir = project_root / "tests"

    if not test_dir.exists():
        print("❌ Tests directory not found!")
        return 1

    success_count = 0
    total_tests = 0

    # Test 1: Check if pytest is available
    if run_command("uv run python -m pytest --version", "Checking pytest availability"):
        success_count += 1
    total_tests += 1

    # Test 2: Run basic setup tests
    if run_command(
        "uv run python -m pytest tests/test_basic_setup.py -v", "Running basic setup tests"
    ):
        success_count += 1
    total_tests += 1

    # Test 3: Run unit tests
    if run_command("uv run python -m pytest tests/test_unit_*.py -v", "Running unit tests"):
        success_count += 1
    total_tests += 1

    # Test 4: Check test coverage
    if run_command(
        "uv run python -m pytest tests/test_basic_setup.py --cov=scripts --cov-report=term",
        "Checking test coverage",
    ):
        success_count += 1
    total_tests += 1

    # Test 5: Check if integration tests exist (don't run them as they might need network)
    integration_files = list(test_dir.glob("test_integration_*.py"))
    if integration_files:
        print(f"\n✅ Found {len(integration_files)} integration test files")
        success_count += 1
    else:
        print("\n⚠️  No integration test files found")
    total_tests += 1

    # Summary
    print(f"\n{'=' * 60}")
    print(f"📊 Test Summary: {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("🎉 All tests passed! The testing suite is working correctly.")
        print("\nNext steps:")
        print("1. Add more test cases to tests/test_unit_core.py")
        print("2. Implement integration tests in tests/test_integration_*.py")
        print("3. Add regression tests in tests/test_regression_*.py")
        print("4. Set up pre-commit hooks: make setup-precommit")
        print("5. Run tests in CI/CD with the GitHub Actions workflow")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
