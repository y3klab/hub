# Fractal Self-Describing Nodes

**Every node describes itself**, by the same rule, **at every depth** - so there is no index to keep. **The structure is the index.**

## What FSDN is

**Every node describes itself.** A node is any unit of organization - a whole portfolio, a project, a sub-tool, a single catalog entry. The word is deliberate: a node is never just an item; it is a thing among other things that knows its place among them. To describe itself, a node carries its own overview *inside* itself, named for it - `project/project.md`. The description is part of the thing, so it can't wander off from the thing.

**By the same rule.** Not a template per level - one rule, applied to whatever is in front of it. A portfolio's overview, a project's, and a catalog entry's look different; they were all made the same way. That sameness is what lets one reader - a person, a script, an AI agent - walk the whole structure knowing one thing.

**At every depth.** The rule has no depth in it, so there is no depth it stops at. Zoom in or out and you land on a node that explains itself: self-similar, the way a fractal is one rule applied at every depth. Hence the name.

**So there is no index to keep. The structure is the index.** Because every child names itself by the rule, what lies below any node is computed - `ls` - never written. A parent's overview describes the parent, not its children; it may curate - an order, a *start here* - but nothing depends on that list being complete. Each node is both a map and a thing-on-a-map: it points up to its parent by where it sits, and down to its children by the rule. Delete every list, and everything is still findable.

### Self-describing

Each node carries its own overview, inside itself and named for it. The description is part of the thing it describes.

### One rule

The same move at every level. The output varies; the rule doesn't - one thing to know, and the whole structure is walkable.

### Every depth

The rule has no depth in it, so there is no depth it stops at. Self-similar, like a fractal - hence the name.

### No index

What lies below any node is computed, never written. Nothing is kept, so nothing goes stale. The structure is the index.

## The mechanism

The law isn't a metaphor - a single rule of construction makes it concrete: a container's overview is **named after the container**, in the shape that level uses. That co-location **structurally enforces it against orphaning and drift** - the description can't separate from the thing it describes - while completeness and accuracy stay a *discipline*. The same law, one level down, forever.

```
# a self-naming overview at every depth
portfolio/
├─ portfolio.md         ← the portfolio describes itself
└─ project/
   ├─ project.md        ← the project describes itself
   └─ tool/
      └─ tool.md        ← the tool describes itself
```

Written as code, the rule is one function that calls itself - the way a fractal tree is drawn:

```
# the generator, as a rewrite rule:  node → node.md  node*
describe(node):
    node/node.md              ← the node describes itself
    for child in node:        ← and so does everything beneath it,
        describe(child)          by the same rule
```

**Notice what's missing.** A fractal tree drawn by code is `draw(branch, depth - 1)`: its branches don't exist until the rule invents them, so the rule has to carry its own stopping point. Here there is no depth parameter. The recursion stops where the data stops - at a node with no children - which is why the law can say *at every depth* without naming one.

**Don't create a node that can't describe itself.** Any new container - a project, a sub-tool, a module, a grouping - gets a self-named overview in its level's shape. It points up to its parent; what lies beneath it is found by the same rule, not by a list it keeps. That single discipline is the whole of FSDN, applied.

**Only containers get the overview - and they earn it.** A leaf - a lone file with nothing beneath it - describes itself in-band, in its own header or metadata, and only points up: its place in the tree is its up-pointer. A container earns an overview when it has something to say that the shape doesn't already; a grouping folder whose contents are self-evident can go without. What the law governs is the *name*: wherever an overview exists, it is named after its container.

**The mechanism is medium-specific.** The law is the *behavior* - self-describe, point up and down - not the file type. Folders a human opens to understand the structure get a `folder/folder.md`. *Code* packages already self-describe in their own idiom - a package docstring, a README - so they satisfy the law without a parallel `.md` that would only shadow the code's own description. The test: *would a human navigate here to understand the system?* If yes, it's an organizational node and earns the overview.

## What it buys

Why enforce FSDN, instead of keeping a good index by hand? Because the law buys properties a maintained map can't:

**The description can't drift from the thing.** The overview lives inside what it describes and is named after it, so the two move together - rename, relocate, or delete a node and its description travels with it. There is no separate map to forget to update, so there is no stale map.

**Navigation doesn't dead-end.** Land at any depth - a deep leaf, a mid-level folder, the root - and you can always read where you are, step up to its context, or step down into its parts. Wayfinding and handoff stop depending on a guide who already knows the layout.

**It scales without a center.** No master document has to know everything; each node knows only itself and its neighbors. Add a thousand nodes and nothing has to be rewired - the rule carries the structure, not a registry that grows more brittle the larger it gets.

**It's traversable by machines, not just people.** The same rule at every depth means a tool - or an AI agent - can walk the structure with no bespoke instructions for any of it. Self-similarity is an API.

## A worked example

Say you add an apple pie to the Y3K Cookbook. The law decides the shape before you do:

```
y3k-cookbook/
├─ y3k-cookbook.md        ← whose kitchen, the chapters, how to read a card
└─ desserts/
   ├─ desserts.md         ← what counts as dessert; pastry and sugar basics
   ├─ lemon-tart/
   │  └─ lemon-tart.md    ← ingredients, steps, provenance, related recipes
   └─ apple-pie/
      ├─ apple-pie.md     ← ingredients, steps, provenance; crust + filling
      ├─ hero.jpg         ← the finished pie
      ├─ crust/
      │  └─ crust.md      ← ingredients, steps; a recipe inside the recipe
      └─ filling/
         └─ filling.md    ← ingredients, steps
```

Four depths, one rule, four different documents. The book's overview is front matter. The chapter's is an opener - what counts as a dessert in this kitchen, and the pastry and sugar basics every recipe below it assumes. The dish's is a recipe card. The crust's is a recipe card too, because a crust is a recipe. Nobody would confuse them, and nobody wrote a template for each: the same rule, applied to whatever was in front of it, produced all four.

**A recipe of recipes.** The pie is a crust and a filling, and each of those is a recipe in its own right - so the node's children are the same kind of thing as the node. `describe(apple-pie)` calls `describe(crust)`. That is the fractal claim, run one turn further than the generator above shows.

Navigation works in every direction *for free*: from the chapter you step **down** into the pie; from the pie, **up** to the chapter and across to the lemon tart; from the crust, up to the pie it belongs to. Nobody wired those links - the shape did.

**The book's two indexes write themselves.** The table of contents is `ls` - no author types one; it is generated from the chapters at layout, page numbers and all. The index at the back - *apples, 112, 140* - is generated from the recipe cards by the indexer, never written first. Every cookbook you own already computes both from its structure.

Skip the rule and you get the folder everyone has: `hero.jpg`, and nothing beside it. You can see what it was. You can't make it again - the only way is to ask whoever did, and the day they're gone, so is the dish. That is the provenance line, missing: the one fact a photo can't give back.

The law can't make you write the card - that's the discipline it asks for. What it *guarantees* is the other half: a card written there can never drift to another dish. `apple-pie/apple-pie.md` cannot describe the lemon tart.

## Instances

FSDN is already load-bearing across the lab - the node pointing **down**. Each of these describes itself, and everything beneath it describes itself the same way:

- **The self-identifying filesystem** - a folder's overview is named after the folder, at every level, the workspace root included: `Projects/projects.md` describes the workspace and lists no projects - a project is a folder in a tier, and the dashboard reads the disk. The Project System runs on this; the master `INDEX.md` it once kept, drift check and all, is gone.

- **A folder-per-tool catalog** - `stack/<tool>/<tool>.md`, each entry a self-describing node in a folder-per-tool shape.

- **[The Y3K RC Garage](https://garage.y3krc.com)** - a fleet catalog where every vehicle is a node: `fleet/<slug>/<slug>.md` plus role-named assets.

- **An ecosystem map** - a self-describing node for an entire multi-project ecosystem, spanning platforms, tools, and catalogs alike.

## Lineage

This is a deliberate synthesis, not a coinage from nothing. What's genuinely new is none of the pieces below but their **fusion - and the insistence on enforcing it**: the synthesis becomes a rule of construction rather than a description added after the fact - a self-naming overview at every depth, so a structure can never drift from the thing that explains it. The ideas it fuses:

- **Holon & holarchy** *whole-and-part* Koestler, 1967 - a thing that is simultaneously a whole and a part. The closest single-named ancestor.

- **The Composite pattern** *in code* Gang of Four - treat an individual object and a composition of objects uniformly. The same idea, stated for software.

- **HATEOAS · Zettelkasten · Maps of Content** *up/down links* Hypermedia that carries its own links; atomic notes, each self-contained yet an index to others. The “no dead-ends” property.

- **Self-similarity** *fractal* Mandelbrot - one generator, applied at every depth; the part resembles the whole, at every scale.

This page is itself a fractal self-describing node. It names itself, it points **up** to its parent - [the Y3K Lab hub](https://y3klab.com/) - and **down** to [its instances](#instances). It practices what it documents.

Every node is a fractal self.

---

Source: [https://y3klab.com/fractal-self-describing-nodes/](https://y3klab.com/fractal-self-describing-nodes/) - Y3K Lab
