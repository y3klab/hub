#!/usr/bin/env python3
"""emit-markdown - give every hub section a machine-readable twin.

The hub is hand-authored HTML by design: each page's markup IS the craft (bespoke
inline CSS, scanlines, power-on motion), so markdown can't be the source without
flattening five distinct page designs into one template. This runs the other way -
HTML stays canonical and hand-written; this only DERIVES an additional artifact:

    <section>/index.html   →   <section>/<section>.md      (front-matter-free prose)
    all sections           →   /llms.txt                   (the machine index)

That is why this is not the "build step or framework" the hub's conventions rule
out: nothing sits between author and output, and no page is generated from a
template. Deleting this script would cost the .md twins and nothing else.

Naming follows the node law - a file that represents its container takes the
container's name (fractal-self-describing-nodes/fractal-self-describing-nodes.md),
which is the very rule the FSDN page documents.

⚠️ Run AFTER any upstream sync (a3k ← y3k-brand, blue-steel ← dotfiles,
project-system ← project-system). The .md is derived from the published HTML, so
syncing a section and not re-running this leaves a stale twin.

Usage:  python3 scripts/emit-markdown.py [--check]
        --check  verify twins are current without writing (exit 1 if stale)
"""
from __future__ import annotations

import html as _html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://y3klab.com"

# Sections with an extractable content root (every page uses class="wrap"). The
# landing page is a card grid - llms.txt IS its machine-readable twin, so no .md.
# a3k/ WAS excluded on the assumption its substance is visual; that was wrong. The
# page is mostly prose, and its swatch/mono grids and registry table lift cleanly
# into markdown tables (see `lift` in render), so it earns a twin like the rest.
SECTIONS = ("fractal-self-describing-nodes", "blue-steel", "project-system", "a3k", "phos4")

# Landing page + every section, for llms.txt. (title, url_path) - title is read
# from each page's <title>, so this list only fixes order and membership.
INDEXED = ("", "a3k", "blue-steel", "fractal-self-describing-nodes", "phos4", "project-system")

BLOCK = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "pre", "tr"}
SKIP = {"style", "script", "svg", "nav", "footer", "head", "title", "noscript"}
VOID = {"br", "img", "hr", "input", "meta", "link", "source"}
# Divs whose content is a terminal/tree mockup - preserved verbatim in a fence.
# NB: "decoder" is deliberately NOT here. It reads as art (the ═ rules) but is
# prose carrying **emphasis** - fencing it printed literal asterisks in the twin
# on both a3k and phos4. Fence only things that need column alignment.
PRE_CLASSES = {"tree", "term", "screen", "glyphs"}
# The content root, shared by every page: <article class="wrap"> on the three prose
# pages, <div class="wrap"> on a3k. Keying on the class (not the tag) covers both.
ROOT_CLASS = "wrap"
# Swatch grids carry real data (ANSI index / hex / role) behind presentational divs;
# lifted into a markdown table rather than flattened into a run-on line.
SWATCH_RE = re.compile(
    r'sw-idx">([^<]*)<.*?sw-hex">([^<]*)<.*?sw-role">([^<]*)<', re.S)
# The greyscale band is the same idea in different clothes: the hex lives in the
# chip's style attribute rather than a text node.
MONO_RE = re.compile(
    r'mono-chip" style="background:\s*(#[0-9a-fA-F]{6})".*?mono-cap">([^<]*)<', re.S)
TABLE_ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<(th|td)[^>]*>(.*?)</\1>", re.S)


def _text(frag: str) -> str:
    """Tags out, entities decoded, whitespace collapsed."""
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", frag))).strip()


def close_div(src: str, start: int) -> int:
    """Index just past the </div> that closes the <div> opening at `start`.

    A depth counter, not a closing-tag pattern: the grids nest to different depths
    (mono-band is one level shallower than swatches), and a fixed `</div></div>…`
    regex silently matches the wrong span - which is exactly how the mono-band lift
    failed the first time."""
    depth, i = 0, start
    for m in re.finditer(r"<(/?)div\b[^>]*>", src[start:]):
        depth += -1 if m.group(1) else 1
        i = start + m.end()
        if depth == 0:
            return i
    return i


def table_md(block: str) -> str:
    """A real <table> - keep it a table instead of flattening it to a run-on."""
    rows = []
    for rm in TABLE_ROW_RE.finditer(block):
        cells = [_text(c) for _, c in CELL_RE.findall(rm.group(1))]
        if any(cells):
            rows.append(cells)
    if len(rows) < 2:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)
# Display-only chrome: heading numerals ("01", "i"), the eyebrow above the H1, the
# decorative arrow on linked cards. Dropping these keeps markdown headings clean.
# NB: "band-label" is deliberately NOT here. It names each palette band ("The
# synthwave ramp", "The accent", "Status") - without it the twin shows three
# unlabelled tables in a row and a reader can't tell which is which.
DROP_CLASSES = {"n", "i", "sw-idx", "kicker", "arw", "spin", "sec-num", "eyebrow"}
# Card-style children that are semantically list items, whatever tag they use
# (FSDN's "Instances" uses a mix of div.item and a.item).
# NB: "d" is deliberately NOT here. It names a card's *description* on FSDN
# (span.d, inline) and on a3k (div.d, inside div.tleg) - treating it as an item
# splits every card off from its own heading. The wrappers (item/tleg/door) are
# the items; d is always their tail.
ITEM_CLASSES = {"item", "vrow", "warm", "cool", "grey", "tleg", "status", "door",
                "dec-row"}
# Labelled spans that carry visual hierarchy on the page; mirror it in markdown so
# a flat line ("Holon & holarchy whole-and-part Koestler, 1967") keeps its structure.
STRONG_CLASSES = {"src", "h", "vlabel", "nm", "dh", "dec-mark"}
EM_CLASSES = {"tag"}
# Band labels head a palette/demo band ("The engine at work", "The accent"). They're
# not list items and not headings - just their own line. Without an explicit flush
# they glue onto whatever paragraph precedes them.
LABEL_CLASSES = {"band-label", "surfaces-label"}


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.buf: list[str] = []
        self.stack: list[tuple[str, str]] = []   # (tag, class)
        self.depth_skip = 0
        self.depth_drop = 0
        self.in_article = False
        self.wrap_depth = 0
        self.pre_depth = 0
        self.list_depth = 0
        self.href: str | None = None

    # -- helpers ---------------------------------------------------------
    def _cls(self, attrs) -> str:
        return dict(attrs).get("class", "")

    def _flush(self, prefix: str = "") -> None:
        text = "".join(self.buf)
        self.buf.clear()
        if self.pre_depth:
            # Never emit an empty fence - decorative sub-divs inside a terminal
            # mockup would otherwise leave ``` ``` pairs wrapping whitespace.
            if re.search(r"[A-Za-z0-9]", text):
                # Trailing spaces are invisible on the page but noise in a fence.
                body = "\n".join(l.rstrip() for l in text.strip("\n").splitlines())
                self.out.append("```\n" + body + "\n```")
            return
        text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
        text = re.sub(r"\s{2,}", " ", text)
        # Closing a classed inline element injects a space so abutting spans don't
        # fuse ("Holon & holarchy" + "whole-and-part"). Undo it before punctuation.
        text = re.sub(r"\s+([,.;:!?)\]])", r"\1", text).strip()
        if text:
            self.out.append(prefix + text)

    # -- parsing ---------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        cls = self._cls(attrs)
        if not self.in_article:
            if ROOT_CLASS in cls.split():
                self.in_article = True
                self.wrap_depth = 0
            return
        if tag not in VOID:
            self.wrap_depth += 1
        if tag in SKIP:
            self.depth_skip += 1
            return
        if self.depth_skip:
            return
        # Dropped subtrees: count every nested open tag so we leave at the right depth.
        if self.depth_drop:
            if tag not in VOID:
                self.depth_drop += 1
            return
        if set(cls.split()) & DROP_CLASSES:
            if tag not in VOID:
                self.depth_drop += 1
            return

        if set(cls.split()) & (ITEM_CLASSES | LABEL_CLASSES):
            self._flush()
        if not self.pre_depth:
            if set(cls.split()) & STRONG_CLASSES:
                self.buf.append("**")
            elif set(cls.split()) & EM_CLASSES:
                self.buf.append(" *")
        if tag == "div" and (set(cls.split()) & PRE_CLASSES):
            self._flush()
            self.pre_depth += 1
        elif tag == "br":
            self.buf.append("\n" if self.pre_depth else " ")
        elif tag in ("ul", "ol"):
            self._flush()
            self.list_depth += 1
        elif tag in BLOCK:
            # Inside a mockup, block boundaries are layout, not structure - flushing
            # on them would shatter one terminal into a dozen fences.
            if not self.pre_depth:
                self._flush()
            else:
                self.buf.append("\n")
        elif tag == "a":
            self.href = dict(attrs).get("href")
        elif tag == "code" and not self.pre_depth:
            self.buf.append("`")
        elif tag in ("em", "i"):
            self.buf.append("*")
        elif tag in ("strong", "b"):
            self.buf.append("**")
        self.stack.append((tag, cls))

    def handle_endtag(self, tag):
        if not self.in_article:
            return
        # Depth back to zero = the root element just closed. Everything after it
        # (the footer, in every hub page) is chrome and must not reach the twin.
        if self.wrap_depth == 0:
            self._flush()
            self.in_article = False
            return
        self.wrap_depth -= 1
        if tag in SKIP:
            self.depth_skip = max(0, self.depth_skip - 1)
            return
        if self.depth_skip:
            return
        if self.depth_drop:
            self.depth_drop -= 1
            return

        cls = ""
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                cls = self.stack[i][1]
                del self.stack[i]
                break

        if set(cls.split()) & LABEL_CLASSES:
            self._flush()
        elif set(cls.split()) & ITEM_CLASSES:
            self._flush("- ")
            self.href = None
        elif tag == "div" and (set(cls.split()) & PRE_CLASSES):
            self._flush()
            self.pre_depth = max(0, self.pre_depth - 1)
        elif tag in ("ul", "ol"):
            self.list_depth = max(0, self.list_depth - 1)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush("#" * int(tag[1]) + " ")
        elif tag == "li":
            self._flush("- ")
        elif tag == "blockquote":
            self._flush("> ")
        elif tag in BLOCK:
            if not self.pre_depth:
                self._flush()
        elif tag == "a":
            self.href = None
        elif tag == "code" and not self.pre_depth:
            self.buf.append("`")
        elif tag in ("em", "i"):
            self.buf.append("*")
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag in ("span", "div") and cls.strip():
            if not self.pre_depth and (set(cls.split()) & STRONG_CLASSES):
                self.buf.append("**")
            elif not self.pre_depth and (set(cls.split()) & EM_CLASSES):
                self.buf.append("*")
            # Labelled spans often abut with no whitespace in the source; keep them
            # from fusing. _flush() strips the space back off before punctuation.
            self.buf.append(" ")

    def handle_data(self, data):
        if not self.in_article or self.depth_skip or self.depth_drop:
            return
        if self.href is not None and data.strip():
            url = self.href
            if url.startswith("/"):
                url = SITE + url
            elif url.startswith("#") or url.startswith("http"):
                pass
            else:
                url = f"{SITE}/{url.lstrip('./')}"
            self.buf.append(f"[{data.strip()}]({url})")
            self.href = None
            return
        self.buf.append(data)


def page_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    t = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(untitled)"
    # Drop the site suffix - llms.txt is already headed "Y3K Lab". Anchored to the
    # END so the landing page's "Y3K Lab - Built for the year 3000" is untouched.
    return re.sub(r"\s*[|—-]\s*Y3K Lab$", "", t)


def page_description(html: str) -> str:
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def swatch_table(block: str) -> str:
    """A swatch grid is a table wearing presentational divs - lift it back."""
    rows = SWATCH_RE.findall(block)
    if rows:
        out = ["| ANSI | Hex | Role |", "|---:|---|---|"]
        out += [f"| {i.strip()} | `{hx.strip()}` | {r.strip()} |" for i, hx, r in rows]
        return "\n".join(out)
    rows = MONO_RE.findall(block)
    if rows:
        out = ["| ANSI | Hex |", "|---:|---|"]
        out += [f"| {idx.strip()} | `{hx.strip()}` |" for hx, idx in rows]
        return "\n".join(out)
    return ""


def render(section: str) -> str:
    html = (ROOT / section / "index.html").read_text(encoding="utf-8")
    # Replace each swatch grid with a placeholder BEFORE parsing, so the parser
    # can't flatten the chips into a run-on line; the table is spliced back after.
    tables: list[str] = []

    def lift(pattern: str, fn) -> None:
        """Replace each matched block with a placeholder + a built markdown table."""
        nonlocal html
        while True:
            m = re.search(pattern, html)
            if not m:
                return
            end = close_div(html, m.start()) if pattern.startswith("<div") \
                else html.index("</table>", m.start()) + len("</table>")
            built = fn(html[m.start():end])
            if not built:
                return
            tables.append(built)
            html = html[:m.start()] + f"<p>@@SWATCH{len(tables) - 1}@@</p>" + html[end:]

    lift(r'<div class="swatches">', swatch_table)
    lift(r'<div class="mono-band">', swatch_table)
    lift(r"<table[^>]*>", table_md)
    ex = Extractor()
    ex.feed(html)
    body = "\n\n".join(b for b in ex.out if b.strip())
    body = re.sub(r"\n{3,}", "\n\n", body)
    for n, t in enumerate(tables):
        body = body.replace(f"@@SWATCH{n}@@", t)
    if "@@SWATCH" in body:
        raise SystemExit(f"{section}: a swatch placeholder survived - table lift broke")
    src = f"{SITE}/{section}/"
    return f"{body}\n\n---\n\nSource: [{src}]({src}) - Y3K Lab\n"


def render_llms() -> str:
    lines = [
        "# Y3K Lab - y3klab.com",
        "",
        "> The Y3K Lab hub. Each section below links to its plain-Markdown twin;",
        "> the rendered version lives at the same path without the /<name>.md suffix.",
        "",
    ]
    for sec in INDEXED:
        html = (ROOT / (sec or ".") / "index.html").read_text(encoding="utf-8")
        title, desc = page_title(html), page_description(html)
        url = f"{SITE}/{sec}/" if sec else f"{SITE}/"
        target = f"{SITE}/{sec}/{sec}.md" if sec in SECTIONS else url
        lines.append(f"- [{title}]({target}){': ' + desc if desc else ''}")
    return "\n".join(lines) + "\n"


def main(argv) -> int:
    check = "--check" in argv
    stale = []
    for sec in SECTIONS:
        dest = ROOT / sec / f"{sec}.md"
        new = render(sec)
        if check:
            if not dest.exists() or dest.read_text(encoding="utf-8") != new:
                stale.append(str(dest.relative_to(ROOT)))
        else:
            dest.write_text(new, encoding="utf-8")
            print(f"  {dest.relative_to(ROOT)}  ({len(new.splitlines())} lines)")
    dest = ROOT / "llms.txt"
    new = render_llms()
    if check:
        if not dest.exists() or dest.read_text(encoding="utf-8") != new:
            stale.append("llms.txt")
        if stale:
            print("STALE (re-run without --check): " + ", ".join(stale), file=sys.stderr)
            return 1
        print("current - every twin matches its page.")
        return 0
    dest.write_text(new, encoding="utf-8")
    print(f"  llms.txt  ({len(new.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
