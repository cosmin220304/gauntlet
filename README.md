# Gauntlet

Fable plans and reviews. Opus 4.6 builds. You decide at three gates.

`/gauntlet:run <spec or ticket>` turns Fable into the product owner for one feature in the current worktree. It writes a brief that says what and why, splits the work only where a second engineer could take a part without stepping on the first, and spawns one `gauntlet-builder` per slice. Builders run on `claude-opus-4-6`. They explore the code, choose their own files, names and steps, write their own tests, and never run them. Fable never tells a builder how to build. A hook stops any builder that crosses 130k tokens of context and makes it hand off. Fable checks every diff for business sense, runs the tests itself, and ships through `/gauntlet:ship-it`.

The run stops to ask you three times:

1. Before any builder starts: what Fable understood, what is in and out, and every ambiguity it would otherwise decide alone.
2. After the builders report: does the code look right, and may it run validation and the tests.
3. With everything green: ship it?

A monitor at http://localhost:7777 shows every session and builder on this machine: what each one is doing right now, its context against the cap, how it ended (report, stopped, cap hit, compacted), and the uncommitted diff of its worktree, one file at a time.

## Install

You need Claude Code with access to `claude-opus-4-6`, `python3`, `git`, and `gh` for shipping.

Inside Claude Code:

```
/plugin marketplace add cosmin220304/gauntlet
/plugin install gauntlet@gauntlet
```

From a local checkout, for trying it out:

```
claude --dangerously-skip-permissions --plugin-dir /path/to/gauntlet
```

## Use

```
/gauntlet:run SHOP-142
/gauntlet:run docs/plans/payment-provider.md
/gauntlet:run "Add a second payment provider: checkout flow and refund flow"
```

Answer the three gates. Fixes you ask for at gate 2 become new builder slices and come back to the same gate.

The first run starts the monitor if nothing is listening on port 7777 and registers the session with its checkout; open http://localhost:7777. It shows the latest registered run, under its checkout, and diffs that checkout, so a run started on main that moves into a worktree shows that worktree. It reads local transcripts under `~/.claude/projects` and sends nothing anywhere. The Changes tab loads its diff viewer from a CDN, so it needs internet access in the browser.

If the monitor is not up, or you want this session diffed against another checkout, run `/gauntlet:monitor` or `/gauntlet:monitor /path/to/worktree`. It starts the monitor if needed, registers the session, and opens the page.

## Knobs

- `GAUNTLET_CONTEXT_CAP` (default `130000`): the builder context cap, read by the hook and the monitor.
- `agents/gauntlet-builder.md`: the builder's model, turn limit, and working rules.
- `commands/ship-it.md`: how a run becomes a PR. Edit the commit and PR conventions there.

## Output style

The plugin ships a "Simple language" output style and forces it on while the plugin is enabled: Simplified Technical English, active voice, one idea per sentence, bullets over paragraphs. It applies to every conversation, not only gauntlet runs. Disable the plugin to get your own style back, or edit `output-styles/simple-language.md` and drop the `force-for-plugin` line to make it optional.

## Layout

```
skills/run/SKILL.md     the orchestration playbook Fable follows
skills/run/watch.py     the monitor, one stdlib Python file
agents/gauntlet-builder.md
commands/ship-it.md
commands/monitor.md     start the monitor, register this session, open the page
hooks/hooks.json        PreToolUse hook wiring
hooks/context-cap.py    blocks a gauntlet builder's next tool call past the cap
output-styles/simple-language.md
```
