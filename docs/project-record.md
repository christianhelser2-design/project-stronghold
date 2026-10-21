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
| Repository publication | Maintainer | Local review and passing tests | Exact published files verified | Published in PR #1; hosted checks passed |

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
- Hosted publication and validation are recorded below.
- Repository rulesets were empty when inspected. Required-check enforcement and
  branch protection are not configured by this starter.

## Publication receipt — 2026-10-18

- Candidate commit: `d396aeae319c314647d9fc8b3192b5cfd128aeab`.
- All 17 remote file paths, modes and Git blob hashes matched the tested local files.
- Both push and pull-request workflows completed successfully. The hosted job
  passed Python-version verification, starter validation and the behavior tests.
- [Verified pull-request run](https://github.com/christianhelser2-design/project-stronghold/actions/runs/39157489262).
- This receipt is a documentation-only follow-up to that tested candidate.
  [Pull request #1](https://github.com/christianhelser2-design/project-stronghold/pull/1)
  holds the final merge state; [Actions](https://github.com/christianhelser2-design/project-stronghold/actions)
  holds subsequent checks. Do not treat the earlier run as a test of later edits.

The remaining configuration is agent/runtime selection and enforcement, approved
private-source access, any intentionally scheduled work, and mandatory branch checks.
No schedule, integration, classroom application or live agent was created.

## Supervised public research trial — 2026-10-21

The existing lesson-readiness prompt now has an optional, one-question public
source check for visual references, standards and material facts. The working guide
specifies a manual Firecrawl-assisted path: publisher search, direct page check,
dated claim, unresolved condition and teacher decision. No API key, runtime, agent
tool permission, account integration or recurring monitor was added.

One-time live checks of [The Met's image FAQ](https://www.metmuseum.org/policies/frequently-asked-questions-image-and-data-resources),
its [individual Hokusai object record](https://collectionapi.metmuseum.org/public/collection/v1/objects/45434),
and [NAEF's grant page](https://www.arteducators.org/events-and-opportunities/naef-grants/)
showed why broad search snippets need object-level rights and current-cycle checks.
The object record explicitly reported `isPublicDomain: true` and a `primaryImage`;
the public collection page's extracted text alone did not expose that specific flag.
A separate [fullscreen API page](https://developer.mozilla.org/en-US/docs/Web/API/Element/requestFullscreen)
surfaced transient user activation, iframe permission and rejected promises as
debugging leads; the [dedicated policy page](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy/fullscreen)
clarified that `fullscreen` has a default `self` allowlist. There is no camera app
in this repository, so these are research leads, not a tested repair.

Manual synthetic trial: using `examples/lesson.synthetic.json`, a draft labeled
readiness **needs preparation** because stock, class size and current pacing are
unknown. It proposed a 40-minute flow (entry 4, demonstration 5, making 21,
checkpoint 4, cleanup 6), left the standard unverified, and named a teacher-drawn
curved-line example as a fallback. The candidate Hokusai reference was tied to
the dated individual object record's `isPublicDomain` flag; no image was copied
into the repository. This checks the prompt's source handling, not classroom use.

Next: have the teacher review a real candidate visual and actual section readiness
in approved private storage before using either in class. A teacher must verify
classroom readiness and any use of the image separately.

Local verification: `python3 scripts/validate.py` passed; all 20 unit tests
passed; `git diff --cached --check` passed and the full staged diff was reviewed.
These checks do not evaluate the quality of an AI lesson draft or prove live
classroom use.
