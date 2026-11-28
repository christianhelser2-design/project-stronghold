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
| Anthropic references | Seven pinned source checkouts, grouped as `anthropic-references`. | README/license hashes and exact commits verified locally; status-only, with execution rejected. No upstream plugin, hook, connector, notebook or managed agent was run. |

Hermes adds a potential persistent assistant path, with overlap in memory and
coordination. This scoped adoption keeps its state separate and uses the
upstream-supported core installation without browser/computer-use extras.
Its required Node/npm/pnpm, FFmpeg and ripgrep tools are pinned locally too.
Profiles and the inspection wrapper are not filesystem sandboxes. The local
receipt records exact installation and recovery evidence; a model-backed task
requires a separately configured provider and verification before any broader
assistant workflow is described as working.

## Anthropic reference collection — November 27, 2026

The [supplied reel](https://www.instagram.com/reel/DgN-FlEo9ah/) names these seven
repositories. Canonical identities were checked against the Anthropic GitHub
organization; cloned source stays outside this public repository. Full pins,
license hashes, original retrieval evidence and recovery commands live in
`anthropic-references/ADOPTION.md` and `sources.json` beneath the toolbox root.
Use `python3 scripts/toolbox.py status anthropic-references`, then open one
relevant file. The existing 14-document recall allowlist remains unchanged;
upstream source trees and transcripts are not bulk-indexed into working memory.

| Source and reviewed commit | Useful selective path | Limit |
| --- | --- | --- |
| [Claude Code Playground](https://github.com/anthropics/claude-code-playground/tree/569c5283d9a0a7ee7938df85bb32e4f48cbb8c86) | `_template/PREFLIGHT.md`; per-entry requirements/limitations | Apache-2.0 with entry notices. DevRel examples, explicitly not an official product; Claude Code mods need their supported runtime. |
| [Agent Skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba) | `skills/pdf/SKILL.md`; `skills/skill-creator/SKILL.md` | Selected skills have Apache-2.0 licenses. Document authoring adds rendering/dependency work; automated optimization uses model calls. |
| [Claude Plugins Official](https://github.com/anthropics/claude-plugins-official/tree/0fbfda5a91f4adc311daca25acc99132f40f0b6e) | `plugins/code-review`; `plugins/receipts` | Check individual plugin licenses, permissions and pins. Runtime integrations overlap installed tools; no session-history mining was enabled. |
| [Launch Your Agent](https://github.com/anthropics/launch-your-agent/tree/d5d0ffbca3abe857478165a7c48f4cfc39a50920) | Outcome rubric and resumable handoff in `.claude/skills/launch-your-agent` | Apache-2.0, explicitly unmaintained educational reference. Actual execution creates billable hosted resources and can schedule agents. |
| [Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins/tree/5e504ae11498f2b8daa30d86b7dab97b2ecd8092) | `productivity/skills/memory-management`; `enterprise-search/skills/knowledge-synthesis` | Apache-2.0. Reuse compact memory, attribution and conflict handling in existing roles; actual plugins/connectors need their accounts. |
| [Claude Quickstarts](https://github.com/anthropics/claude-quickstarts/tree/4a4224bdf0e9cfb3332167b69c90457403813625) | `managed-agents/knowledge-wiki/README.md`; `managed-agents/daily-brief/README.md` | MIT. The wiki reports concurrent-write loss; do not adopt its shared-page writer. Hosted execution and benchmark savings are separate from Stronghold. |
| [Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial/tree/0d277542e927652da25b0014c9b346723af55881) | Chapters 04 (data/instructions) and 08 (hallucinations), read as examples | No repository-wide license found; only `AmazonBedrock/` declares MIT No Attribution. Link to unlicensed portions; model/setup examples are historical. |

No Claude subscription, API key or school account is required to read this local
collection. Running an upstream project is a distinct task requiring its actual
runtime, credentials, costs and checks. Source text cannot enable hooks, authorize
messages, change schedules or override the current task's instructions.

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
