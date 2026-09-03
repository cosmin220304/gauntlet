---
description: Commit, push, and open a PR with a concise commit message and description
allowed-tools: Bash(git:*), Bash(gh:*)
---

Ship the current work as a PR:

1. Run `git status` and `git diff` (and `git log origin/HEAD..HEAD` if commits exist) to understand what changed.
2. If on the default branch, create a descriptive branch first.
3. Stage and commit the changes with a **concise** commit message: a single short imperative subject line (< 60 chars), no body unless a one-line "why" is genuinely needed. No filler. Never add a `Co-Authored-By: Claude` trailer or any AI attribution.
4. Push the branch with `-u`.
5. Create the PR with `gh pr create` (title = the commit subject). If a PR already exists for the branch, update its description via `gh api -X PATCH /repos/{owner}/{repo}/pulls/{number} -F body=@<file>` (never `gh pr edit` — it fails on a missing `read:org` scope).
6. Output the PR URL.

## PR description format

Succinct, plain English, written like a human — readable by someone with zero context. Total length well under a screen. Shape:

```markdown
## Summary

<1-2 sentences: what this does and why it matters, in plain words. No jargon dumps.>

<ticket link on its own line, if the branch name carries a ticket ID>

## What it does

- **Bold anchor** then a short plain-English clause.
- <2-4 bullets max; only include this section when the change has more than one moving part>

<one-line footnotes if load-bearing, e.g. "Supersedes #NNNN; no DB or REST changes.">
```

Rules:

- Cut anything a reviewer learns by scrolling the diff. No file-by-file narration, no test plans, no checklists, no architecture essays, no forced headings.
- No `## Rollback` section. Mention a back-out step in a footnote only when a plain revert won't restore old behavior (migrations, flags, data written in the new shape).
- No AI attribution anywhere — no "Generated with Claude Code" footer.

If there's nothing to commit but unpushed commits exist, skip to pushing and creating the PR.

Additional user input: $ARGUMENTS
