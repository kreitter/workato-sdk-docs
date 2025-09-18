#!/bin/bash

DOCS_PATH="$HOME/.workato-sdk-docs"
cd "$DOCS_PATH" || exit 1

echo "=== Testing auto-commit function ==="

# Check if there are any changes
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

# Check if ALL changes are only in docs/*.md and docs_manifest.json
non_doc_changes=$(git diff --name-only | grep -v "^docs/.*\.md$" | grep -v "^docs/docs_manifest.json$" || true)
if [[ -n "$non_doc_changes" ]]; then
    echo "Found non-doc changes, exiting"
    exit 0
fi

# Check if the only changes in md files are timestamp/metadata updates
has_non_timestamp_changes=0
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        if [[ "$file" == "docs/docs_manifest.json" ]]; then
            # For manifest file, allow any changes since it's auto-generated metadata
            echo "  - $file: auto-generated metadata (allowed)"
            continue
        elif [[ "$file" == docs/*.md ]]; then
            # For markdown files, check if changes are only in the "Fetched:" line
            diff_lines=$(git diff "$file" | grep "^[+-]" | grep -v "^[+-][+-][+-]" | grep -v "^[+-]> \*\*Fetched\*\*:" || true)
            if [[ -n "$diff_lines" ]]; then
                echo "  - $file: has non-timestamp changes"
                has_non_timestamp_changes=1
                break
            else
                echo "  - $file: only timestamp changes"
            fi
        fi
    fi
done < <(git diff --name-only)

if [[ $has_non_timestamp_changes -eq 1 ]]; then
    echo "There are non-timestamp changes, exiting"
    exit 0
fi

# At this point, we only have timestamp changes
echo ""
echo "=== All changes are timestamp/metadata updates! ==="
echo "📝 Auto-committing timestamp updates..."

# Stage all the timestamp changes
git add docs/*.md docs/docs_manifest.json 2>/dev/null || true

# Create commit message with date
commit_date=$(date +"%Y-%m-%d %H:%M")
git commit -m "Update SDK docs timestamps - $commit_date

Auto-generated commit: Documentation fetch timestamps updated" >/dev/null 2>&1

if [[ $? -eq 0 ]]; then
    echo "✅ Commit created successfully"

    # Push to origin
    echo "📤 Pushing timestamp updates to origin..."
    if git push origin HEAD >/dev/null 2>&1; then
        echo "✅ Timestamp updates pushed successfully"
    else
        echo "⚠️  Could not push timestamp updates (may need authentication)"
    fi
else
    echo "⚠️  Failed to create commit"
fi