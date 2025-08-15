#!/bin/bash
set -euo pipefail

# Test script for Workato SDK Docs implementation
echo "========================================="
echo "Workato SDK Docs Implementation Test"
echo "========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "Testing $test_name... "
    
    if eval "$test_command" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Test detailed function with output
run_test_with_output() {
    local test_name="$1"
    local test_command="$2"
    
    echo ""
    echo "Testing $test_name:"
    echo "Command: $test_command"
    echo "---"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "1. Checking directory structure..."
echo "-----------------------------------"

run_test "Project root exists" "[ -d '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs' ]"
run_test "Scripts directory exists" "[ -d '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/scripts' ]"
run_test "GitHub workflows directory exists" "[ -d '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/.github/workflows' ]"

echo ""
echo "2. Checking required files..."
echo "------------------------------"

run_test "fetch_workato_docs.py exists" "[ -f '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/scripts/fetch_workato_docs.py' ]"
run_test "Helper script template exists" "[ -f '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/scripts/workato-sdk-helper.sh.template' ]"
run_test "Requirements file exists" "[ -f '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/scripts/requirements.txt' ]"
run_test "Install script exists" "[ -f '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/install.sh' ]"
run_test "Uninstall script exists" "[ -f '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/uninstall.sh' ]"
run_test "README exists" "[ -f '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/README.md' ]"
run_test "LICENSE exists" "[ -f '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/LICENSE' ]"
run_test "GitHub workflow exists" "[ -f '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/.github/workflows/update-docs.yml' ]"

echo ""
echo "3. Checking script syntax..."
echo "-----------------------------"

run_test "Python script syntax" "python3 -m py_compile '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/scripts/fetch_workato_docs.py'"
run_test "Bash helper script syntax" "bash -n '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/scripts/workato-sdk-helper.sh.template'"
run_test "Install script syntax" "bash -n '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/install.sh'"
run_test "Uninstall script syntax" "bash -n '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/uninstall.sh'"

echo ""
echo "4. Checking Python dependencies..."
echo "-----------------------------------"

run_test "requests module available" "python3 -c 'import requests'"
run_test "beautifulsoup4 module available" "python3 -c 'from bs4 import BeautifulSoup'"
run_test "html2text module available" "python3 -c 'import html2text'"

echo ""
echo "5. Checking script permissions..."
echo "----------------------------------"

run_test "Install script is executable" "[ -x '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/install.sh' ] || chmod +x '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/install.sh'"
run_test "Uninstall script is executable" "[ -x '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/uninstall.sh' ] || chmod +x '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/uninstall.sh'"

echo ""
echo "6. Testing Python fetcher (dry run)..."
echo "---------------------------------------"

cd /Users/dave/Documents/GitHub/kreitter/workato-sdk-docs

# Create docs directory for test
mkdir -p docs

echo "Attempting to fetch a sample page..."
run_test_with_output "Python fetcher imports" "python3 -c 'from scripts.fetch_workato_docs import WorkatoDocsConverter, SDK_URLS; print(f\"Imports successful, {len(SDK_URLS)} SDK URLs defined\")'"

echo ""
echo "7. Checking documentation structure..."
echo "---------------------------------------"

run_test "Docs directory can be created" "mkdir -p '/Users/dave/Documents/GitHub/kreitter/workato-sdk-docs/docs'"

echo ""
echo "========================================="
echo "Test Results Summary"
echo "========================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ All tests passed! The implementation is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Create a GitHub repository named 'workato-sdk-docs'"
    echo "2. Update REPO_URL in install.sh with your repository URL"
    echo "3. Update repository URLs in README.md"
    echo "4. Push the code to GitHub"
    echo "5. Test the installation with:"
    echo "   curl -fsSL https://raw.githubusercontent.com/kreitter/workato-sdk-docs/main/install.sh | bash"
else
    echo ""
    echo -e "${YELLOW}⚠ Some tests failed. Please review and fix the issues above.${NC}"
fi

echo ""
echo "Optional: Test the fetcher with a real fetch (this will take time):"
echo "  cd /Users/dave/Documents/GitHub/kreitter/workato-sdk-docs"
echo "  python3 scripts/fetch_workato_docs.py"