#!/usr/bin/env bash
#
# Claude Code statusLine — answers "which project is this session in?" with the
# project name swept in the A3K magenta→cyan gradient, framed in gradient-tipped
# brackets, plus session gauges: context-window %, the 5-hour and 7-day rate-limit
# % (Claude Max), session elapsed time, and the active model (e.g. "Opus 4.8"), in
# that order. The % gauges colour themselves green→amber→red as they fill (A3K §2
# status palette) so the colour IS the warning; each gauge shows only once its
# value exists (they're null/absent early).
#
# Parsing uses jq (the statusLine JSON repeats `used_percentage` under context /
# five_hour / seven_day, which sed can't disambiguate cleanly). Without jq it
# degrades to just the project name. Kept fast (one jq call) — Claude re-runs this
# on every render.
#
# Wired via Claude Code's settings.json ("statusLine" key), pointing at wherever
# this script lives:
#   "statusLine": { "type": "command", "command": "/path/to/statusline.sh" }

# The per-char gradient needs a UTF-8 locale so ${#s}/${s:i:1} count characters,
# not bytes (titles can carry ·, —, é). Guard a bare/odd locale.
[ -z "${LANG:-}" ] && [ -z "${LC_ALL:-}" ] && export LANG=en_US.UTF-8

input=$(cat)

# ── helpers ───────────────────────────────────────────────────────────────────
_dur() {  # milliseconds → compact human time (12s / 3m / 1h2m)
  local s=$(( ${1:-0} / 1000 ))
  if   (( s < 60 ));   then printf '%ds' "$s"
  elif (( s < 3600 )); then printf '%dm' "$(( s / 60 ))"
  else                      printf '%dh%dm' "$(( s / 3600 ))" "$(( (s % 3600) / 60 ))"; fi
}
_pctcol() {  # percent → A3K status colour (green <60 · amber <85 · red ≥85)
  local p=${1%%.*}
  if   (( p < 60 )); then printf '\033[38;5;42m'
  elif (( p < 85 )); then printf '\033[38;5;220m'
  else                    printf '\033[38;5;203m'; fi
}
_meter1() {  # percent → one eighths-block char (▁..█) — a 1-col "how full" cue
  local p=${1%%.*} blocks=(▁ ▂ ▃ ▄ ▅ ▆ ▇ █) i
  i=$(( p * 8 / 100 )); (( i > 7 )) && i=7; (( i < 0 )) && i=0
  printf '%s' "${blocks[i]}"
}

# ── parse the statusLine JSON (jq when available; else cwd-only via sed) ───────
cwd=""; dur_ms=""; ctx=""; rl5=""; rl7=""; model=""
if command -v jq >/dev/null 2>&1; then
  # Absent fields become the literal string "null", never "" — bash `read` with a
  # tab IFS collapses adjacent tabs, so an empty TSV field would shift every later
  # field left. The per-gauge `!= null` checks below skip the sentinel.
  IFS=$'\t' read -r cwd dur_ms ctx rl5 rl7 model < <(printf '%s' "$input" | jq -r \
    '[.workspace.current_dir // .cwd // "null", .cost.total_duration_ms // "null", .context_window.used_percentage // "null", .rate_limits.five_hour.used_percentage // "null", .rate_limits.seven_day.used_percentage // "null", .model.display_name // .model.id // "null"] | @tsv' 2>/dev/null)
  [ "$cwd" = null ] && cwd=""
  [ "$dur_ms" = null ] && dur_ms=""
else
  cwd=$(printf '%s' "$input" | sed -n 's/.*"current_dir"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
  [ -z "$cwd" ] && cwd=$(printf '%s' "$input" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi
[ -z "$cwd" ] && cwd="$PWD"

# ── project label: managed-project friendly title → git repo name → basename ──
label=""
case "$cwd/" in
  "$HOME/Projects/"*)
    rel="${cwd#"$HOME/Projects/"}"; section="${rel%%/*}"; rest="${rel#*/}"; name="${rest%%/*}"
    proot="$HOME/Projects/$section/$name"
    [ -f "$proot/.system/project.md" ] && \
      label=$(grep -m1 '^# ' "$proot/.system/project.md" 2>/dev/null | sed 's/^#[[:space:]]*//')
    [ -z "$label" ] && label="$name"
    ;;
  *)
    top=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null)
    if [ -n "$top" ]; then label="${top##*/}"; else label="${cwd##*/}"; fi
    ;;
esac

# ── gauges: " · <dur> · ctx N% · 5h N%", each present-only. $1=1 colour, 0 plain ─
gauges() {  # $1=1 colour, 0 plain. A uniform ` | ` seam (grey 238) joins the gauges
            # to each other — but not to the bracketed name: the brackets already set
            # identity apart, so a divider there would do that job twice.
            # Gauge values sit at 243 so they out-rank the separators. The model is
            # shown bare (its name self-labels); duration wears a "session" label.
            # Colour stays semantic: only the % gauges get status hues.
  local colour=$1 sep dim="" rst="" v="" segs=() i out=""
  if (( colour )); then
    sep=$' \033[38;5;238m|\033[0m '
    dim=$'\033[38;5;245m'; rst=$'\033[0m'; v=$'\033[38;5;243m'
  else
    sep=" | "
  fi
  if [ -n "$ctx" ] && [ "$ctx" != null ]; then
    if (( colour )); then segs+=( "${dim}context ${rst}$(_pctcol "$ctx")$(_meter1 "$ctx")${ctx%%.*}%${rst}" )
    else                  segs+=( "context ${ctx%%.*}%" ); fi
  fi
  if [ -n "$rl5" ] && [ "$rl5" != null ]; then
    if (( colour )); then segs+=( "${dim}5h limit ${rst}$(_pctcol "$rl5")${rl5%%.*}%${rst}" )
    else                  segs+=( "5h limit ${rl5%%.*}%" ); fi
  fi
  if [ -n "$rl7" ] && [ "$rl7" != null ]; then
    if (( colour )); then segs+=( "${dim}7d limit ${rst}$(_pctcol "$rl7")${rl7%%.*}%${rst}" )
    else                  segs+=( "7d limit ${rl7%%.*}%" ); fi
  fi
  [ -n "$dur_ms" ] && [ "$dur_ms" != null ] && segs+=( "${dim}session ${rst}${v}$(_dur "$dur_ms")${rst}" )
  [ -n "$model" ] && [ "$model" != null ] && segs+=( "${v}${model}${rst}" )
  (( ${#segs[@]} == 0 )) && return
  out="  ${segs[0]}"
  for (( i = 1; i < ${#segs[@]}; i++ )); do out+="${sep}${segs[i]}"; done
  printf '%s' "$out"
}

# ── width guard: trim the lowest-signal gauges if the line would overflow the
# terminal ($COLUMNS, exported by Claude). Drop duration first, then the model, then
# the 7-day limit (slower-moving than the 5-hour), then the 5-hour; the bracketed
# name + context are the irreducible core. (Measured on the plain text — ANSI codes
# are zero-width, so plain length == rendered width.)
cols=${COLUMNS:-9999}; [[ $cols =~ ^[0-9]+$ ]] || cols=9999
guard_line="[ $label ]$(gauges 0)"
if (( ${#guard_line} > cols )); then dur_ms=""; guard_line="[ $label ]$(gauges 0)"; fi
if (( ${#guard_line} > cols )); then model="";  guard_line="[ $label ]$(gauges 0)"; fi
if (( ${#guard_line} > cols )); then rl7="";    guard_line="[ $label ]$(gauges 0)"; fi
(( ${#guard_line} > cols )) && rl5=""

# ── plain degradation (no colour) ─────────────────────────────────────────────
if [ -n "${NO_COLOR:-}" ] || [ "${TERM:-dumb}" = "dumb" ]; then
  printf '[ %s ]%s' "$label" "$(gauges 0)"
  exit 0
fi

# ── A3K livery. The project NAME sweeps the canonical Phos4 magenta→cyan ramp per
# character (idx = i*6/(N-1) — the dashboard-wordmark rule), bold, anchored magenta
# on char 0 and bright-cyan on the last; framed by padded gradient-tipped brackets
# ([ magenta … cyan ]) that cap the sweep. Gauges follow, dim with status-coloured %.
ESC=$'\033'; RST="${ESC}[0m"
RAMP=(201 171 135 99 75 45 51); PN=7
n=${#label}; (( n < 2 )) && n=2
name=""
for (( i = 0; i < ${#label}; i++ )); do
  idx=$(( i * (PN - 1) / (n - 1) )); (( idx >= PN )) && idx=$(( PN - 1 ))
  name+="${ESC}[1m${ESC}[38;5;${RAMP[idx]}m${label:i:1}"
done
lb="${ESC}[1m${ESC}[38;5;201m[${RST}"
rb="${ESC}[1m${ESC}[38;5;51m]${RST}"
printf '%s %s%s %s%s' "$lb" "$name" "$RST" "$rb" "$(gauges 1)"
