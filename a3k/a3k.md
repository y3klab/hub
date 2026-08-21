# Aesthetic 3000

The design language of **Y3K** - the look every experiment wears.

Built for the year 3000

- **Y3K** ═ the **future**

- **A3K** ═ the **look** it wears

retro-futurist synthwave look

## What A3K is

**A3K** (*Aesthetic 3000*) is a retro-futurist “year 3000” synthwave look - neon magenta→cyan gradients, double-line box-drawing wordmarks, and brief power-on animations. Retro-future computing optimism - a named system in its own right, not a one-off theme.

A3K is the **design language**; **Y3K Lab** is the umbrella incubator that houses the surfaces that wear it - a terminal-UI engine, a Claude Code theme, a project OS, an RC team, a home. Each wears it in its own format. The through-line is the language, not a monorepo.

The verbs are deliberate: a surface wears A3K; an engine like **Phos4** is *fluent* in it and

- renders

it; **built** is reserved for the tagline, *Built for the year 3000*.

## The palette

The one **canonical shared asset**. Everything else - wordmarks, chips, headers, doorways - is the palette bound to a surface’s own tokens. Get the ramp and the temperature map right and a surface reads as Y3K; the rest is binding. All values are **ANSI 256-colour** indices.

The synthwave ramp · magenta → cyan · 7 stops

| ANSI | Hex | Role |
|---:|---|---|
| 201 | `#ff5fff` | magenta · warm end |
| 171 | `#d75fd7` | pink |
| 135 | `#af5fff` | purple |
| 99 | `#875fff` | indigo |
| 75 | `#5fafff` | blue |
| 45 | `#00d7ff` | cyan |
| 51 | `#00ffff` | bright cyan · cool end |

The accent · the single “live” cue - *not* a ramp stop

| ANSI | Hex | Role |
|---:|---|---|
| 39 | `#00afff` | accent · glyphs, spinners, rules |

**39 is the accent; 45 is a ramp stop.** Both are cyan and they are *not* interchangeable. The accent marks the one *live* thing on a screen - a glyph, a spinner, a rule. Cyan **45** is the ramp’s cool end and the right-hand **box-rail** that frames a wordmark, paired with magenta **201** on the left. Reach for 39 when something is alive; reach for 45 when something is structure.

The mono band · a deliberately mid grey (a visible mode)

| ANSI | Hex |
|---:|---|
| 243 | `#767676` |
| 244 | `#808080` |
| 245 | `#8a8a8a` |
| 246 | `#949494` |
| 247 | `#9e9e9e` |
| 248 ·acc | `#a8a8a8` |
| 249 | `#b2b2b2` |

Status

- **ok** 42 · #00d787

- **warn** 220 · #ffd700

- **err** 203 · #ff5f5f

## The temperature map

The identity hangs on one idea: **lifecycle state = colour temperature.** It isn’t decoration - it **enforces the hierarchy for free.** Active pops forward, dormant recedes, with no extra weight or size cue.

- warm · advances

- cool · recedes

- grey · archived

- **Warm - magenta→purple** Active · engaged · “create” actions.

- **Cool - cyan→blue** Inactive · dormant · receding.

- **Grey - the mid band** Archive · done · the focused-tool mode.

## Wordmarks & glyphs

Wordmarks are set in a **double-line box-drawing** font, framed and gradient-filled. There is **no double-line diagonal in Unicode**, so the letters that need one were hand-built from the available pieces - part of the brand’s story, documented so they’re reused, not reinvented.

```

╦  ╦
╚╗╔╝
 ╚╝ V arms converge to a point

╦╗╦
║╚╣
╩ ╩N stems + a ╗╚ diagonal step

╦ ╦
║║║
╚╩╝W an inverted-M

╦ ╦
╚╦╝
 ╩ Y arms drop to a single stem

╔╦╗
 ║
╚╩╝I an I-beam - distinct from T

```

A boxed wordmark has a louder sibling - the **celebration banner** (giant full-block letters) for the moment a surface *finishes* something: an installer’s success, a completed build. The banner shouts the name; a letter-spaced bracketed caption whispers the meaning.

## Gradients

A gradient sweeps the ramp across a string. Section headers take a **temperature-appropriate slice** - so a header sweeps yet stays in its own band. (Every section title on this page is a warm slice; the rule, applied to itself.)

Active *- warm slice, magenta→purple* Inactive *- cool slice, reversed: cyan lands first* Archive *- fixed grey, no sweep*

## Chips

A chip is a short padded label with a background fill. **Three independent dials** - weight, muting, hue - each carry one meaning.

↵ Enter selected row → active → archive ░▒ 3 ▒░

**Bright fill** = primary action · **muted fill** = secondary doorway · **colour** = section or destination.

## Animation

Animated moments are **opt-in or one-shot, and short** - a banner *powers on* (rows reveal top→bottom), *shimmers* (the 16-stop ramp marches down), then *settles* into the static gradient. Two rules: **degrade off-TTY** (never animate into a pipe) and **stay sub-second**. Animations are **punctuation, not entertainment.**

AESTHETIC 3000 ▶ Power on

This whole page powered on the same way when it loaded - reveal, then settle. (Respects `prefers-reduced-motion`.)

## Voice

The words are part of the brand too.

- **Tagline - a standalone stamp** Built for the year 3000

- **Motto - the sign-off, after the “Y2K Ready” stickers** Certified Y3K Ready

## Tables

A table is how A3K states canon - the palette, the statuses, the element registry are all tables. The **registry style** reads as an *instrument readout*, not a spreadsheet: **rails, not zebra** · headers **whisper** (the caption idiom) · **one ramp rule** crowns the top · the **key column** carries the ink · colour only where it *means* something.

The Y3K element registry · canon, set in the canon style

| Tile | Element | Symbol | Note |
|---|---|---|---|
| 3000 | Y3K Lab | Lab | the umbrella - the whole, not an element |
| 00 | Y3K Home | Home | the household - the count’s zero point |
| 01 | Y3K RC | RC | first of the series - pole position |

**Single-line rails** - double-line stays reserved for wordmarks · **accent** only on the cue-bearing tile numbers · hover = the menu highlight.

## Binding to a surface

The brand travels by **binding the canonical palette to a surface’s own token vocabulary** - ANSI escapes for a terminal, theme-token JSON for an editor, CSS for the web. Pick the temperature of each thing (§3); that answer picks its hue. Use the ramp, not raw colours. Apply the chip-weight rule. If you animate, keep it sub-second. Match the voice.

The surfaces that wear A3K - and where to find them:

- **[Y3K Lab](https://y3klab.com/)** The incubator - every surface that wears A3K.

- **[Blue Steel](https://y3klab.com/blue-steel/)** The palette on Claude Code - theme + status bar.

- **[Project System](https://y3klab.com/project-system/)** The terminal project OS the look grew up in.

---

Source: [https://y3klab.com/a3k/](https://y3klab.com/a3k/) - Y3K Lab
