# Stronghold starter: scope and implementation record

## Objective and acceptance

Build one small public foundation for repeatable K–8 lesson preparation and
classroom organization. Keep current lessons and school records in their approved
private systems. This repository holds reusable methods and wholly invented examples.

Done means: readable instructions, two bounded draft-only agent templates, safe
configuration examples, a local validator with negative tests, and a GitHub workflow.
Publication and hosted test results must be verified separately from local tests.

## Design

- Python 3.11+ standard library; no package install, model subscription or API key.
- Markdown prompts are usable manually. JSON profiles describe future agents;
  they do not launch anything or grant permission.
- One source for each prompt; agent profiles point to it instead of copying it.
- Local and hosted checks use the same two commands:
  `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`.
- Simple Python functions, descriptive names, four-space indentation. Errors name
  a file and problem category, never echo a suspected secret or record.
- No app build, deployment, database, external integration or telemetry in scope.

## Work plan and owners

This is the public development record for this starter, not a replacement for
private Stronghold operational tracking. Owners below are responsibilities,
not claims that staff or background agents are running.

| Milestone | Owner | Depends on | Success measure | Status |
| --- | --- | --- | --- | --- |
| Scope and privacy boundary | Maintainer | Repository access | Public/private split documented | Defined |
| Prompts, profiles, examples | Implementer | Scope | Two complete manual-use paths | Implemented |
| Validation and regression tests | Implementer | Examples | Good input passes; unsafe/broken fixtures fail | Locally verified |
| Repository publication | Maintainer | Local review and passing tests | Exact published files verified | Pending |

Target: this starter task. No classroom date or ongoing maintenance commitment is
assigned. Work order: finish one milestone, verify it, then continue.

## Test scope

Use disposable, fictional fixtures for invalid JSON, missing fields, broken prompt
references, unsafe settings, credential-like strings, private links, symlinks,
and accidentally tracked private files. Review prose for identifying context;
pattern matching cannot prove that prose is anonymous. Test the actual GitHub
workflow after publication when available.

## Boundaries and next milestone

Always preserve original work, use synthetic fixtures, inspect staged diffs and
record actual results. Obtain specific authorization before sending messages,
changing grades, spending money, adding sensitive integrations or scheduling work.
Never place private records, credentials or exported school documents here.

Next proposed milestone: try the lesson-readiness prompt manually with one invented
lesson, then revise only a demonstrated problem. A real classroom pilot requires
verified current pacing, materials, access and teacher review in approved private
storage. Its timing is not scheduled.

Defer model runtimes, automatic messages, grading, workbook imports, app/campus
rebuilds and extra departments. Integration access, district storage approval and
runtime choices are unresolved; this starter does not settle them.

## Local verification receipt — 2026-10-18

- Environment: Linux, Python 3.12.14, Git; no third-party Python dependencies.
- Starter validation passed; 20 behavior tests passed, including CLI failure status,
  forced private-file staging, duplicate JSON keys and links to ignored local files.
- The ignored-file link test failed before its fix, then passed after publication
  membership was checked. Negative fixtures are generated only in temporary folders.
- Reviewed source, examples, docs and workflow for scope and private content;
  checked whitespace with `git diff --cached --check`. No private workbook was imported.
- This is author review and local execution, not an independent security audit,
  an AI output evaluation, a classroom trial or hosted CI evidence.
- Hosted publication and validation: pending; record verified results after upload.
- Repository rulesets were empty when inspected. Required-check enforcement and
  branch protection are not configured by this starter.
