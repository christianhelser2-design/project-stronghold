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
```

The local default root is the sibling `toolbox/` directory beside this checkout.
Set `STRONGHOLD_TOOLBOX_ROOT` to relocate it. `status` reports file/receipt presence,
not runtime health; it starts nothing. `run` uses installed executable paths and
literal arguments, with no implicit package download. SDK entries launch their
isolated Python interpreter; reference libraries remain source material.
Registered server entries require the explicit `--start` action; the Ruflo CLI
uses explicit `mcp start` arguments. Host execution permissions still apply;
this launcher is not a file/network sandbox.

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
