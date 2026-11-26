# Stronghold development memory

Verified 2026-11-26. This is the short public entry point, not school records.
Check the actual branch and live pull-request state before acting on a snapshot.

## Current facts

- Stronghold is a Python/Markdown lesson-preparation starter, not a running
  classroom application. Both classroom profiles remain disabled.
- Ruflo 3.80.8 is configured and locally smoke-tested on the development branch.
  [PR 4](https://github.com/christianhelser2-design/project-stronghold/pull/4)
  was open and unmerged when checked. Main does not yet contain that setup.
- Ruflo 3.80.9 is an upgrade candidate, not the installed project pin. Hallmark is
  downloaded separately; it is not installed into this starter.
- Current implementation adds bounded recall and a 12-tool Ruflo client allowlist.
  Local validation and all 54 tests passed. Its reviewed change depends on PR 4;
  neither is claimed merged. Next: review the dependent change and hosted checks.

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
| How is Ruflo configured or removed? | [Ruflo setup](ruflo.md) |

At a verified task boundary, replace stale current facts here and append the
evidence once to the project record. Keep this index under 2,500 characters.
Operational context remains in its existing approved private system; never copy
its records or private source links into GitHub to make recall easier.
