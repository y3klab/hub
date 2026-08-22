# Fractal Self-Describing Nodes

**Every node describes itself**, by the same rule, **at every depth** - so there is no index to keep. **The structure is the index.**

## What FSDN is

A **node** is any unit of organization - a whole portfolio, a project, a sub-tool, a single catalog entry. The word is deliberate: a node is never just an item; it is a thing among other things that knows its place among them. Under FSDN, each one carries its own overview inside itself, named for it - made by the same rule as every other node, at every depth - so what lies below any node is computed, never written. Nothing is kept, so nothing goes stale.

### Self-describing

Each node carries its own overview, inside itself and named for it - `project/project.md`. The description is part of the thing, so it can't wander off from the thing.

### One rule

Not a template per level - one rule, applied to whatever is in front of it. The output varies; the rule doesn't. Know one thing, and you can walk the whole structure.

### Every depth

The rule has no depth in it, so there is no depth it stops at. Zoom in or out and you land on a node that explains itself - self-similar, like a fractal. Hence the name.

### No index

What lies below any node is computed - `ls` - never written. A parent's overview describes the parent, not its children. The structure is the index.

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

**Don't create a node that can't describe itself.** Any new container - a project, a sub-tool, a module, a grouping - gets a self-named overview in its level's shape. It points up to its parent; what lies beneath it is found by the same rule, not by a list it keeps - it may curate one, an order or a *start here*, but nothing depends on that list being complete. That single discipline is the whole of FSDN, applied.

**Only containers get the overview - and they earn it.** A leaf - a lone file with nothing beneath it - describes itself in-band, in its own header or metadata, and only points up: its place in the tree is its up-pointer. A container earns an overview when it has something to say that the shape doesn't already; a grouping folder whose contents are self-evident can go without. What the law governs is the *name*: wherever an overview exists, it is named after its container.

**The mechanism is medium-specific.** The law is the *behavior* - self-describe, point up and down - not the file type. Folders a human opens to understand the structure get a `folder/folder.md`. *Code* packages already self-describe in their own idiom - a package docstring, a README - so they satisfy the law without a parallel `.md` that would only shadow the code's own description. The test: *would a human navigate here to understand the system?* If yes, it's an organizational node and earns the overview.

## What it buys

Why enforce FSDN, instead of keeping a good index by hand? Because the law buys properties a maintained map can't:

**The description can't drift from the thing.** The overview lives inside what it describes and is named after it, so the two move together - rename, relocate, or delete a node and its description travels with it. There is no separate map to forget to update, so there is no stale map.

**Navigation doesn't dead-end.** Land at any depth - a deep leaf, a mid-level folder, the root - and you can always read where you are, step up to its context, or step down into its parts. Wayfinding and handoff stop depending on a guide who already knows the layout.

**It scales without a center.** No master document has to know everything; each node knows only itself and its neighbors. Add a thousand nodes and nothing has to be rewired - the rule carries the structure, not a registry that grows more brittle the larger it gets.

**It's traversable by machines, not just people.** The same rule at every depth means a tool - or an AI agent - can walk the structure with no bespoke instructions for any of it. Self-similarity is an API.

## A worked example

Say you add pho to the Y3K Cookbook. The law decides the shape before you do:

```
y3k-cookbook/
├─ y3k-cookbook.md         ← whose kitchen, the chapters, how to read a card
└─ soups/
   ├─ soups.md             ← what counts as soup; stock and simmer basics
   ├─ ramen/
   │  ├─ ramen.md          ← ingredients, steps, provenance; broth + tare
   │  └─ broth/
   │     └─ broth.md       ← ingredients, steps; a day's boil of pork bones
   └─ pho/
      ├─ pho.md            ← ingredients, steps, provenance; broth + greens
      ├─ hero.jpg          ← the finished bowl
      ├─ assembly.jpg      ← the bowl being built
      ├─ broth/
      │  ├─ broth.md       ← ingredients, steps; a recipe inside the recipe
      │  └─ simmering.jpg  ← the pot at hour six
      └─ greens/
         └─ greens.md      ← rau sống: Thai basil, sprouts, lime, chili
```

Four depths, one rule, four different documents. The book's overview is front matter. The chapter's is an opener - what counts as a soup in this kitchen, and the stock and simmer basics every recipe below it assumes. The dish's is a recipe card. The broth's is a recipe card too, because a broth is a recipe. Nobody would confuse them, and nobody wrote a template for each: the same rule, applied to whatever was in front of it, produced all four.

**A recipe of recipes.** Pho is a broth over noodles and a plate of greens - *rau sống*: the basil, sprouts, lime and chili the diner adds, not a garnish but half the dish - and the broth is a recipe in its own right: charred onion and ginger, bones, star anise, a day's simmer. So the node's children are the same kind of thing as the node. `describe(pho)` calls `describe(broth)`. That is the fractal claim, run one turn further than the generator above shows.

**Named for what the path doesn't say.** Three photos, and none is named for the dish, because the folder already is. Inside a node, a file that isn't the overview is named for its role or its subject - `hero.jpg`, `assembly.jpg` - and a photo of the broth lives with the broth, as `broth/simmering.jpg`, because an asset belongs to the node it depicts. The day the hero shot leaves the folder for a flat `images/` directory it becomes `pho-hero.jpg`: the path stopped saying *pho*, so the name has to. The same rule is why two nodes can both be called `broth/` - one inside the ramen, one inside the pho - and neither has to say which.

Navigation works in every direction *for free*: from the chapter you step **down** into the pho; from the pho, **up** to the chapter and across to the ramen; from the broth, up to the bowl it belongs to. Nobody wired those links - the shape did.

**The book's two indexes write themselves.** The table of contents is `ls` - no author types one; it is generated from the chapters at layout, page numbers and all. The index at the back - *star anise, 88, 140* - is generated from the recipe cards by the indexer, never written first. Every cookbook you own already computes both from its structure.

Skip the rule and you get the folder everyone has: `hero.jpg`, and nothing beside it. You can see what it was. You can't make it again - the only way is to ask whoever did, and the day they're gone, so is the dish. That is the provenance line, missing: the one fact a photo can't give back.

The law can't make you write the card - that's the discipline it asks for. What it *guarantees* is the other half: a card written there can never drift to another dish. `pho/pho.md` cannot describe the ramen.

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
