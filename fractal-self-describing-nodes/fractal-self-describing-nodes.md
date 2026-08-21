# Fractal Self-Describing Nodes

**Every node describes itself**, in a consistent shape, **at every altitude.**

## What a node is

A **node** is any unit of organization - the whole portfolio, a project, a sub-tool, a single catalog entry. The word is deliberate: a node is inherently *part of a graph*. It is never just an item; it is a thing that sits among other things and knows its place among them.

The law says that whatever the node, and whatever its size, it carries its own identity in the same recognizable shape - and it does so all the way up and all the way down.

## Three properties

### Self-describing

Each node carries its own overview in a consistent, templated shape - the portfolio's index, a project's overview, a tool's doc. The same “describe yourself” move at every level.

### Scale-invariant

That move repeats at *every* altitude. Zoom in or out and you always land on a node that explains itself. Self-similar, like a fractal - hence the name.

### Whole *and* part

Each node is self-contained *and* a member of the node above and an index to the nodes below. It's **built to point up** and **down** - both a map and a thing-on-a-map - so navigation needn't dead-end.

## The mechanism

The law isn't a metaphor - a single rule of construction makes it concrete: a container's overview is **named after the container**, in the shape that level uses. That co-location **structurally enforces it against orphaning and drift** - the description can't separate from the thing it describes - while completeness and accuracy stay a *discipline*. The same law, one level down, forever.

```
# a self-naming index file at every altitude
portfolio/
├─ INDEX.md             ← the portfolio describes itself
└─ project/
   ├─ project.md        ← the project describes itself
   └─ tool/
      └─ tool.md       ← the tool describes itself
```

**Don't create a node that can't describe itself.** Any new container - a project, a sub-tool, a module, a grouping - gets a self-named overview in its level's shape, pointing up to its index and down to its children. That single discipline is the whole law, applied.

**The mechanism is medium-specific.** The law is the *behavior* - self-describe, point up and down - not the file type. Folders a human opens to understand the structure get a `folder/folder.md`. *Code* packages already self-describe in their own idiom - a package docstring, a README - so they satisfy the law without a parallel `.md` that would only shadow the code's own description. The test: *would a human navigate here to understand the system?* If yes, it's an organizational node and earns the overview.

## Why it matters

Why enforce this, instead of keeping a good index by hand? Because the law buys properties a maintained map can't:

**The description can't drift from the thing.** The overview lives inside what it describes and is named after it, so the two move together - rename, relocate, or delete a node and its description travels with it. There is no separate map to forget to update, so there is no stale map.

**Navigation doesn't dead-end.** Land at any altitude - a deep leaf, a mid-level folder, the root - and you can always read where you are, step up to its context, or step down into its parts. Wayfinding and handoff stop depending on a guide who already knows the layout.

**It scales without a center.** No master document has to know everything; each node knows only itself and its neighbors. Add a thousand nodes and nothing has to be rewired - the rule carries the structure, not a registry that grows more brittle the larger it gets.

**It's traversable by machines, not just people.** A predictable shape at every altitude means a tool - or an AI agent - can walk the structure with no bespoke instructions per level. Self-similarity is an API.

## A worked example

Say you add a Traxxas Maxx to the [Garage](https://garage.y3krc.com). The law decides the shape before you do:

```
fleet/
├─ INDEX.md              ← lists every vehicle
└─ traxxas-maxx/         ← the new node, named for the slug
   ├─ traxxas-maxx.md    ← names itself; describes the vehicle
   └─ hero.png            ← a role-named asset
```

The folder is named for the vehicle; inside it, a file named for the folder describes it - the self-naming move. Navigation now works in both directions *for free*: from the fleet index you step **down** into the vehicle; from the vehicle you step **up** to the index and across to its siblings. Nobody wired those links - the shape did.

Skip the rule and you get a folder of assets with no `traxxas-maxx.md`: a node that can't describe itself. It might still be listed in `INDEX.md` - but that listing is now hand-maintained, and the day it isn't, the index lies and the folder is a dead-end. The law can't force you to create the node - that's the discipline it asks for. What it *guarantees* is the other half: follow it and the node names and describes itself, so there's no separate listing to fall out of sync - the description can't drift from the thing.

## Instances

The law is already load-bearing across the lab - the node pointing **down**. Each of these describes itself and indexes the nodes beneath it:

- **The self-identifying filesystem** - a folder's overview is named after the folder, at every level. The Project System runs on this.

- **A folder-per-tool catalog** - `stack/<tool>/<tool>.md`, each entry a self-describing node under a master index.

- **[The Y3K RC Garage](https://garage.y3krc.com)** - a fleet catalog where every vehicle is a node: `fleet/<slug>/<slug>.md` plus role-named assets.

- **An ecosystem map** - a self-describing node for an entire multi-project ecosystem, indexing platforms, tools, and catalogs alike.

## Lineage

This is a deliberate synthesis, not a coinage from nothing. What's genuinely new is none of the pieces below but their **fusion - and the insistence on enforcing it**: the synthesis becomes a rule of construction rather than a description added after the fact - a self-naming index file at every altitude, so a structure can never drift from the thing that explains it. The ideas it fuses:

- **Holon & holarchy** *whole-and-part* Koestler, 1967 - a thing that is simultaneously a whole and a part. The closest single-named ancestor.

- **The Composite pattern** *in code* Gang of Four - treat an individual object and a composition of objects uniformly. The same idea, stated for software.

- **HATEOAS · Zettelkasten · Maps of Content** *up/down links* Hypermedia that carries its own links; atomic notes, each self-contained yet an index to others. The “no dead-ends” property.

- **Self-similarity** *fractal* Mandelbrot - the part resembles the whole, at every scale.

This page is itself a fractal self-describing node. It names itself, it points **up** to its index - [the Y3K Lab hub](https://y3klab.com/) - and **down** to [its instances](#instances). It practices what it documents.

Every node is a fractal self.

---

Source: [https://y3klab.com/fractal-self-describing-nodes/](https://y3klab.com/fractal-self-describing-nodes/) - Y3K Lab
