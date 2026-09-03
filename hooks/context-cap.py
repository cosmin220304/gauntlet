#!/usr/bin/env python3
"""PreToolUse hook: blocks a gauntlet subagent's next tool call once its context passes the cap."""
import json, os, sys

CAP = int(os.environ.get("GAUNTLET_CONTEXT_CAP", "130000"))

hook = json.load(sys.stdin)
if not str(hook.get("agent_type", "")).startswith("gauntlet-"):
    sys.exit(0)

path = os.path.join(
    os.path.dirname(hook["transcript_path"]),
    hook["session_id"], "subagents", f"agent-{hook['agent_id']}.jsonl",
)
if not os.path.exists(path):
    sys.exit(0)

usage = {}
with open(path) as f:
    for line in f:
        d = json.loads(line)
        if d.get("type") == "assistant" and "usage" in d.get("message", {}):
            usage = d["message"]["usage"]

context = usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
if context < CAP:
    sys.exit(0)

print(
    f"CONTEXT CAP REACHED: your context is {context} tokens, cap is {CAP}. "
    "Make no more tool calls. Reply now with your report, Status: SPLIT, "
    "and a precise handoff of what is done and what remains.",
    file=sys.stderr,
)
sys.exit(2)
