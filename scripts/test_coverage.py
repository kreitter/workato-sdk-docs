#!/usr/bin/env python3
"""
Coverage analysis script for Workato SDK Documentation Mirror.

Generates detailed coverage reports and identifies areas needing more testing.
"""

import subprocess
import sys
from pathlib import Path


def run_coverage():
    """Run tests with coverage and generate reports."""
    print("🔍 Running coverage analysis...")

    # Run tests with coverage
    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/",
        "--cov=scripts",
        "--cov=workato_sdk_docs",
        "--cov-report=html",
        "--cov-report=term",
        "--cov-report=xml",
        "-v",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)

    return result.returncode == 0


def analyze_coverage_gaps():
    """Analyze coverage gaps and suggest improvements."""
    print("\n📊 Coverage Analysis:")
    print("-" * 50)

    # Check coverage XML report
    coverage_file = Path("coverage.xml")
    if not coverage_file.exists():
        print("❌ No coverage.xml found. Run tests with --cov-report=xml first.")
        return

    try:
        import xml.etree.ElementTree as ET

        tree = ET.parse(coverage_file)
        root = tree.getroot()

        # Get overall coverage
        coverage = root.get("line-rate")
        if coverage:
            coverage_pct = float(coverage) * 100
            print(f"Overall coverage: {coverage_pct:.1f}%")

            if coverage_pct < 70:
                print("⚠️  Coverage below 70% - needs improvement")
            elif coverage_pct < 85:
                print("✅ Coverage at 70-85% - good foundation")
            else:
                print("🎉 Coverage above 85% - excellent!")

        # Analyze by file
        print("\n📁 Coverage by file:")
        for package in root.findall(".//package"):
            for class_elem in package.findall("classes/class"):
                filename = class_elem.get("filename")
                line_rate = class_elem.get("line-rate")
                if line_rate:
                    rate_pct = float(line_rate) * 100
                    status = "✅" if rate_pct > 80 else "⚠️" if rate_pct > 50 else "❌"
                    print(f"  {status} {filename}: {rate_pct:.1f}%")

    except Exception as e:
        print(f"Error analyzing coverage: {e}")


def main():
    """Main function."""
    print("🧪 Workato SDK Documentation Mirror - Coverage Analysis")
    print("=" * 60)

    success = run_coverage()

    if success:
        analyze_coverage_gaps()
        print("\n✅ Coverage analysis complete!")
        print("\n💡 Next steps:")
        print("1. View HTML report: open htmlcov/index.html")
        print("2. Upload to Codecov: check GitHub Actions workflow")
        print("3. Identify low-coverage areas and add tests")
    else:
        print("\n❌ Coverage analysis failed!")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
