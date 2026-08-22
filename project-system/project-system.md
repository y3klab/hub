# Project System

Spin up projects, shelve them, archive them, and always know what you're building - from the terminal, with **no master list to keep**: the workspace *is* the list. Pure bash, zero daemons, **Claude Code** intake built in. Yours the moment you unzip it.

## What you get

One dashboard answers the question every side-project-haver dreads - **“what am I building, and where did I leave it?”** Type `proj` and your whole portfolio is on screen - read straight off the disk, so a folder in the workspace is a project, with nothing to register and no list that can go stale. Arrow keys to move, **Enter** to drop into a project with Claude Code already open, **m** to move or delete it:

```
❯ proj

  ╔═════════════════════════════════╗
  ║ ╔═╗ ╦═╗ ╔═╗  ╦  ╔═╗ ╔═╗ ╔╦╗ ╔═╗ ║
  ║ ╠═╝ ╠╦╝ ║ ║  ║  ╠═  ║    ║  ╚═╗ ║
  ║ ╩   ╩╚═ ╚═╝ ╚╝  ╚═╝ ╚═╝  ╩  ╚═╝ ║
  ╚═════════════════════════════════╝

Active   (3)
░▒   1  ▒░    rocket-skates           │  ●  Phase 2  ·  thruster tuning next
░▒   2  ▒░    bbs-revival             │  ●  Live  ·  two new door games shipping
░▒   3  ▒░  x  zine-printer            │  ●  Phase 1  ·  blocked on toner supplier

●  good ·  ●  actionable ·  ●  pending ·  x  stale

↑/↓  move  ·  enter  open  ·  m  move  ·  1-3  jump  ·  q  quit
n  new  ·  i  import  ·  r  refresh stale  ·  a  archive
```

Those status lines aren't something you type in and forget to update - each one is an **actual judgment** of where the project stands, made by Claude reading the project's plan, decisions, and git history, then cached locally. **Green → amber → cyan** reads as resting → your move → waiting on someone, and an `x` flags a chip gone stale.

Claude Code rides along the whole way: `/setup-project` interviews you and writes a new project's docs, `/grill` pressure-tests a design one decision at a time, and `/architect` advises from the next window over.

Underneath it all is a three-folder workspace - dead-simple on purpose, so your projects outlive any tooling:

```
~/Projects/
├── Active/       engaged now - building or using
├── Inactive/     dormant but alive - paused, will resume
└── Archive/      finished work, year-prefixed, kept to read
```

## Install

### The easy way

Download [project-system.zip](https://y3klab.com/project-system.zip) (327 KB - the whole system, nothing personal of the author's inside, no account, no telemetry). Unzip it, open the folder, and double-click **“Double-Click to Install.command”**. Terminal opens, the system moves itself to `~/project-system`, the installer runs, and you land in a ready shell.

If macOS balks (“could not verify it is free of malware”, offering only *Move to Trash* / *Done*): click **Done**, open **System Settings → Privacy & Security**, scroll down to *Security*, click **Open Anyway**, then double-click the installer again - once. macOS just wants to hear you trust a script you downloaded. (Or sidestep the dialog entirely: Gatekeeper only fusses over double-clicks, so the [From the terminal](#install-terminal) route below never sees it.)

### From the terminal

Prefer to drive? Same result, three moves:

```
unzip project-system.zip -d ~
~/project-system/install.sh
exec zsh
```

The installer checks your tools, symlinks the slash commands into `~/.claude/commands/`, seeds your lexicon, creates the `~/Projects` workspace, and offers - showing the exact line - to wire the aliases into your `~/.zshrc`. It announces every path it touches and touches nothing else. Cautious? Preview every change first, writing nothing:

```
~/project-system/install.sh --dry-run
```

**Requirements:** `git` (required - the engine under the hood), [Claude Code](https://claude.com/claude-code) (for the slash commands), and a zsh-ish shell. `gh` is optional - it auto-creates GitHub remotes; skip it and paste any clone URL by hand.

## First contact

Two doorways in - both interactive, both also reachable from the dashboard's `n` and `i` keys:

```
newproject     # spin up a NEW project - scaffold, hand off to Claude
importproject  # adopt an EXISTING folder or git repo - original never touched
```

`newproject` creates your first project in `~/Projects/Active/`, drops in a starter scaffold, and hands off to Claude Code to help define what the thing actually is. Already have a pile of project folders? `importproject` is the adoption on-ramp - point it at each one and it's copied in, with the full Claude intake *offered* rather than forced. Either way the project exists the moment its folder does - there is no register step, because there is no list. Want the why behind the design? `CONVENTIONS.md` ships in the zip - the system's principles, ~850 lines.

## Uninstall

The system lives in four announced places: the `~/project-system` folder, five command symlinks, the `~/Projects` workspace, and one line in `~/.zshrc`. To remove it, delete the first two and the line:

```
rm -rf ~/project-system
rm -f ~/.claude/commands/{setup-project,grill,architect,init-claude-md,project-status}.md
# then delete the one project-system line from ~/.zshrc
```

`~/Projects` - your actual work - stays. It was never the system's; it's just folders and git repos, plus one `projects.md` that describes the workspace in plain text, all readable with or without any of this. That's the point.

---

Source: [https://y3klab.com/project-system/](https://y3klab.com/project-system/) - Y3K Lab
