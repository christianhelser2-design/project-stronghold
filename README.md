# Project Stronghold

A small foundation for consistent K–8 art lesson preparation and classroom
organization. The goal is less repeated planning and clearer next actions.

**This is a public repository. Use invented examples only.** Keep actual student
records and school operations in approved private systems. Read the
[privacy boundary](docs/privacy.md) before adding anything.

## Start here

1. Open the [lesson-readiness prompt](prompts/lesson-readiness.md) or
   [room-reset prompt](prompts/room-reset.md).
2. Try it manually with the matching file in [examples](examples/).
3. Review the result for usable steps, honest unknowns and a clear finish.
   Record an improvement only when the trial reveals a real problem.

The JSON agent profiles are **disabled configuration templates**, not installed
or running agents. No model API, account connection, scheduling or paid service is
required for this starter. This repository does not run a classroom application.

## Run the checks

Requires Git and Python 3.11 or newer. No third-party Python packages are needed.
From the repository folder:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The checks inspect candidate files,
parse Python and JSON, validate template contracts, check local Markdown links,
and flag selected private paths, links and credential patterns. Tests exercise
both valid examples and failures. They never call an AI model or school system.

GitHub Actions runs the same commands on pushes and pull requests. A green check
is evidence about these checks only; it is not a privacy guarantee or a classroom
trial. Review the diff **before** pushing: a public CI failure is already public.

## Where things belong

| Location | Purpose |
| --- | --- |
| `prompts/` | Two reusable, source-aware planning prompts |
| `agents/` | Disabled draft-only profiles pointing to those prompts |
| `config/` | Safe project defaults; no credentials or private source IDs |
| `examples/` | Wholly invented inputs, never anonymized real records |
| `docs/` | Privacy, working instructions and this starter's project record |
| `scripts/`, `tests/` | Local validation and regression checks |
| `.github/` | Validation workflow and pull-request checklist |

See the [working guide](docs/working-guide.md) for changes and recovery, and the
[project record](docs/project-record.md) for scope, evidence and the next milestone.

## Build on it carefully

The first useful step is a manual prompt trial, followed by a small revision.
Real agent execution needs a separately chosen runtime, access controls, cost
limits and tests. School integrations need approved data handling and verified
permissions. No grades, family messages, workbook synchronization, deployment or
scheduled tasks are implemented here.

No redistribution license has been selected. Public visibility alone does not
grant permission to reuse third-party curriculum, student art or private documents.
