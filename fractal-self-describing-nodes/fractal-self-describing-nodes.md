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

A single rule of construction makes the law concrete: a container's overview is **named after the container**. Because the description lives inside the thing and carries its name, it can't separate from it - that co-location is what the law **structurally enforces**; completeness and accuracy stay a *discipline*.

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

**There is no depth parameter.** A fractal tree drawn by code is `draw(branch, depth - 1)`: its branches don't exist until the rule invents them, so the rule has to carry its own stopping point. This one stops where the data stops - at a node with no children - which is why the law can say *at every depth* without naming one.

**What the rule asks of you.** Every container gets a self-named overview - don't create a node that can't describe itself - but only containers, and only when there is something to say: a leaf describes itself in-band, in its own header, and a grouping folder whose contents are self-evident can go without. The law governs the name, not the file type - a code package already describes itself through its docstring or README and needs no parallel `.md`. The test: *would a human navigate here to understand the system?* If yes, it earns the overview. A parent may still curate a list of what's below it; nothing may depend on that list.

## Why it matters

Why enforce FSDN instead of keeping a good index by hand? Because the law buys what a maintained map can't. **The description can't drift from the thing**: it lives inside what it describes and carries its name, so rename, move, or delete a node and its description travels with it. **Navigation doesn't dead-end**: land at any depth and you can read where you are, step up to its context, or down into its parts, with no guide who already knows the layout. **It scales without a center**: no master document has to know everything, so add a thousand nodes and nothing is rewired. And **it's traversable by machines** as well as people: one rule at every depth means a tool - or an AI agent - can walk the whole structure with no instructions for any of it. Self-similarity is an API.

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

One rule produced all of it - front matter, a chapter opener, recipe cards, and, because a broth is a recipe, a recipe inside the recipe: `describe(pho)` calls `describe(broth)`. The photos are named for what they show, not for the dish; the folder already says *pho*. The table of contents is `ls`, and the index at the back is generated from the cards - every cookbook you own already computes both. Skip the rule and you get the folder everyone has: `hero.jpg` and nothing beside it. You can see what it was. You can't make it again.

## Where it runs

Two systems already run on the law - the node pointing **down**:

- **[The Project System](https://y3klab.com/project-system/)** - a workspace where a project is a folder and every folder's overview carries its name, the root included: `Projects/projects.md` describes the workspace and lists no projects; the dashboard reads the disk. It once kept a master `INDEX.md`, with a drift check to police it. Both are gone.

- **[The Y3K RC Garage](https://garage.y3krc.com)** - a fleet catalog where every vehicle is a node: `fleet/<slug>/<slug>.md` plus role-named assets. The site is rendered from the nodes; no list of vehicles exists anywhere.

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
