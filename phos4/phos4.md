# Phos4

The **Y3K Lab** terminal-UI engine — pure bash, zero dependencies, fluent in A3K.

Built for the year 3000

```
      Phos4 ═ reads **phos-for** ≈ **phosphor** — the coating that makes a CRT glow
      P₄ ═ white phosphorus — the molecule that glows on its own
      The family resemblance is the embedded numeral: **Y3K** carries a 3 — Phos4 answers with a 4.

```

The engine at work · a demo session · every colour below is theme data

```
❯ PHOS4_THEME=y3k PHOS4_ANIMATE=1 ./demo.sh

  ╔═════════════════════════════════╗
  ║ ╔═╗ ╦═╗ ╔═╗  ╦  ╔═╗ ╔═╗ ╔╦╗ ╔═╗ ║
  ║ ╠═╝ ╠╦╝ ║ ║  ║  ╠═  ║    ║  ╚═╗ ║
  ║ ╩   ╩╚═ ╚═╝ ╚╝  ╚═╝ ╚═╝  ╩  ╚═╝ ║
  ╚═════════════════════════════════╝
  ✓ phos4_step_ok — the good news
  ⚠ phos4_step_warn — the heads-up
  ✗ phos4_step_err — the bad news
  · phos4_step_info — the aside

  ─────────────────────────────────────────────────────
  phos4_choose — pick one
  ─────────────────────────────────────────────────────

  ❯  1   banner                the wordmark, boxed and swept
     2   picker                this very menu
     3   panel                 the completion box

  ↑/↓ navigate · enter to select · type number to jump · esc to cancel
```

Hand-made in HTML/CSS from the engine's golden masters — the real thing is bash writing ANSI. The wordmark is the **y3k** theme's default; **▶** replays its power-on, and **PS_MONO=1** re-renders the same markup from the grey band — a theme swap, live.

## What Phos4 is

**Phos4** is a pure-bash, themeable *terminal-UI engine* — gradient-swept wordmarks, arrow-key pickers, panels, spinners, progress — shipped as a single file any CLI script can `source`. No curses, no Python, no npm — bash 3.2 and ANSI escapes, nothing else.

It exists because the look outgrew its birthplace. **A3K** — the Y3K design language — took shape inside the Project System, entangled across three scripts; the installer even carried its own duplicate copies of the animations. Good enough to reuse, too tangled to travel. Phos4 is the extraction: the **engine** (mechanics) pulled clean of the **look** (data), so the machinery is shared once and the look is swappable per consumer.

The verbs stay disciplined: a surface wears A3K; Phos4 is *fluent* in it and renders it. An engine never *builds* the look — “built” stays reserved for the tagline, *Built for the year 3000*.

## Engine vs. theme

The architecture is one clean cleave, three roles. The **engine** owns the mechanics — how a gradient sweeps a ramp across characters, how a wordmark gets boxed in rails, how a picker repaints in place. A **theme** is *pure data* — colour indices, gradient stops, rail glyphs, literal wordmark rows — **no rendering code in a theme, ever**; the contract is locked. And the **consumer** — the script that sourced the file — owns choreography: what happens, in what order, is its business. How it looks is not.

The whole theme contract · six functions of pure data

| Theme function | Supplies |
|---|---|
| y3k_palette | the colour indices — accent, ok / warn / err, rails, highlight |
| y3k_ramp | the gradient stops — 201 171 135 99 75 45 51, magenta → cyan |
| y3k_anim_ramp | the longer 16-stop loop the power-on animation flows through |
| y3k_wm_width | the wordmark row width every row is padded to (31) |
| y3k_rail | the box rails — top, bottom, side; every glyph is theme data |
| y3k_wordmark | literal glyph-rows for each wordmark key |

That table *is* the theme side of the seam — swap the prefix and you’ve named a new theme; the engine dispatches through `PHOS4_THEME` and never knows the difference. The seam is proven, not promised: a second theme — a different brand with its own logo language, flat colour, single-line box — renders through the same engine with **zero engine changes**. The one gap it exposed (a hardcoded `║` side glyph) was closed by promoting that glyph to theme data; the pure-data contract held, no escape hatch.

Even greyscale is data: `PS_MONO=1` swaps the ramp for a mid-grey band and the engine renders on, colour-blind — that’s the toggle under the demo above.

## The primitives

The API is small, and all of it is namespaced: source one file, get every `phos4_*` call. Prompts answer the bash way — through environment variables and exit status, never parsed stdout — and `ESC` always means no.

| Call | Renders |
|---|---|
| phos4_render_banner | the rail-boxed, gradient-swept wordmark — with a sub-second power-on entrance when PHOS4_ANIMATE=1 |
| phos4_render_splash | rail-less splash art — install banners, mascots, shapes that aren’t a boxed wordmark |
| phos4_gradient_text | the theme ramp swept per-character across any string |
| phos4_choose · confirm · input | the arrow-key picker, the Yes/No toggle, the line prompt |
| phos4_step_ok · warn · err · info | the ✓ ⚠ ✗ · status lines |
| phos4_header · rule · panel | section chrome and the bordered completion box |
| phos4_spin · loadbar | a spinner (⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏) that wraps a command; the self-clearing fill bar |
| phos4_celebrate · celebrate_banner | the shimmer sign-off; giant block letters for the moment a surface finishes something |

## The correctness rules

Half of Phos4’s value is invisible: the accumulated rules that keep a pure-bash renderer from corrupting a terminal. They live as comments at their site in the engine — no external doc to consult — and every one of them was paid for.

- **Rule 1 — TTY-gate every visual** Off a terminal the style strings are empty, and the same `printf` emits plain text. Pipe it, log it, test it — the escapes simply aren’t there. The engine never animates into a pipe.

- **Rule 2 — Guard the locale** Box glyphs are multibyte. `${#s}` has to count characters, not bytes, or the per-character gradient miscounts and the box tears.

- **Rule 3 — Box borders are literals** Never loop-build a multibyte `═` — concatenation corrupts in the C locale. Every rail ships as a hand-typed literal string.

- **Rule 4 — len on its own line** A combined `local s="$1" len=${#s}` measures `s` before it’s assigned — length zero, and the gradient silently vanishes. The engine’s signature bug, immortalized as a rule.

- **Rule 5 — Leave no dirty terminal** Anything that hides the cursor restores it under a `trap` — on every exit path, Ctrl-C included. The terminal is handed back the way it was found.

## Proven pixel-identical

Extraction invites drift: rewrite the machinery and the look shifts a shade. Phos4’s acceptance bar refused that — **byte-identical** output, enforced by a golden master: renders captured from the original source before extraction, and every engine render since diffed against them, raw ANSI and all.

```
❯ ./test/parity.sh

  ◆ Parity ──────────────────────────────────────────
  the built engine vs the frozen golden master

  ✓ banner-default — byte-identical
  ✓ choose-nav — byte-identical
  ✓ celebrate — byte-identical
  · 24 more captures — every one green

  ╭───────────────────────────────────────────────────────╮
  │                                                       │
  │  ✓  Parity green                                      │
  │     27 of 27 captures byte-identical                  │
  │                                                       │
  ╰───────────────────────────────────────────────────────╯
  Certified Y3K Ready
```

Twenty-seven captures — banners, pickers, panels, both themes, colour and mono — all green. Vendoring the engine back into the Project System deleted **~960 lines** of duplicated look from its first consumer, and that consumer’s release script re-copies the built engine every time it runs — a stale copy can’t ship.

## One file, every theme

**Authored split, shipped single.** Source is an engine plus one file per theme; the build is a concatenation — this is bash, and the build step is a `cat` with opinions:

```
src/engine.sh       the mechanics — rendering + the correctness rules
src/themes/y3k.sh   the default theme: A3K as pure data (the canonical values)
build.sh            engine + themes → one file
dist/phos4.sh       what consumers vendor — every theme aboard
test/               the golden-output parity harness
```

Consumers copy `dist/phos4.sh` into their own repo and `source` it. Zero dependencies, nothing to install, no version to negotiate — the file that ships is the whole engine:

```
# in any bash script
source phos4.sh                          # every phos4_* call, every theme

phos4_render_banner default              # the boxed, gradient-swept wordmark
phos4_step_ok "did the thing"
phos4_choose "Pick one" "Alpha|first" "Beta|second"
echo "$PHOS4_CHOSEN_TITLE"               # prompts answer via environment
```

Three environment variables drive everything: `PHOS4_THEME` picks the theme (default `y3k` — the A3K look), `PHOS4_ANIMATE=1` opts into the power-on entrance, and `PS_MONO=1` goes greyscale.

## Where it lives

Phos4 has no public repo and no standalone download — yet. Today it ships the way it was always meant to: **vendored inside a consumer**. The [Project System kit](https://y3klab.com/project-system/) carries it as `bin/phos4.sh`, rendering the dashboard, the lifecycle scripts, and the installer. A standalone kit in the [Blue Steel](https://y3klab.com/blue-steel/) mold is planned — and until something actually ships, this page stays a read.

- **[A3K](https://y3klab.com/a3k/)** The design language Phos4 renders — palette, temperature map, voice.

- **[Project System](https://y3klab.com/project-system/)** The first consumer — Phos4 rides inside the free download.

- **[Y3K Lab](https://y3klab.com/)** The incubator — every surface that wears A3K.

---

Source: [https://y3klab.com/phos4/](https://y3klab.com/phos4/) — Y3K Lab
