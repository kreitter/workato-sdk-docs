#!/bin/bash
set -euo pipefail

# Error handler function
error_exit() {
    echo "❌ Error: $1" >&2
    exit 1
}

# Trap errors and provide context
trap 'error_exit "Installation failed at line $LINENO. Please check the error messages above."' ERR

# Workato SDK Docs Installer v1.0
# This script installs workato-sdk-docs to ~/.workato-sdk-docs

echo "Workato SDK Docs Installer v1.0"
echo "================================"

# Fixed installation location
INSTALL_DIR="$HOME/.workato-sdk-docs"

# Branch to use for installation
INSTALL_BRANCH="main"

# Function to detect repository URL
detect_repo_url() {
    # 1. Check for environment variable override
    if [[ -n "${WORKATO_SDK_REPO_URL:-}" ]]; then
        echo "$WORKATO_SDK_REPO_URL"
        return 0
    fi
    
    # 2. Try to detect from current git repository (if running from cloned repo)
    if [[ -d ".git" ]] && command -v git &> /dev/null; then
        local detected_url=$(git remote get-url origin 2>/dev/null || true)
        if [[ -n "$detected_url" ]] && [[ "$detected_url" == *"workato-sdk-docs"* ]]; then
            # Convert SSH URLs to HTTPS for consistency
            if [[ "$detected_url" == git@github.com:* ]]; then
                detected_url="https://github.com/${detected_url#git@github.com:}"
                detected_url="${detected_url%.git}.git"  # Ensure .git suffix
            fi
            echo "$detected_url"
            return 0
        fi
    fi
    
    # 3. Fall back to default repository
    echo "https://github.com/kreitter/workato-sdk-docs.git"
}

# Detect or use configured repository URL
REPO_URL=$(detect_repo_url)
echo "Using repository: $REPO_URL"

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

# Check for Claude Code installation
echo "Checking for Claude Code..."
if [[ ! -d "$HOME/.claude" ]]; then
    echo ""
    echo "⚠️  Warning: Claude Code directory not found (~/.claude)"
    echo ""
    echo "This tool integrates with Claude Code to provide the /workato-sdk command."
    echo "Without Claude Code, the documentation will be downloaded but not accessible"
    echo "via the slash command."
    echo ""
    echo "To install Claude Code, visit: https://claude.ai/code"
    echo ""
    read -p "Continue installation anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled. Please install Claude Code first."
        exit 0
    fi
    echo "Continuing installation without Claude Code integration..."
    CLAUDE_CODE_FOUND=false
else
    echo "✓ Claude Code found at ~/.claude"
    CLAUDE_CODE_FOUND=true
fi

# Function to safely update git repository
safe_git_update() {
    local repo_dir="$1"
    cd "$repo_dir"
    
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    local target_branch="$INSTALL_BRANCH"
    
    # Check for local changes
    if [[ -n "$(git status --porcelain)" ]]; then
        echo "⚠️  Local changes detected in ~/.workato-sdk-docs"
        echo ""
        echo "Your local changes:"
        git status --short
        echo ""
        echo "Options:"
        echo "  1. Stash changes and update (recommended)"
        echo "  2. Keep local changes and skip update"
        echo "  3. Discard local changes and update"
        echo ""
        read -p "Choose option (1-3): " -n 1 -r choice
        echo
        
        case $choice in
            1) 
                echo "  Stashing local changes..."
                git stash push -m "Auto-stash before workato-sdk-docs update $(date +%Y%m%d-%H%M%S)"
                
                # Fetch and update
                git fetch origin "$target_branch"
                git checkout -B "$target_branch" "origin/$target_branch"
                git pull origin "$target_branch"
                
                # Try to restore stashed changes
                echo "  Restoring stashed changes..."
                if git stash pop; then
                    echo "  ✓ Successfully restored your local changes"
                else
                    echo "  ⚠️  Stash conflicts detected - please review manually"
                    echo "  Your changes are saved in: git stash list"
                fi
                ;;
            2) 
                echo "  Skipping update - keeping local changes"
                echo "  ⚠️  You may need to manually merge updates later"
                return 0
                ;;
            3) 
                echo "  Discarding local changes..."
                git reset --hard HEAD
                git clean -fd
                
                # Now update normally
                git fetch origin "$target_branch"
                git checkout -B "$target_branch" "origin/$target_branch"
                git pull origin "$target_branch"
                echo "  ✓ Updated to latest version (local changes discarded)"
                ;;
            *) 
                echo "  ❌ Invalid choice - aborting installation"
                echo "  Your local changes are preserved"
                exit 1
                ;;
        esac
    else
        # No local changes, proceed with normal update
        if [[ "$current_branch" != "$target_branch" ]]; then
            echo "  Switching from $current_branch to $target_branch branch..."
        else
            echo "  Updating $target_branch branch..."
        fi
        
        # Set git config for pull strategy if not set
        if ! git config pull.rebase >/dev/null 2>&1; then
            git config pull.rebase false
        fi
        
        # Try regular pull
        if git pull origin "$target_branch" 2>/dev/null; then
            echo "  ✓ Updated successfully"
            return 0
        fi
        
        # If pull failed, try to recover
        echo "  Standard update failed, attempting recovery..."
        
        # Fetch latest
        if ! git fetch origin "$target_branch" 2>/dev/null; then
            echo "  ⚠️  Could not fetch from GitHub (offline?)"
            echo "  Installation will continue with existing version"
            return 1
        fi
        
        # Abort any in-progress merge/rebase
        git merge --abort >/dev/null 2>&1 || true
        git rebase --abort >/dev/null 2>&1 || true
        
        # Reset to remote state
        git checkout -B "$target_branch" "origin/$target_branch"
        git reset --hard "origin/$target_branch"
        
        echo "  ✓ Updated successfully to clean state"
    fi
    
    return 0
}

# Main installation logic
echo ""

# Check if already installed
if [[ -d "$INSTALL_DIR" && -f "$INSTALL_DIR/docs/docs_manifest.json" ]]; then
    echo "✓ Found installation at ~/.workato-sdk-docs"
    echo "  Updating to latest version..."
    
    # Update it safely
    safe_git_update "$INSTALL_DIR" || {
        echo "❌ Error: Failed to update existing installation"
        echo "  Your installation at $INSTALL_DIR may be in an inconsistent state."
        echo "  Try running: cd $INSTALL_DIR && git status"
        exit 1
    }
    cd "$INSTALL_DIR" || {
        echo "❌ Error: Failed to change to installation directory $INSTALL_DIR"
        exit 1
    }
else
    # Fresh installation
    echo "Installing fresh to ~/.workato-sdk-docs..."
    
    if ! git clone -b "$INSTALL_BRANCH" "$REPO_URL" "$INSTALL_DIR" 2>/dev/null; then
        echo "❌ Error: Failed to clone repository from $REPO_URL"
        echo "  Please check:"
        echo "  1. Your internet connection"
        echo "  2. The repository URL is correct"
        echo "  3. You have access to the repository"
        exit 1
    fi
    cd "$INSTALL_DIR" || {
        echo "❌ Error: Failed to change to installation directory $INSTALL_DIR"
        echo "  Installation may be incomplete."
        exit 1
    }
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
    echo "  ❌ Error: Template file missing at $INSTALL_DIR/scripts/workato-sdk-helper.sh.template"
    echo "  This is required for the /workato-sdk command to work."
    echo "  Please ensure the repository was cloned correctly."
    exit 1
fi

# Create docs directory if it doesn't exist
mkdir -p "$INSTALL_DIR/docs"

# Always update command - only if Claude Code is installed
if [[ "$CLAUDE_CODE_FOUND" == "true" ]]; then
    echo "Setting up /workato-sdk command..."
    mkdir -p ~/.claude/commands || {
        echo "❌ Error: Failed to create ~/.claude/commands directory"
        echo "  Please check permissions for your home directory."
        exit 1
    }

# Create workato-sdk command
if ! cat > ~/.claude/commands/workato-sdk.md << 'EOF'
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
then
    echo "❌ Error: Failed to create /workato-sdk command file"
    echo "  Please check write permissions for ~/.claude/commands/"
    exit 1
fi

    echo "✓ Created /workato-sdk command"
else
    echo "⚠️  Skipping /workato-sdk command setup (Claude Code not installed)"
fi

# Always update hook - only if Claude Code is installed
if [[ "$CLAUDE_CODE_FOUND" == "true" ]]; then
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
else
    echo "⚠️  Skipping automatic updates setup (Claude Code not installed)"
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
if [[ "$CLAUDE_CODE_FOUND" == "true" ]]; then
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
else
    echo "✅ Workato SDK Docs downloaded successfully!"
    echo ""
    echo "📂 Location: ~/.workato-sdk-docs"
    echo ""
    echo "⚠️  Claude Code integration not available."
    echo "   To enable the /workato-sdk command:"
    echo "   1. Install Claude Code from https://claude.ai/code"
    echo "   2. Re-run this installer"
    echo ""
    echo "For now, you can access the documentation directly:"
    echo "  cd ~/.workato-sdk-docs/docs"
    echo "  ls *.md"
fi
echo ""

# List available topics if docs were fetched
if [[ -d "$INSTALL_DIR/docs" ]] && ls "$INSTALL_DIR/docs"/*.md >/dev/null 2>&1; then
    echo "Available SDK topics:"
    ls "$INSTALL_DIR/docs" | grep '\.md$' | sed 's/\.md$//' | sort | column -c 60
    echo ""
fi

if [[ "$CLAUDE_CODE_FOUND" == "true" ]]; then
    echo "⚠️  Note: Restart Claude Code for auto-updates to take effect"
fi
