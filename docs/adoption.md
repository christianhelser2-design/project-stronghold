# Installed toolbox and viable next paths

The reviewed toolbox is now installed locally for explicit, on-demand use.
The earlier [toolbox review](toolbox-review.md) remains dated research; this
execution record supersedes its defer/install decisions under the expanded
adoption request. Canonical development facts remain Markdown, and operational
context remains in its approved private system. The memory engines below have
separate stores; none is automatically fed the Workroom or school records.

## Entry point

```bash
python3 scripts/toolbox.py status
python3 scripts/toolbox.py run qmd --version
python3 scripts/toolbox.py run markitdown --version
python3 scripts/toolbox.py run rtk --version
python3 scripts/toolbox.py run hermes --status
```

The local default root is the sibling `toolbox/` directory beside this checkout.
Set `STRONGHOLD_TOOLBOX_ROOT` to relocate it. `status` reports file/receipt presence,
not runtime health; it starts nothing. `run` uses installed executable paths and
literal arguments, with no implicit package download. SDK entries launch their
isolated Python interpreter; reference libraries remain source material.
Registered server entries require the explicit `--start` action; the Ruflo CLI
uses explicit `mcp start` arguments. Host execution permissions still apply;
this launcher is not a file/network sandbox.

The Hermes pilot is registered separately as a manual inspection entry. Its only
accepted actions are exactly `--status`, `--version` and `--help`; the local
wrapper checks its source pin and lock before the genuine version command.
Chat, model setup, imports, gateways and scheduled jobs are outside this route.

Each tool has an `ADOPTION.md` receipt in its local directory with pinned versions,
source/license evidence, exact setup/start commands, fixtures and limits.
Package files, model weights, caches and local stores are not committed here.
On a fresh machine, restore the pinned packages using those receipts and rerun
their checks; repository checkout alone does not install them.

## Adopted inventory

| Tool | Local installation | Verified scope |
| --- | --- | --- |
| Ruflo | Project-pinned 3.80.9 MCP runtime; 12 client-selected tools. | Read-only MCP initialization, selected-name discovery and `system_info`; worker/model execution remains separate. |
| Hallmark | Project-local Codex skill from commit `04977e1`, plus local Puppeteer/Chromium path. | Theme/reference validation and the synthetic static/browser audit receipt. No public interface was redesigned. |
| Agency Agents | Complete MIT role-library checkout `8ae6164`; loaded selectively. | Mapped source/review/handoff roles exist; prompt files are not running workers. |
| QMD | `@tobilu/qmd` 2.9.0 with local CPU models. | Source revision/deletion, bounded citations and a local semantic paraphrase pilot. Full expansion/rerank is a slower optional mode, not the default. |
| MarkItDown | 0.1.9 with PDF/DOCX/PPTX extras in its own environment. | Invented text/table conversions, source/output hashes and physical-PDF-page companion. OCR, audio and cloud/LLM conversion are separate. |
| RTK OSS | 1.2.1 Apache-only artifact, verified digest/license. | Exit codes and local full-output recovery; generic filtering loses unittest assertion detail. Prefer native quiet tests or the failure-restoring wrapper. |
| Context7 | MCP 4.9.0, local wrapper, OTEL disabled. | Initialize/two-tool discovery and clean shutdown; hosted documentation retrieval was not exercised. |
| Playwright | CLI 0.1.25, Test 1.65.1, local skill and browser binaries. | Synthetic input/button/status flow and CLI open/close. No school site, login or live application was tested. |
| Caveman | CLI/companions 4.2.0 plus 22 local skills; signatures checked. | Explicit synthetic compression, failing exit/marker preservation and exact content recovery under native execution permission. Hooks/proxy/automatic capture are off. |
| Official MCP memory | `@modelcontextprotocol/server-memory` 2.2.1 with a persistent local JSONL path. | Real entity/observation lifecycle and deletion surviving restart. Source citations and freshness still require explicit metadata/workflow. |
| MCP memory service | 13.0.0 SQLite/ONNX environment and a localized model cache. | Real local embedding initialization and storage lifecycle as recorded in its receipt; hash fallback disabled. |
| Mem0 | `mem0ai` 2.2.1, FastEmbed 0.9.1 and local Qdrant. | Add/get/semantic-search/reopen/update/delete with `infer=False`, no LLM request. Automatic inference/extraction needs separate model setup. |
| Graphiti | `graphiti-core` 0.32.1, embedded Relate 1.0.1 and reference MCP source. | Persistent graph-driver health/create/read/update/delete under native process permission. LLM-driven episode extraction and reference-MCP authentication are not established by that test. |
| Hermes Agent | MIT [v0.23.4](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.4), commit `8fc037444731`, isolated PM-managed Python 3.14.9 and core dependency lock. | Genuine CLI version, restricted wrapper, local MemoryStore lifecycle and SQLite FTS5/session search passed on an approved public fixture, removed afterward. No local model endpoint was found; model-backed assistant execution remains unconfigured. |

Hermes adds a potential persistent assistant path, with overlap in memory and
coordination. This scoped adoption keeps its state separate and uses the
upstream-supported core installation without browser/computer-use extras.
Its required Node/npm/pnpm, FFmpeg and ripgrep tools are pinned locally too.
Profiles and the inspection wrapper are not filesystem sandboxes. The local
receipt records exact installation and recovery evidence; a model-backed task
requires a separately configured provider and verification before any broader
assistant workflow is described as working.

## Approved research and reference sources — 2026-11-27

All five sources below are adopted for the named research roles. They are
reference sources, separate from the installed-tool inventory above. Consult the
relevant source for a concrete task, then use the [research checklist](instagram-notes.md)
and [existing source workflow](working-guide.md#default-source-workflow).

1. **Promptfoo — prompt evaluation methods.** Start with its
   [introduction](https://www.promptfoo.dev/docs/intro/) and
   [assertions guide](https://www.promptfoo.dev/docs/configuration/expected-outputs/).
   For a proposed prompt revision, choose an existing synthetic input, write
   expected checks for citations, preserved unknowns and usable next actions,
   compare old/new outputs, and record failures plus independent review. The
   method can be used manually; this adoption does not install its evaluator.
2. **Hugging Face — model and demonstration discovery.** Use
   [model cards](https://huggingface.co/docs/hub/model-cards) to inspect a candidate's
   revision, license, intended uses, limitations, evaluation evidence and resource
   needs before a model trial. Inspect a [Space](https://huggingface.co/docs/hub/spaces-overview)
   and its source as a discovery lead; verify its publisher, hosting requirements,
   current plan terms and data handling before any synthetic demonstration.
   Listing on the Hub does not establish school suitability or permission to reuse.
3. **n8n templates — workflow design references.** Find a relevant example in the
   [template library](https://n8n.io/workflows), trace its trigger, nodes, credentials,
   data destinations and failure path, then write the manual equivalent for one
   bounded task. Check required nodes and dependencies against the current
   [Community Edition features](https://docs.n8n.io/deploy/host-n8n/community-edition-features/).
   Review the workflow definition before any import; a template is not a running,
   tested or approved school integration.
4. **Codeberg — free-software source discovery.** Use its
   [purpose and scope](https://docs.codeberg.org/getting-started/what-is-codeberg/)
   and [FAQ](https://docs.codeberg.org/getting-started/faq/) to find suitable public
   software references. For one candidate, inspect its license, maintained revision,
   dependencies and issue/release history; compare the demonstrated gap with the
   existing toolbox before proposing reuse. Adoption is a research route and does
   not move or mirror the working repository.
5. **GitLab Education — instructional resources and conditional program research.**
   Read the [official program requirements](https://about.gitlab.com/solutions/education/join/)
   when evaluating a teaching or noncommercial-research use. Document institution,
   age and intended-use eligibility before an application; the education license
   excludes running or administering the institution. Current SaaS requirements
   exclude institutions enrolling students under 13. Reference adoption does not
   establish eligibility, obtain a license or authorize administrative use.

Capture the chosen source URL, revision/version, date checked and decisive passage
in the existing task receipt; recheck changeable plan and eligibility conditions
when used. Public demonstrations use public or wholly fictional inputs;
authorized private tests remain in approved private stores. Implementations need
a concrete task scope, current access and data requirements, and verified results.
Apply existing authorization and approval rules; reference adoption alone is not
execution.

## Useful paths forward

1. **Convert once, retrieve selectively.** For an approved public guide, preserve
   the original and hash, convert with MarkItDown, inspect tables/page markers,
   and register only reviewed text in a scoped QMD collection. Retrieve a few
   cited passages rather than repeatedly attaching whole documents. Keep private
   material in its existing authorized source/search boundary.
2. **Use the preparation/review handoff.** Follow the
   [agent workflow](agent-workflow.md). The saved synthetic lesson draft provides
   a concrete example; actual section readiness still needs teacher evidence.
3. **Compare engines before choosing a primary derived store.** Keep Mem0,
   Graphiti and both MCP memory stores separate. Test current facts, correction,
   deletion, restart, citations and latency on the same invented fixture. Do not
   create competing automatic copies of decisions or chat transcripts.
4. **Gate compression on preserved evidence.** RTK's lost assertion detail and
   Caveman's exact-recovery test show why exit status, failure markers and a full
   recoverable source matter. Explicit filters come before any automatic hook.
5. **Make the next interface task testable.** Use Playwright for a named synthetic
   flow, then Hallmark for a named visual audit. Context7 can supply the exact
   version's library documentation when a concrete implementation needs it.

Native execution restrictions initially made several child-process, SQLite and
embedded-driver checks fail or hang; the same bounded synthetic checks passed
with the host's native process permission. Record the real permission requirement
instead of diagnosing an upstream bug from that symptom alone. No host sandbox
or browser policy was disabled.

No production token/billing savings or end-to-end classroom outcome is claimed.
Local model download/indexing and CPU latency also count as operating costs.
