#!/usr/bin/env bash
#
# Blue Steel — a theme + status bar for Claude Code. One-command installer.
#   https://y3klab.com/blue-steel/
#
# Transparent by design: announces every path it touches, backs up your
# settings.json before changing it, and touches nothing else. To undo, see
# "Changed your mind?" on the page above — two files, three settings keys.
set -euo pipefail

base="${BLUE_STEEL_BASE:-https://y3klab.com/blue-steel}"
claude="$HOME/.claude"
settings="$claude/settings.json"

say() { printf '%s\n' "$*"; }

# --uninstall: remove exactly what install added — the two files and the
# three settings keys. (curl … | bash -s -- --uninstall)
if [ "${1:-}" = "--uninstall" ]; then
  say "Blue Steel — uninstalling"
  say ""
  rm -f "$claude/statusline.sh" "$claude/themes/blue-steel.json" \
        "$settings.blue-steel-backup"
  say "  - $claude/statusline.sh"
  say "  - $claude/themes/blue-steel.json"
  if [ -f "$settings" ] && command -v jq >/dev/null 2>&1; then
    tmp=$(mktemp)
    jq 'del(.statusLine, .tui, .theme)' "$settings" > "$tmp"
    mv "$tmp" "$settings"
    say "  ~ $settings (statusLine/tui/theme keys removed)"
  elif [ -f "$settings" ]; then
    say "  ! jq isn't available — remove the \"statusLine\", \"tui\", and"
    say "    \"theme\" keys from $settings yourself."
  fi
  say ""
  say "Done. Restart Claude Code — you're back to stock."
  exit 0
fi

say "Blue Steel — a theme + status bar for Claude Code"
say ""

mkdir -p "$claude/themes"

curl -fsSL "$base/statusline.sh" -o "$claude/statusline.sh"
chmod +x "$claude/statusline.sh"
say "  + $claude/statusline.sh"

curl -fsSL "$base/blue-steel.json" -o "$claude/themes/blue-steel.json"
say "  + $claude/themes/blue-steel.json"

if [ ! -f "$settings" ]; then
  cat > "$settings" <<'JSON'
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  },
  "tui": "fullscreen",
  "theme": "custom:blue-steel"
}
JSON
  say "  + $settings (created)"
elif command -v jq >/dev/null 2>&1; then
  cp "$settings" "$settings.blue-steel-backup"
  tmp=$(mktemp)
  jq '. + {
        statusLine: { type: "command", command: "~/.claude/statusline.sh" },
        tui: "fullscreen",
        theme: "custom:blue-steel"
      }' "$settings" > "$tmp"
  mv "$tmp" "$settings"
  say "  ~ $settings (backup: $settings.blue-steel-backup)"
else
  say ""
  say "  ! $settings already exists, and jq isn't available to merge it safely."
  say "    Add these keys to it yourself:"
  say ""
  say '      "statusLine": { "type": "command", "command": "~/.claude/statusline.sh" },'
  say '      "tui": "fullscreen",'
  say '      "theme": "custom:blue-steel"'
fi

say ""
command -v jq >/dev/null 2>&1 || \
  say "note: the status-bar gauges need jq (built into macOS 15+; otherwise: brew install jq)"
say "Done. Restart Claude Code to power it on."
