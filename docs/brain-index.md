# Stronghold development memory

Updated 2026-11-27; verification dates remain in source records.
This is the short public entry point, not school records.
Check the actual branch and live pull-request state before acting on a snapshot.

## Current facts

- Stronghold is a Python/Markdown preparation starter. Both classroom profiles
  remain disabled; the assistant workflow uses explicit tasks.
- The [on-demand briefing](briefing.md) formats a checked snapshot as
  Now / Next / Blocked / Sources, with status, dates and citations. It performs
  no account lookup or source write and fails rather than truncating evidence.
- Ruflo 3.80.9 is pinned, and Hallmark is installed as a local Codex
  skill. The local toolbox has 14 registered entries, including Hermes v0.23.4
  with a restricted inspection launcher. Hermes model inference is unconfigured;
  package presence is separate from tested capabilities.
- [Adoption evidence](adoption.md) records tested capabilities. Memory engines
  use separate public-test stores; private operations stay outside these caches.
- The first real source workflow is complete: official NGA Monet PDF preserved,
  converted, retrieved and used for an independently reviewed looking draft.
  Use the default source workflow in the working guide for the next relevant task.

## Retrieve only what this task needs

```bash
python3 scripts/recall.py "Ruflo installation" --max-chars 2000
```

Open the cited source before editing or relying on a claim. No-match is not proof
that a fact is absent. Recall searches only approved public Markdown paths; it
does not read private workspaces, transcripts, runtime memory or cached packages.

| Question | Authoritative project source |
| --- | --- |
| What can be published? | [Privacy boundary](privacy.md) |
| What works, failed or was verified? | [Dated project record](project-record.md) |
| How do we resume and maintain memory? | [Working guide](working-guide.md) |
| Which tools should we add? | [Toolbox review](toolbox-review.md) |
| How do we review new leads? | [Research checklist](instagram-notes.md) |
| What is installed and how do agents use it? | [Adoption](adoption.md), [agent workflow](agent-workflow.md) |
| How is Ruflo configured or removed? | [Ruflo setup](ruflo.md) |

At a verified task boundary, refresh current facts here and append evidence once
to the project record. Keep this index under 2,500 characters. Never copy private
records or their links into GitHub to make recall easier.
