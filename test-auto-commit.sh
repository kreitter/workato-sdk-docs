#!/bin/bash
set -x  # Enable debug output

DOCS_PATH="$HOME/.workato-sdk-docs"
cd "$DOCS_PATH" || exit 1

echo "=== Testing auto-commit function ==="
echo "Current directory: $(pwd)"
echo ""

# Check if there are any changes
echo "=== Checking for changes ==="
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

echo "Changes detected!"
echo ""

# Check if ALL changes are only timestamp updates in docs
echo "=== Checking for non-doc changes ==="
non_timestamp_changes=$(git diff --name-only | grep -v "^docs/.*\.md$" | grep -v "^docs/docs_manifest.json$" || true)
if [[ -n "$non_timestamp_changes" ]]; then
    echo "Found non-doc changes:"
    echo "$non_timestamp_changes"
    exit 0
fi

echo "All changes are in docs/"
echo ""

# Check if the only changes in md files are timestamp lines
echo "=== Checking if changes are timestamp-only ==="
has_non_timestamp_changes=0
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        echo "Checking file: $file"
        # Check if changes are only in the "Fetched:" line
        diff_lines=$(git diff "$file" | grep "^[+-]" | grep -v "^[+-][+-][+-]" | grep -v "^[+-]> \*\*Fetched\*\*:" || true)
        if [[ -n "$diff_lines" ]]; then
            echo "Found non-timestamp changes in $file:"
            echo "$diff_lines"
            has_non_timestamp_changes=1
            break
        else
            echo "  - Only timestamp changes"
        fi
    fi
done < <(git diff --name-only)

if [[ $has_non_timestamp_changes -eq 1 ]]; then
    echo "There are non-timestamp changes, exiting"
    exit 0
fi

echo ""
echo "=== All changes are timestamp-only! ==="
echo "Would commit and push these changes"

# Show what would be committed
echo ""
echo "=== Files to be committed ==="
git diff --name-only