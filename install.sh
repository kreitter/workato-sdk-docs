#!/bin/bash
set -euo pipefail

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "This installer has been replaced with a modern Python version"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Please use the new installer:"
echo ""
echo "  uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install"
echo ""
echo "Don't have uv? Install it first:"
echo "  • macOS:  brew install uv"
echo "  • Linux:  curl -LsSf https://astral.sh/uv/install.sh | sh"
echo "  • Docs:   https://docs.astral.sh/uv/"
echo ""
echo "The new installer handles Python dependencies automatically and"
echo "avoids PEP 668 'externally managed environment' errors."
echo ""
exit 1
