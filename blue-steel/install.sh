#!/usr/bin/env bash
#
# Blue Steel — a theme + status bar for Claude Code. One-command installer.
#   https://y3klab.com/blue-steel/
#
# Transparent by design: announces every path it touches, backs up your
# settings.json before changing it, and touches nothing else. To undo, see
# "Uninstall" on the page above — or run this with --uninstall
# (curl … | bash -s -- --uninstall): it removes exactly what install added,
# the two files and the three settings keys.
#
# The branded header is TTY-gated: piped or NO_COLOR output stays plain.
set -euo pipefail

base="${BLUE_STEEL_BASE:-https://y3klab.com/blue-steel}"
claude="$HOME/.claude"
settings="$claude/settings.json"

say() { printf '%s\n' "$*"; }

# ── The header echoes the status bar it installs: the name swept along the
# magenta→cyan ramp, framed in gradient-tipped brackets. Colour only on a TTY.
if [ -t 1 ] && [ "${TERM:-dumb}" != dumb ] && [ -z "${NO_COLOR:-}" ]; then
  ESC=$'\033'; RST="${ESC}[0m"
  DIM="${ESC}[38;5;245m"; OK="${ESC}[38;5;42m"; WRN="${ESC}[38;5;220m"
  ACC="${ESC}[38;5;39m"
  header() {
    local s="Blue Steel" ramp=(201 171 135 99 75 45 51) n=10 out="" i idx
    for (( i = 0; i < n; i++ )); do
      idx=$(( i * 6 / (n - 1) ))
      out+="${ESC}[1m${ESC}[38;5;${ramp[idx]}m${s:i:1}"
    done
    printf '%s %s%s %s %s\n' \
      "${ESC}[1m${ESC}[38;5;201m[${RST}" "$out" "$RST" \
      "${ESC}[1m${ESC}[38;5;51m]${RST}" "${DIM}$1${RST}"
  }
else
  RST=""; DIM=""; OK=""; WRN=""; ACC=""
  header() { printf '[ Blue Steel ] %s\n' "$1"; }
fi

# ── The sign-off banner: BLUE over STEEL, swept top-to-bottom through the same
# ramp, revealed row by row on a TTY (plain rows when piped). Install-end only.
banner() {
  local rows=(
'██████╗ ██╗     ██╗   ██╗███████╗'
'██╔══██╗██║     ██║   ██║██╔════╝'
'██████╔╝██║     ██║   ██║█████╗  '
'██╔══██╗██║     ██║   ██║██╔══╝  '
'██████╔╝███████╗╚██████╔╝███████╗'
'╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝'
'███████╗████████╗███████╗███████╗██╗     '
'██╔════╝╚══██╔══╝██╔════╝██╔════╝██║     '
'███████╗   ██║   █████╗  █████╗  ██║     '
'╚════██║   ██║   ██╔══╝  ██╔══╝  ██║     '
'███████║   ██║   ███████╗███████╗███████╗'
'╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝'
  )
  local ramp=(201 171 135 99 75 45 51) i idx
  for (( i = 0; i < ${#rows[@]}; i++ )); do
    if [ -n "$RST" ]; then
      idx=$(( i * 6 / (${#rows[@]} - 1) ))
      printf '%s%s%s\n' "${ESC}[38;5;${ramp[idx]}m" "${rows[i]}" "$RST"
      sleep 0.04
    else
      printf '%s\n' "${rows[i]}"
    fi
  done
}

# --uninstall: remove exactly what install added — the two files and the
# three settings keys.
if [ "${1:-}" = "--uninstall" ]; then
  header "uninstalling"
  say ""
  rm -f "$claude/statusline.sh" "$claude/themes/blue-steel.json" \
        "$settings.blue-steel-backup"
  say "  ${DIM}-${RST} $claude/statusline.sh"
  say "  ${DIM}-${RST} $claude/themes/blue-steel.json"
  if [ -f "$settings" ] && command -v jq >/dev/null 2>&1; then
    tmp=$(mktemp)
    jq 'del(.statusLine, .tui, .theme)' "$settings" > "$tmp"
    mv "$tmp" "$settings"
    say "  ${WRN}~${RST} $settings (statusLine/tui/theme keys removed)"
  elif [ -f "$settings" ]; then
    say "  ${WRN}!${RST} jq isn't available — remove the \"statusLine\", \"tui\", and"
    say "    \"theme\" keys from $settings yourself."
  fi
  say ""
  say "Done. Restart Claude Code — you're back to stock."
  exit 0
fi

header "a theme + status bar for Claude Code"
say ""

mkdir -p "$claude/themes"

curl -fsSL "$base/statusline.sh" -o "$claude/statusline.sh"
chmod +x "$claude/statusline.sh"
say "  ${OK}+${RST} $claude/statusline.sh"

curl -fsSL "$base/blue-steel.json" -o "$claude/themes/blue-steel.json"
say "  ${OK}+${RST} $claude/themes/blue-steel.json"

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
  say "  ${OK}+${RST} $settings (created)"
elif command -v jq >/dev/null 2>&1; then
  cp "$settings" "$settings.blue-steel-backup"
  tmp=$(mktemp)
  jq '. + {
        statusLine: { type: "command", command: "~/.claude/statusline.sh" },
        tui: "fullscreen",
        theme: "custom:blue-steel"
      }' "$settings" > "$tmp"
  mv "$tmp" "$settings"
  say "  ${WRN}~${RST} $settings (backup: $settings.blue-steel-backup)"
else
  say ""
  say "  ${WRN}!${RST} $settings already exists, and jq isn't available to merge it safely."
  say "    Add these keys to it yourself:"
  say ""
  say '      "statusLine": { "type": "command", "command": "~/.claude/statusline.sh" },'
  say '      "tui": "fullscreen",'
  say '      "theme": "custom:blue-steel"'
fi

say ""
banner
say ""
# The caption: A3K's tagline idiom — accent brackets, dim letter-spaced caps.
say "${ACC}[ ${RST}${DIM}S U C C E S S F U L L Y   I N S T A L L E D${RST} ${ACC}]${RST}"
say ""
# Instant proof: render the just-installed bar itself with a sample session
# (colour only when the installer itself is colouring).
sample='{"workspace":{"current_dir":"/tmp/your-project"},"cost":{"total_duration_ms":15600000},"context_window":{"used_percentage":42},"rate_limits":{"five_hour":{"used_percentage":85},"seven_day":{"used_percentage":60}},"model":{"display_name":"Fable 5"}}'
if [ -n "$RST" ]; then
  preview=$(printf '%s' "$sample" | bash "$claude/statusline.sh" 2>/dev/null) || preview=""
else
  preview=$(printf '%s' "$sample" | NO_COLOR=1 bash "$claude/statusline.sh" 2>/dev/null) || preview=""
fi
if [ -n "$preview" ]; then
  say "${DIM}your bar:${RST}"
  say "$preview"
  say ""
fi
command -v jq >/dev/null 2>&1 || \
  say "note: the status-bar gauges need jq (built into macOS 15+; otherwise: brew install jq)"
say "Done. Restart Claude Code to power it on."
