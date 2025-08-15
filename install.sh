#!/bin/bash
set -euo pipefail

# Workato SDK Docs Installer v1.0
# This script installs workato-sdk-docs to ~/.workato-sdk-docs

echo "Workato SDK Docs Installer v1.0"
echo "================================"

# Fixed installation location
INSTALL_DIR="$HOME/.workato-sdk-docs"

# Branch to use for installation
INSTALL_BRANCH="main"

# Repository URL (change this to your actual repository)
REPO_URL="https://github.com/kreitter/workato-sdk-docs.git"

# Detect OS type
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
    echo "✓ Detected macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    echo "✓ Detected Linux"
else
    echo "❌ Error: Unsupported OS type: $OSTYPE"
    echo "This installer supports macOS and Linux only"
    exit 1
fi

# Check dependencies
echo "Checking dependencies..."
for cmd in git jq curl python3; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "❌ Error: $cmd is required but not installed"
        echo "Please install $cmd and try again"
        exit 1
    fi
done

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import requests, bs4, html2text" 2>/dev/null || {
    echo "⚠️  Python dependencies missing. Installing..."
    pip3 install --user requests beautifulsoup4 html2text lxml || {
        echo "❌ Error: Failed to install Python dependencies"
        echo "Please install manually: pip3 install requests beautifulsoup4 html2text lxml"
        exit 1
    }
}

echo "✓ All dependencies satisfied"

# Function to safely update git repository
safe_git_update() {
    local repo_dir="$1"
    cd "$repo_dir"
    
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    local target_branch="$INSTALL_BRANCH"
    
    if [[ "$current_branch" != "$target_branch" ]]; then
        echo "  Switching from $current_branch to $target_branch branch..."
    else
        echo "  Updating $target_branch branch..."
    fi
    
    # Set git config for pull strategy if not set
    if ! git config pull.rebase >/dev/null 2>&1; then
        git config pull.rebase false
    fi
    
    echo "Updating to latest version..."
    
    # Try regular pull first
    if git pull --quiet origin "$target_branch" 2>/dev/null; then
        return 0
    fi
    
    # If pull failed, try more aggressive approach
    echo "  Standard update failed, trying harder..."
    
    # Fetch latest
    if ! git fetch origin "$target_branch" 2>/dev/null; then
        echo "  ⚠️  Could not fetch from GitHub (offline?)"
        return 1
    fi
    
    # Force clean state
    echo "  Updating to clean state..."
    
    # Abort any in-progress merge/rebase
    git merge --abort >/dev/null 2>&1 || true
    git rebase --abort >/dev/null 2>&1 || true
    
    # Clear any stale index
    git reset >/dev/null 2>&1 || true
    
    # Force checkout target branch
    git checkout -B "$target_branch" "origin/$target_branch" >/dev/null 2>&1
    
    # Reset to clean state
    git reset --hard "origin/$target_branch" >/dev/null 2>&1
    
    # Clean any untracked files
    git clean -fd >/dev/null 2>&1 || true
    
    echo "  ✓ Updated successfully to clean state"
    
    return 0
}

# Main installation logic
echo ""

# Check if already installed
if [[ -d "$INSTALL_DIR" && -f "$INSTALL_DIR/docs/docs_manifest.json" ]]; then
    echo "✓ Found installation at ~/.workato-sdk-docs"
    echo "  Updating to latest version..."
    
    # Update it safely
    safe_git_update "$INSTALL_DIR"
    cd "$INSTALL_DIR"
else
    # Fresh installation
    echo "Installing fresh to ~/.workato-sdk-docs..."
    
    git clone -b "$INSTALL_BRANCH" "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Set up the script-based system
echo ""
echo "Setting up Workato SDK Docs v1.0..."

# Copy helper script from template
echo "Installing helper script..."
if [[ -f "$INSTALL_DIR/scripts/workato-sdk-helper.sh.template" ]]; then
    cp "$INSTALL_DIR/scripts/workato-sdk-helper.sh.template" "$INSTALL_DIR/workato-sdk-helper.sh"
    chmod +x "$INSTALL_DIR/workato-sdk-helper.sh"
    echo "✓ Helper script installed"
else
    echo "  ❌ Template file missing"
    exit 1
fi

# Create docs directory if it doesn't exist
mkdir -p "$INSTALL_DIR/docs"

# Always update command
echo "Setting up /workato-sdk command..."
mkdir -p ~/.claude/commands

# Create workato-sdk command
cat > ~/.claude/commands/workato-sdk.md << 'EOF'
Execute the Workato SDK Docs helper script at ~/.workato-sdk-docs/workato-sdk-helper.sh

Usage:
- /workato-sdk - List all available SDK documentation topics
- /workato-sdk <topic> - Read specific SDK documentation
- /workato-sdk -t - Check sync status without reading a doc
- /workato-sdk -t <topic> - Check freshness then read documentation
- /workato-sdk whats new - Show recent documentation changes

Examples:
/workato-sdk sdk-reference
/workato-sdk platform-quickstart
/workato-sdk -t

Every request checks for the latest documentation from GitHub.
The helper script handles all functionality including auto-updates.

Execute: ~/.workato-sdk-docs/workato-sdk-helper.sh "$ARGUMENTS"
EOF

echo "✓ Created /workato-sdk command"

# Always update hook
echo "Setting up automatic updates..."

# Simple hook that just calls the helper script
HOOK_COMMAND="~/.workato-sdk-docs/workato-sdk-helper.sh hook-check"

if [ -f ~/.claude/settings.json ]; then
    # Update existing settings.json
    echo "  Updating Claude settings..."
    
    # First remove any existing workato-sdk-docs hooks
    jq '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.hooks[0].command | contains("workato-sdk-docs") | not)]' ~/.claude/settings.json > ~/.claude/settings.json.tmp
    
    # Then add our new hook
    jq --arg cmd "$HOOK_COMMAND" '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[]] + [{"matcher": "Read", "hooks": [{"type": "command", "command": $cmd}]}]' ~/.claude/settings.json.tmp > ~/.claude/settings.json
    rm -f ~/.claude/settings.json.tmp
    echo "✓ Updated Claude settings"
else
    # Create new settings.json
    echo "  Creating Claude settings..."
    jq -n --arg cmd "$HOOK_COMMAND" '{
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Read",
                    "hooks": [
                        {
                            "type": "command",
                            "command": $cmd
                        }
                    ]
                }
            ]
        }
    }' > ~/.claude/settings.json
    echo "✓ Created Claude settings"
fi

# Fetch initial documentation
echo ""
echo "Fetching Workato SDK documentation..."
cd "$INSTALL_DIR"
python3 scripts/fetch_workato_docs.py || {
    echo "⚠️  Initial fetch failed. You can retry later with:"
    echo "    cd ~/.workato-sdk-docs && python3 scripts/fetch_workato_docs.py"
}

# Success message
echo ""
echo "✅ Workato SDK Docs v1.0 installed successfully!"
echo ""
echo "📚 Command: /workato-sdk (user)"
echo "📂 Location: ~/.workato-sdk-docs"
echo ""
echo "Usage examples:"
echo "  /workato-sdk              # List all SDK topics"
echo "  /workato-sdk sdk-reference  # Read SDK reference"
echo "  /workato-sdk -t          # Check sync status"
echo "  /workato-sdk what's new  # See recent updates"
echo ""
echo "🔄 Auto-updates: Enabled - syncs automatically when GitHub has newer content"
echo ""

# List available topics if docs were fetched
if [[ -d "$INSTALL_DIR/docs" ]] && ls "$INSTALL_DIR/docs"/*.md >/dev/null 2>&1; then
    echo "Available SDK topics:"
    ls "$INSTALL_DIR/docs" | grep '\.md$' | sed 's/\.md$//' | sort | column -c 60
    echo ""
fi

echo "⚠️  Note: Restart Claude Code for auto-updates to take effect"