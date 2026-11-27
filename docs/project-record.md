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

## Validator contract repair — 2026-10-21

A synthetic review found that a profile could point to the other prompt or
example, or duplicate the other profile's ID, while validation still passed.
The validator now ties each profile ID to its filename and the two supported
prompt/example pairs. It also checks private directory and filename patterns
without case sensitivity, so a capitalized `Private/` or `.ENV` path is flagged.

The same review found that staged content could differ from a safe working-tree
copy, a staged deletion or empty index could be hidden by untracked copies,
and a staged link could depend on an untracked target. A second pass now checks
staged Git blobs, file modes, required paths, contracts and links alongside
working-tree candidates.
The simple Markdown link check also handles optional titles.

Local verification: `python3 scripts/validate.py` passed; all 31 unit tests
passed, including eleven new tests for these cases. The Git regression fixtures use
only invented files in temporary directories. This is local source validation,
not a hosted check or privacy certification. The link check does not cover all
Markdown syntax or verify anchors and remote pages; review staged content and
publication text before any push.

Next: review the full staged diff, then publish this bounded repair through a
reviewed pull request and verify the hosted workflow.

## Ruflo development connection and public tutorial review — 2026-11-26

Added a project-level Codex MCP connection pinned to `ruflo@3.80.8`, using stdio
and the existing host approval and sandbox settings. This is optional repository
development tooling. It does not enable either classroom profile, connect school
accounts, schedule work or start model workers. The existing prompt paths,
synthetic examples and classroom configuration were preserved.

The first npm install failed during ONNX Runtime's Linux GPU-library download.
Inspection of Microsoft's published 1.30.0 installer showed that
`ONNXRUNTIME_NODE_INSTALL=skip` skips unbundled CUDA/TensorRT binaries while
retaining bundled CPU files. The retry succeeded. The connection sets that
option and keeps npm's cache in ignored project runtime storage. GPU and neural
execution were not tested. See [setup and removal](ruflo.md).

Verification on Linux with Node 24.22.3: the configured command completed MCP
initialization, discovered 394 tool definitions, and executed `system_info` with
the expected 3.80.8 version, project working directory, positive process ID and
supported Node version. Closing stdin stopped the server with exit status zero.
This proves a local tool call; advertised feature flags do not prove model,
memory, swarm or classroom execution.

The validator now parses only the reviewed `.codex/config.toml` shape, requires
a numeric version pin and stdio, and rejects additional host settings. Both
`.swarm/` and `.claude-flow/` are ignored and rejected if force-added. Six new
tests cover the accepted config, malformed TOML, host-setting changes, moving
version/transport changes, unreviewed TOML and forced runtime-state staging.
All 37 unit tests and the public-file validator passed locally. Review also
identified and fixed copying local runtime directories into test fixtures.

[Public Instagram findings](instagram-notes.md) link the matching district post,
a Ruflo overview and a Hallmark audit example. Retrieved captions were compared
with official documentation; cost savings and rendering prices remain unverified
promotional claims. Hallmark is a downloaded reference, not installed in this
starter, and no campus view was built.

Next: review this change through a pull request and check its hosted validation.
After merging, reopen Codex in the trusted project to load the connection and
try one synthetic lesson-readiness review. No paid model run or classroom trial
was performed. Hosted results must be verified separately from this local receipt.

## Selective development recall and toolbox review — 2026-11-26

Added a short current-state index and a dependency-free Python recall command.
The command reads only 11 named public Markdown sources on each invocation,
skips file/ancestor symlinks and oversized inputs, and returns up to three
file/line-cited excerpts within a default 4,000-character ceiling. It does not
index private workspaces, package caches, transcripts or runtime memory. The
current index is under 2,500 characters; the validator now enforces that ceiling.
Session instructions start with the short index and privacy boundary, retrieve
relevant passages, then update current facts and the existing dated record at
verified task boundaries. No background capture or new schedule was created.

The [dated toolbox review](toolbox-review.md) compares official repositories,
current release/maintenance evidence, licenses and operating costs. It identifies
QMD, MarkItDown and RTK OSS as conditional pilots, and records Ruflo 3.80.9 for
separate upgrade review. No candidate package was installed or runtime pin
changed. The existing Ruflo client configuration now selects 12 reviewed
memory/task/status tools, with regression checks for an empty, duplicate or
unreviewed tool list. This is client exposure filtering, not a sandbox or proof
of any particular host's context-token count.

Verification: all 54 Python tests passed, including 15 recall behavior checks.
The full public validator and staged whitespace check passed before publication.
The configured Ruflo 3.80.8 server again initialized, advertised 394 definitions,
contained all 12 selected names, executed `system_info` with expected project
context and shut down cleanly. No memory write, worker or model request was run.

The first retrieval trial incorrectly ranked fenced CLI examples above evidence;
regression tests now exclude fenced examples and preserve accurate source lines.
Specific probes `Ruflo installation`, `private records` and `QMD retrieval`
returned their expected source among the first three excerpts, using 1,043,
961 and 1,821 characters respectively with a 2,000-character limit. These are
character counts, not measured model-token or billing savings.
Broad `next useful tool` still retrieved generic/self-referential passages, and
`public private boundaries` ranked the privacy source third. This lexical system
needs concrete source terms; it is not semantic question answering. Revisit QMD
only if such misses justify model downloads and a maintained index.

An independent implementation review found no blocking correctness/privacy issue
and identified the broad-query limitation above. No private source link or
operational record was added to this public change. The current development
branch is based on open PR 4. Next: review the dependent pull request and its
hosted checks, then evaluate recall on the next actual development question.

## Full local toolbox and agent adoption — 2026-11-26 America/Detroit

The expanded adoption request explicitly included all reviewed memory frameworks.
PRs 4 and 5 were checked at their expected heads, with passing hosted validation,
then merged into main. The adoption change builds on that merged foundation.
The tested project runtime pin is now Ruflo 3.80.9; its actual MCP initialization,
394-name discovery, 12 selected-name check, `system_info` and clean shutdown
passed. Classroom profile templates remain disabled; explicit assistant roles
are documented separately from an unattended runtime.

All 13 local toolbox entries and their receipts are present. QMD, MarkItDown,
RTK OSS, Context7, Playwright, Caveman, both MCP memory servers, Mem0 and Graphiti
were installed in isolated local environments. Hallmark is installed as a local
Codex skill, and the Agency Agents source library is available on demand.
The [adoption record](adoption.md) gives versions, verified scopes, limitations
and the next useful workflows. Models, dependencies and synthetic stores remain
outside published source. No private records, paid model API or background
capture/sync was introduced.

Concrete results include source-preserving document conversion; local lexical
and semantic retrieval; real persistent memory/graph lifecycle checks; synthetic
browser interaction and Hallmark static/render audits; and explicit compression
with failure/recovery checks. These do not establish every optional LLM feature,
hosted service, reference MCP runtime or production outcome. Full QMD expansion
exceeded two minutes, while vector-only pilot queries took about 2.5–3.3 seconds.
The public QMD snapshot is restricted to the 13 approved Markdown paths and
requires an explicit source/index refresh after changes.

The launcher is inert for status/list, passes literal argument lists without a
shell, requires deliberate stdio startup, and never implicitly downloads a
package. It derives the Ruflo version from the project configuration. A reviewer
found a Context7 startup-marker mismatch; the guard was tightened and two
regressions passed. Fifteen launcher tests cover dispatch and no-launch cases.
Hallmark's installed payload is ignored and rejected if staged, and fixture
copying excludes that dependency. All 70 project tests passed; the public-file
validator and staged whitespace/diff checks passed before publication.

Several native workflows initially failed or hung under restricted execution;
the same bounded tests passed through the host's authorized native-process path.
The receipt distinguishes that permission issue from an upstream defect.
Doobidoo's hardcoded home-cache path required a local adapter; RTK's generic test
filter dropped assertion detail, so raw failure recovery/native quiet mode is
preferred. No global sandbox, browser policy, proxy or hook was disabled/enabled
to hide these results.

A preparation-role assistant produced the saved synthetic lesson draft. A second
assistant checked its 40-minute sum, source steps, choices, cleanup and preserved
unknowns against the original invented input. A teacher-drawn step card emerged
as a reusable demonstration/access/checkpoint aid. This is a digital example,
not classroom use or teacher approval.

Next: apply the conversion, source-hash/citation, retrieval, preparation and
independent-review path to one authorized task, then save its actual result in
the existing knowledge record. Compare memory engines on the same synthetic
questions before choosing a primary derived store; do not synchronize competing
copies automatically. Hosted publication evidence is separate from these local
checks. No production token or billing reduction is claimed.

## First real source workflow — 2026-11-26 America/Detroit

Applied the adopted tools to the official National Gallery of Art
[Claude Monet chapter](https://www.nga.gov/sites/default/files/migrate_images/content/dam/ngaweb/education/learning-resources/an-eye-for-art/aneyeforart-claudemonet.pdf)
from *An Eye for Art*. The unchanged source is 14,906,321 bytes, SHA-256
`dc16ae826402c1a7d7328a27a541f736f0f6194e1f49a93f981955d658134ecc`.
The original landing page's older size label was not used as file evidence.
Four physical pages map to an unnumbered cover and printed pages 12, 13 and 14.

MarkItDown 0.1.9 produced a retained conversion. Whole-page extraction mixed
columns, so a separate region companion was checked against all four rendered
original pages. Physical page 3 / printed 13 supports the water/bridge reflection
claims; physical page 4 / printed 14 supports the comparison and repeated-scene
activity. The source, full conversion and artwork remain outside this public
repository; source access was not treated as a whole-PDF CC0 license.

A separate local QMD index contains only that verified source companion, excluding
the draft, private workspace and default public-project corpus. Local source
queries located the checked passages; bounded original-section opening supplied
the exact activity when a semantic match instead returned background text.
This distinction preserves source evidence rather than treating retrieval scores
as answers. The existing public-project index was not changed by this source run.

An original five-minute looking routine and two-minute alternative were drafted.
An independent assistant opened the original PDF/renders and passed the factual
claims, physical/printed citations, timing sums and stated scope. The reviewed
draft hash is `29a990537a641f477895e0bf1c1633f7111715196176f95ad69b58e09eba04cb`.
Actual classroom fit, progress, display readability, standards and use remain
unverified. Resource links and operational handoff are saved in the existing
private case; no private case identifiers or classroom records are copied here.

The source protocol is now explicit in AGENTS and the working guide. For the
next source task, reuse current verified evidence; preserve/convert/retrieve only
what is needed, obtain a separate review, then update memory once. This change
adds no package, background schedule, source republication or school-record write.
Existing validation and tests were run before publication; there is no new code
behavior requiring an additional test suite. No production token-saving figure
or classroom outcome is claimed.

## On-demand briefing and Hermes adoption — 2026-11-26 America/Detroit

Implemented `scripts/briefing.py` for one explicit, cited JSON snapshot. It renders
Now / Next / Blocked / Sources with observed/proposed/unverified labels and
inspection dates. The 2,000-character default includes formatting and citations;
an over-budget result fails without partial stdout, dropped blockers or clipped
source references. Input is bounded to 64 KiB during reading. Duplicate keys,
invalid references, unsafe locations and future/offset-less dates fail; inspection
age over seven days is flagged without claiming current operational progress.

The formatter has no account lookup, source fetching, model call or state write.
`docs/briefing.md` documents source assembly and a separate revision/hash receipt.
The wholly invented `examples/briefing.synthetic.json` has a narrowly registered
synthetic-only validator contract; unknown JSON contracts remain rejected. The
explicit recall allowlist adds only the new guide, bringing it to 14 named public
Markdown paths. Existing classroom profiles remain disabled. The coordinator and
content-drafter paths use approved sources and private drafts, with no publishing
or scheduling action.

The first real private briefing used the existing reviewed Monet handoff and
preserved NGA chapter. Its complete output is 942 characters, with clickable
source citations and an explicit proposed display/time check. The source PDF,
draft and review still match their recorded hashes. Independent comparison passed
the facts and status labels; classroom use, readability, fit and current stopping
points remain unverified. The actual snapshot, source block hashes, output and
saved briefing view stay outside this public repository.

Installed the MIT Hermes Agent release v0.23.4 at commit `8fc037444731` in its
separate local toolbox. Its PM-managed Python 3.14.9 environment, 66 Python
distributions, required toolchain and exact lock/artifact hashes are recorded in
the local adoption receipt. The core installation excludes browser/computer-use
extras and occupies about 1.8 GiB. Genuine version/help, a restricted inspection
wrapper, MemoryStore add/reload/patch/remove and SQLite FTS5/session-search
lifecycle passed on a small approved public fixture; deletion was verified.
No local model endpoint was found, so model-backed assistant execution remains
unconfigured. The toolbox entry permits only `--status`, `--version` and `--help`;
profiles and this argument guard are not filesystem sandboxes.

All 102 existing/new unit tests passed, including 25 briefing tests, 44 validator
tests and 18 toolbox tests. Independent review found a clickable-link authority
delimiter defect; a regression now rejects malformed authority/IDNA forms while
retaining valid IPv6/ports. Public-data validation and complete staged review are
required before publication. The next useful step is an on-demand briefing from
the named records; real Hermes inference needs a configured provider and a
separate verified task. No measured token/billing savings or unattended operation
is claimed.
