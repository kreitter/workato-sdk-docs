#!/bin/bash
set -euo pipefail

# Workato SDK Documentation Mirror - Uninstaller
# Removes all components of the workato-sdk-docs installation

echo "Workato SDK Documentation Mirror - Uninstaller"
echo "=============================================="
echo ""

echo "This will remove:"
echo "  • The /workato-sdk command from ~/.claude/commands/workato-sdk.md"
echo "  • All workato-sdk-docs hooks from ~/.claude/settings.json"
echo "  • Installation directory ~/.workato-sdk-docs"
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Remove command file
if [[ -f ~/.claude/commands/workato-sdk.md ]]; then
    rm -f ~/.claude/commands/workato-sdk.md
    echo "✓ Removed /workato-sdk command"
fi

# Remove hooks from settings.json
if [[ -f ~/.claude/settings.json ]]; then
    cp ~/.claude/settings.json ~/.claude/settings.json.backup
    
    # Remove ALL hooks containing workato-sdk-docs
    jq '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.hooks[0].command | contains("workato-sdk-docs") | not)]' ~/.claude/settings.json > ~/.claude/settings.json.tmp
    
    # Clean up empty structures
    jq 'if .hooks.PreToolUse == [] then .hooks |= if . == {PreToolUse: []} then {} else del(.PreToolUse) end else . end | if .hooks == {} then del(.hooks) else . end' ~/.claude/settings.json.tmp > ~/.claude/settings.json.tmp2
    
    mv ~/.claude/settings.json.tmp2 ~/.claude/settings.json
    rm -f ~/.claude/settings.json.tmp
    echo "✓ Removed hooks (backup: ~/.claude/settings.json.backup)"
fi

# Remove installation directory
if [[ -d "$HOME/.workato-sdk-docs" ]]; then
    # Check if it has uncommitted changes
    if [[ -d "$HOME/.workato-sdk-docs/.git" ]]; then
        cd "$HOME/.workato-sdk-docs"
        
        if [[ -z "$(git status --porcelain 2>/dev/null)" ]]; then
            cd - >/dev/null
            rm -rf "$HOME/.workato-sdk-docs"
            echo "✓ Removed ~/.workato-sdk-docs (clean git repo)"
        else
            cd - >/dev/null
            echo "⚠️  Preserved ~/.workato-sdk-docs (has uncommitted changes)"
            echo "  To force removal: rm -rf ~/.workato-sdk-docs"
        fi
    else
        rm -rf "$HOME/.workato-sdk-docs"
        echo "✓ Removed ~/.workato-sdk-docs"
    fi
fi

echo ""
echo "✅ Uninstall complete!"
echo ""
echo "To reinstall:"
echo "curl -fsSL https://raw.githubusercontent.com/kreitter/workato-sdk-docs/main/install.sh | bash"