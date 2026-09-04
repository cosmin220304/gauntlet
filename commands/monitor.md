---
description: Start the gauntlet monitor if it is not running, register this session with a checkout, and open http://localhost:7777
allowed-tools: Bash
---

Run these, then tell the user the monitor is at http://localhost:7777:

```
lsof -i :7777 >/dev/null 2>&1 || (python3 "${CLAUDE_PLUGIN_ROOT}/skills/run/watch.py" >/dev/null 2>&1 &)
python3 "${CLAUDE_PLUGIN_ROOT}/skills/run/watch.py" --register "$CLAUDE_CODE_SESSION_ID" "${ARGUMENTS:-$PWD}"
open http://localhost:7777 2>/dev/null || xdg-open http://localhost:7777 2>/dev/null || true
```

If the user gave a path as the argument, that path is the checkout the monitor diffs for this session. Otherwise it is the current directory. A name given earlier by `/gauntlet:run` is kept.

If the port is busy but the page does not load, something else owns port 7777. Say so and stop.
