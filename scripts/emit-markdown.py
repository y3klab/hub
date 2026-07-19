#!/usr/bin/env python3
"""emit-markdown — give every hub section a machine-readable twin.

The hub is hand-authored HTML by design: each page's markup IS the craft (bespoke
inline CSS, scanlines, power-on motion), so markdown can't be the source without
flattening five distinct page designs into one template. This runs the other way —
HTML stays canonical and hand-written; this only DERIVES an additional artifact:

    <section>/index.html   →   <section>/<section>.md      (front-matter-free prose)
    all sections           →   /llms.txt                   (the machine index)

That is why this is not the "build step or framework" the hub's conventions rule
out: nothing sits between author and output, and no page is generated from a
template. Deleting this script would cost the .md twins and nothing else.

Naming follows the node law — a file that represents its container takes the
container's name (fractal-self-describing-nodes/fractal-self-describing-nodes.md),
which is the very rule the FSDN page documents.

⚠️ Run AFTER any upstream sync (a3k ← y3k-brand, blue-steel ← dotfiles,
project-system ← project-system). The .md is derived from the published HTML, so
syncing a section and not re-running this leaves a stale twin.

Usage:  python3 scripts/emit-markdown.py [--check]
        --check  verify twins are current without writing (exit 1 if stale)
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://y3klab.com"

# Sections that carry extractable prose inside a single <article>. The landing page
# is a card grid — llms.txt IS its machine-readable twin, so it gets no .md.
# a3k/ is deliberately absent: it has no <article> and its substance is visual
# (swatch grids, glyph tables, decoders); a mechanical twin would misrepresent it.
SECTIONS = ("fractal-self-describing-nodes", "blue-steel", "project-system")

# Landing page + every section, for llms.txt. (title, url_path) — title is read
# from each page's <title>, so this list only fixes order and membership.
INDEXED = ("", "a3k", "blue-steel", "fractal-self-describing-nodes", "project-system")

BLOCK = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "pre", "tr"}
SKIP = {"style", "script", "svg", "nav", "footer", "head", "title", "noscript"}
VOID = {"br", "img", "hr", "input", "meta", "link", "source"}
# Divs whose content is a terminal/tree mockup — preserved verbatim in a fence.
PRE_CLASSES = {"tree", "term", "screen"}
# Display-only chrome: heading numerals ("01", "i"), the eyebrow above the H1, the
# decorative arrow on linked cards. Dropping these keeps markdown headings clean.
DROP_CLASSES = {"n", "i", "band-label", "sw-idx", "kicker", "arw", "spin"}
# Card-style children that are semantically list items, whatever tag they use
# (FSDN's "Instances" uses a mix of div.item and a.item).
ITEM_CLASSES = {"item"}
# Labelled spans that carry visual hierarchy on the page; mirror it in markdown so
# a flat line ("Holon & holarchy whole-and-part Koestler, 1967") keeps its structure.
STRONG_CLASSES = {"src"}
EM_CLASSES = {"tag"}


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.buf: list[str] = []
        self.stack: list[tuple[str, str]] = []   # (tag, class)
        self.depth_skip = 0
        self.depth_drop = 0
        self.in_article = False
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
            # Never emit an empty fence — decorative sub-divs inside a terminal
            # mockup would otherwise leave ``` ``` pairs wrapping whitespace.
            if re.search(r"[A-Za-z0-9]", text):
                self.out.append("```\n" + text.strip("\n") + "\n```")
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
        if tag == "article":
            self.in_article = True
            return
        if not self.in_article:
            return
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

        if set(cls.split()) & ITEM_CLASSES:
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
            # Inside a mockup, block boundaries are layout, not structure — flushing
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
        if tag == "article":
            self._flush()
            self.in_article = False
            return
        if not self.in_article:
            return
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

        if set(cls.split()) & ITEM_CLASSES:
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
        elif tag == "span" and cls.strip():
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
    # Drop the site suffix — llms.txt is already headed "Y3K Lab". Anchored to the
    # END so the landing page's "Y3K Lab — Built for the year 3000" is untouched.
    return re.sub(r"\s*[|—-]\s*Y3K Lab$", "", t)


def page_description(html: str) -> str:
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def render(section: str) -> str:
    html = (ROOT / section / "index.html").read_text(encoding="utf-8")
    ex = Extractor()
    ex.feed(html)
    body = "\n\n".join(b for b in ex.out if b.strip())
    body = re.sub(r"\n{3,}", "\n\n", body)
    src = f"{SITE}/{section}/"
    return f"{body}\n\n---\n\nSource: [{src}]({src}) — Y3K Lab\n"


def render_llms() -> str:
    lines = [
        "# Y3K Lab — y3klab.com",
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
        print("current — every twin matches its page.")
        return 0
    dest.write_text(new, encoding="utf-8")
    print(f"  llms.txt  ({len(new.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
