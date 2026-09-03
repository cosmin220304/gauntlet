# Gauntlet

Fable plans and reviews. Opus 4.6 builds. You decide at three gates.

`/gauntlet:run <spec or ticket>` turns Fable into the product owner and tech lead for one feature in the current worktree. It writes a brief, splits the work only where a second engineer could take a part without stepping on the first, and spawns one `gauntlet-builder` per slice. Builders run on `claude-opus-4-6`, decide their own implementation, write their own tests, and never run them. A hook stops any builder that crosses 130k tokens of context and makes it hand off. Fable reviews and trims every diff, runs the tests itself, and ships through `/gauntlet:ship-it`.

The run stops to ask you three times:

1. Before any builder starts: what Fable understood, what is in and out, and every ambiguity it would otherwise decide alone.
2. After the builders report: does the code look right, and may it run validation and the tests.
3. With everything green: ship it?

A monitor at http://localhost:7777 shows every session and builder on this machine: what each one is doing right now, its context against the cap, how it ended (report, stopped, cap hit, compacted), and the uncommitted diff of its worktree, one file at a time.

## Install

You need the Opus 4.6 build of Claude Code, `python3`, `git`, and `gh` (for shipping).

<details>
<summary>Installing the prerequisites</summary>

Assumes you already have Node, Python 3, and a GitHub account.

Claude Code, the build that ships Opus 4.6. Always start it with this exact command; a plain `claude` may resolve to a different build:

```
npx @anthropic-ai/claude-code@2.1.81 --dangerously-skip-permissions
```

The first launch asks you to sign in.

The GitHub CLI, used only by `/gauntlet:ship-it` to push and open the PR:

```
brew install gh
gh auth login
```

</details>

From GitHub:

```
/plugin marketplace add cosmin220304/gauntlet
/plugin install gauntlet@gauntlet
```

From a local checkout, for trying it out:

```
npx @anthropic-ai/claude-code@2.1.81 --dangerously-skip-permissions --plugin-dir /path/to/gauntlet
```

## Use

```
/gauntlet:run CONNECT-487
/gauntlet:run docs/plans/einvoice-network.md
/gauntlet:run "Add e-invoice network support: onboarding flow and submit flow"
```

Answer the three gates. Fixes you ask for at gate 2 become new builder slices and come back to the same gate.

The monitor starts with the first run; open http://localhost:7777. Start it by hand with `python3 skills/run/watch.py` from the plugin directory. `GAUNTLET_WATCH_PORT` changes the port.

## Knobs

- `GAUNTLET_CONTEXT_CAP` (default `130000`): the builder context cap, read by the hook and the monitor.
- `agents/gauntlet-builder.md`: the builder's model, turn limit, and working rules.
- `commands/ship-it.md`: how a run becomes a PR. Edit the commit and PR conventions there.

## Layout

```
skills/run/SKILL.md     the orchestration playbook Fable follows
skills/run/watch.py     the monitor, one stdlib Python file
agents/gauntlet-builder.md
commands/ship-it.md
hooks/hooks.json        PreToolUse hook wiring
hooks/context-cap.py    blocks a gauntlet builder's next tool call past the cap
```
