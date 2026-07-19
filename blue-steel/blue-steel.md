# Blue Steel

A really, really, **ridiculously good-looking** terminal. A free theme + live status bar for **Claude Code** — two small files, one minute to install, instantly reversible.

## What you get

The whole look, in one frame: the steel-blue block behind everything *you* type — your words never lost in the scroll — the live spinner, and the status bar pinned beneath it all, answering the question every multi-window session asks — **“which project is this?”** — with your project name in the synthwave magenta→cyan gradient of A3K, the Y3K Lab design language:

```
        
          ❯ claude 
          ❯  make this terminal *ridiculously good-looking* and put a blue-steel color behind everything I type so my words will stand apart from yours at a glance
          
●  I'll put every word you type on the
            blue-steel block and leave mine on bare steel — one glance and you'll always
            know who said what, even 10,000 lines deep in the scrollback buffer.
          
        
        [  your-project  ]   context  ▄42%  |  5h limit  85%  |  7d limit  60%   |  session  4h20m   |  Fable 5  
      
```

The percentage gauges — context-window usage and your five-hour and seven-day rate limits — colour themselves **green → amber → red** as they fill, so the colour *is* the warning. Session time and the active model ride along. Each gauge appears only once it has a value — and in a narrow terminal the bar sheds its quietest gauges first rather than overflow. (The demo above does the same: resize this window and watch.)

### The theme

Dark steel base, synthwave accents — your words on a steel-blue block, themed diffs, borders, spinners.

### Status bar

Gradient name + live gauges, pinned under the scroll (optional). One small shell script.

## Install

### One command

Paste this into your terminal:

```
curl -fsSL https://y3klab.com/blue-steel/install.sh | bash
```

The installer announces every file it touches, backs up your `settings.json` before merging in the three keys it needs, and touches nothing else. Piping a stranger's script into your shell deserves suspicion — [read it first](https://y3klab.com/install.sh); half of it is the uninstaller and the banner art. Then restart Claude Code and you're done.

### By hand

Prefer to place things yourself? Same result. Download [blue-steel-kit.zip](https://y3klab.com/blue-steel-kit.zip) (5 KB — the status bar script, the theme, and a README with these same instructions). Unzip it, then from that folder, copy the two files into place:

```
mkdir -p ~/.claude/themes
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
cp blue-steel.json ~/.claude/themes/blue-steel.json
```

Merge this into `~/.claude/settings.json` (create the file if it doesn't exist):

```
{
  "statusLine" : {
    "type" : "command" ,
    "command" : "~/.claude/statusline.sh" 
  },
  "tui" : "fullscreen" ,
  "theme" : "custom:blue-steel" 
}
```

Restart Claude Code. Done — the bar fills in as the session runs.

**Requirements:** the gauges need `jq`, which is built into macOS 15 and later; on anything older, `brew install jq` (without it you still get the gradient name, just no meters). Custom themes need a current Claude Code. Prefer the bar to ride along with the conversation instead of staying pinned at the bottom? Skip the `"tui"` line.

## Update

**Updating is the install command, run again** — it fetches the latest files over the old ones and leaves your settings alone:

```
curl -fsSL https://y3klab.com/blue-steel/install.sh | bash
```

Installed by hand from the zip? Same idea: download the current [kit](https://y3klab.com/blue-steel-kit.zip) and re-copy the two files — they're the only things that change. Either way, restart Claude Code to pick it up. There's no auto-update and no version to track; when you hear Blue Steel got better, this is the whole ritual.

## Uninstall

Blue Steel touches exactly two files and three settings keys — nothing else, no background processes, no other state. One command removes all of it:

```
curl -fsSL https://y3klab.com/blue-steel/install.sh | bash -s -- --uninstall
```

Restart Claude Code and you're back to stock. (By hand: delete the two files and remove the three keys from `~/.claude/settings.json` — that's everything the installer did.)

---

Source: [https://y3klab.com/blue-steel/](https://y3klab.com/blue-steel/) — Y3K Lab
