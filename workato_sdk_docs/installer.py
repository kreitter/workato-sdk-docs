from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

HOME = Path.home()
INSTALL_DIR = HOME / ".workato-sdk-docs"
CLAUDE_DIR = HOME / ".claude"
COMMANDS_DIR = CLAUDE_DIR / "commands"
SETTINGS_JSON = CLAUDE_DIR / "settings.json"

DEFAULT_REPO_URL = os.environ.get(
    "WORKATO_SDK_REPO_URL",
    "https://github.com/kreitter/workato-sdk-docs.git",
)
DEFAULT_BRANCH = os.environ.get("WORKATO_SDK_REPO_BRANCH", "main")
HOOK_COMMAND = str(INSTALL_DIR / "workato-sdk-helper.sh") + " hook-check"


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=check)


def ensure_git_available() -> None:
    if shutil.which("git") is None:
        raise SystemExit("git is required. Please install git and re-run.")


def clone_or_update(repo_url: str, branch: str) -> None:
    if not INSTALL_DIR.exists():
        print(f"Cloning {repo_url} to {INSTALL_DIR}...")
        run(["git", "clone", "-b", branch, repo_url, str(INSTALL_DIR)])
    else:
        print("Updating existing installation...")
        run(["git", "fetch", "origin", branch], cwd=INSTALL_DIR)
        run(["git", "checkout", branch], cwd=INSTALL_DIR)
        # Be lenient if pull fails (e.g., offline); user still gets local copy
        try:
            run(["git", "pull", "origin", branch], cwd=INSTALL_DIR)
        except subprocess.CalledProcessError:
            print("⚠️  Could not pull latest changes; using current local copy.")


def write_helper_script() -> None:
    template_path = INSTALL_DIR / "scripts" / "workato-sdk-helper.sh.template"
    if not template_path.exists():
        raise SystemExit(f"Missing helper template at {template_path}")
    target = INSTALL_DIR / "workato-sdk-helper.sh"
    target.write_text(template_path.read_text())
    target.chmod(0o755)
    print("✓ Helper script installed")


def write_claude_command() -> None:
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    cmd_path = COMMANDS_DIR / "workato-sdk.md"
    content = (
        "Execute the Workato SDK Docs helper script at\n"
        "~/.workato-sdk-docs/workato-sdk-helper.sh\n\n"
        "Usage:\n"
        "- /workato-sdk - List all available SDK documentation topics\n"
        "- /workato-sdk <topic> - Read specific SDK documentation\n"
        "- /workato-sdk -t - Check sync status without reading a doc\n"
        "- /workato-sdk -t <topic> - Check freshness then read documentation\n"
        "- /workato-sdk whats new - Show recent documentation changes\n\n"
        "Examples:\n"
        "/workato-sdk sdk-reference\n"
        "/workato-sdk platform-quickstart\n"
        "/workato-sdk -t\n\n"
        "Every request checks for the latest documentation from GitHub.\n"
        "The helper script handles all functionality including auto-updates.\n\n"
        'Execute: ~/.workato-sdk-docs/workato-sdk-helper.sh "$ARGUMENTS"\n'
    )
    cmd_path.write_text(content)
    print("✓ Created /workato-sdk command for Claude Code")


def _dedupe_hooks(pre_hooks: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    deduped: list[Dict[str, Any]] = []
    for entry in pre_hooks:
        hooks = entry.get("hooks") or []
        _hooks = []
        for h in hooks:
            cmd = h.get("command", "")
            if isinstance(cmd, str) and "workato-sdk-docs" in cmd:
                continue
            _hooks.append(h)
        entry = {**entry, "hooks": _hooks}
        deduped.append(entry)
    return deduped


def update_claude_settings() -> None:
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    base: Dict[str, Any] = {"hooks": {"PreToolUse": []}}
    if SETTINGS_JSON.exists():
        try:
            base = json.loads(SETTINGS_JSON.read_text() or "{}")
        except Exception:
            pass

    hooks = base.setdefault("hooks", {})
    pre = hooks.setdefault("PreToolUse", [])

    # Remove any existing workato-sdk-docs command hooks
    pre = _dedupe_hooks(pre)

    # Add our hook
    pre.append(
        {
            "matcher": "Read",
            "hooks": [{"type": "command", "command": HOOK_COMMAND}],
        }
    )

    base["hooks"]["PreToolUse"] = pre
    SETTINGS_JSON.write_text(json.dumps(base, indent=2))
    print("✓ Updated Claude settings (PreToolUse hook added)")


def initial_fetch() -> None:
    print("Fetching Workato SDK documentation (initial run)...")
    try:
        script_path = INSTALL_DIR / "scripts" / "fetch_workato_docs.py"
        run([sys.executable, str(script_path)], cwd=INSTALL_DIR)
        print("✓ Initial fetch complete")
    except subprocess.CalledProcessError:
        print(
            "⚠️  Initial fetch failed. You can retry later with:\n"
            "    uv run python scripts/fetch_workato_docs.py"
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="workato-sdk-install",
        description="Install Workato SDK Docs locally and integrate with Claude Code",
    )
    p.add_argument("--repo", default=DEFAULT_REPO_URL, help="Repository URL to clone/update")
    p.add_argument("--branch", default=DEFAULT_BRANCH, help="Branch to use (default: main)")
    p.add_argument("--no-claude", action="store_true", help="Skip Claude integration")
    p.add_argument("--no-hook", action="store_true", help="Create command but skip PreToolUse hook")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    ensure_git_available()

    clone_or_update(args.repo, args.branch)
    write_helper_script()

    if not args.no_claude and CLAUDE_DIR.exists():
        write_claude_command()
        if not args.no_hook:
            update_claude_settings()
    else:
        print("⚠️  ~/.claude not found or Claude integration disabled; skipping command creation.")
        print("   After installing Claude Code, re-run: workato-sdk-install")

    initial_fetch()

    if CLAUDE_DIR.exists() and not args.no_claude:
        print("\n✅ Install complete. Try the command in Claude Code: /workato-sdk")
    else:
        print("\n✅ Install complete. Docs are available under ~/.workato-sdk-docs/docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
