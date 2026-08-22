# Fractal Self-Describing Nodes

**Every node describes itself**, by the same rule, **at every depth** - so there is no index to keep. **The structure is the index.**

## What a node is

A **node** is any unit of organization - the whole portfolio, a project, a sub-tool, a single catalog entry. The word is deliberate: a node is inherently *part of a graph*. It is never just an item; it is a thing that sits among other things and knows its place among them.

The law - **FSDN**, for short - says that whatever the node, and whatever its size, it carries its own identity in the same recognizable shape - and it does so all the way up and all the way down.

## Three properties

### Self-describing

Each node carries its own overview in a consistent, templated shape - the portfolio's overview, a project's overview, a tool's doc. The same “describe yourself” move at every level.

### Scale-invariant

That move repeats at *every* depth. Zoom in or out and you always land on a node that explains itself. Self-similar, like a fractal - hence the name.

### Whole *and* part

Each node is self-contained *and* a member of the node above - and everything beneath it is findable by the same rule, with no list to keep. It's **built to point up** and **down** - both a map and a thing-on-a-map - so navigation needn't dead-end.

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

## Why it matters

Why enforce FSDN, instead of keeping a good index by hand? Because the law buys properties a maintained map can't:

**There is no index to keep.** Because every child names itself by rule, what lies below any node is computed, never written - the directory listing *is* the index. A parent's overview describes the parent, not its children. It may still curate - an order, a *start here* - but nothing depends on that list being complete: delete it, and everything is still findable.

**The description can't drift from the thing.** The overview lives inside what it describes and is named after it, so the two move together - rename, relocate, or delete a node and its description travels with it. There is no separate map to forget to update, so there is no stale map.

**Navigation doesn't dead-end.** Land at any depth - a deep leaf, a mid-level folder, the root - and you can always read where you are, step up to its context, or step down into its parts. Wayfinding and handoff stop depending on a guide who already knows the layout.

**It scales without a center.** No master document has to know everything; each node knows only itself and its neighbors. Add a thousand nodes and nothing has to be rewired - the rule carries the structure, not a registry that grows more brittle the larger it gets.

**It's traversable by machines, not just people.** The same rule at every depth means a tool - or an AI agent - can walk the structure with no bespoke instructions for any of it. Self-similarity is an API.

## A worked example

Say you get back from Yosemite with a phone full of photos. The law decides the shape before you do:

```
photos/
├─ photos.md            ← describes the collection
└─ 2024/
   ├─ 2024.md           ← describes the year
   ├─ birthday/
   │  └─ birthday.md
   └─ yosemite/         ← the new node, named for the trip
      ├─ yosemite.md    ← names itself: who, when, where
      ├─ half-dome.jpg  ← leaves: each names its subject;
      └─ campfire.jpg      the file itself carries the rest
```

The folder is named for the trip; inside it, a file named for the folder describes it - the self-naming move. The photos beside it are leaves: each is named for what it shows, and the file itself carries the rest - the date, the place, the camera - the digital back of the print. Navigation now works in both directions *for free*: from the year you step **down** into the trip; from the trip you step **up** to the year and across to the birthday. Nobody wired those links - the shape did.

Skip the rule and you get what everyone already owns: a folder of `IMG_4821.jpg` through `IMG_4990.jpg` with nothing beside them - a node that can't describe itself. Who is this? Where was it? Ten years on, the only way to know is to find someone who was there. The tempting patch is a list in `2024.md` - *July: Yosemite* - but that is exactly the index the law exists to dissolve: kept by hand, and only ever as true as its last edit.

The shoebox of prints makes the distinction physical. What's written on the back of a photo - *Yosemite, July 2024, Mom and Sam* - travels with it forever; it can't get separated from the thing it describes. The index card taped inside the lid is the separate map: true the day it's written, wrong the day someone reshuffles the boxes. The law can't force you to write on the back - that's the discipline FSDN asks for. What it *guarantees* is the other half: write it there, and it can never drift from the thing.

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
