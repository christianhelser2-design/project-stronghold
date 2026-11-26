# Toolbox review — 2026-11-26

Use the existing connected GitHub, research and browser tools, plus small
source-linked records. Add a package when a demonstrated retrieval, conversion
or testing gap earns its maintenance cost. This review installed no new package.
Recent activity and a license are screening evidence, not a security audit.

## Decisions

| Tool | Decision for Stronghold | Verified evidence and practical cost |
| --- | --- | --- |
| Existing Markdown, Python recall and Codex skills | Use now. Keep a short current-state index and retrieve at most three cited excerpts. | No model/embedding calls or third-party Python packages. Lexical recall cannot match every paraphrase. [Skills](https://developers.openai.com/codex/skills) load full instructions only when selected. |
| [Ruflo](https://github.com/ruvnet/ruflo) | Keep the tested 3.80.8 pin; narrow the client to 12 development tools. | MIT. New [3.80.9](https://github.com/ruvnet/ruflo/releases/tag/v3.80.9), November 26, has relevant search and policy fixes. Review separately; no upgrade performed. |
| [QMD](https://github.com/tobi/qmd) | First optional upgrade if lexical recall misses useful sources. | MIT; [2.9.0](https://github.com/tobi/qmd/releases/tag/v2.9.0), November 18. Local keyword/vector/rerank search and bounded line-numbered reads; updates account for removed documents. Node 22+, local models of roughly 2 GB in total, indexing and refresh work. Test latency and citations first. |
| [MarkItDown](https://github.com/microsoft/markitdown) | Add only when approved document conversion is needed. | MIT; [0.1.9](https://github.com/microsoft/markitdown/releases/tag/v0.1.9), October 21. Select format extras rather than every integration. Preserve original revision, page/section references and rights; conversion alone is not reliable citation or memory. Optional cloud/LLM paths need separate consideration. |
| [RTK OSS](https://github.com/rtk-ai/rtk/tree/v1.2.1) | Candidate for one measured shell-output experiment. | [1.2.1](https://github.com/rtk-ai/rtk/releases/tag/v1.2.1), November 19. Choose Apache-2.0 `rtk-oss`; the default engine and separate proxy include BUSL terms. Compare failures/exit codes and retained diagnostics. No global hooks or proxy enabled. |
| [Context7](https://github.com/upstash/context7) | Defer until repeated version-specific library lookups justify it. | MIT server; [4.9.0](https://github.com/upstash/context7/releases/tag/%40upstash/context7-mcp%404.9.0), November 26. CLI/skill mode can avoid another MCP catalog, but the hosted backend has service limits and optional key requirements. Official docs are accessible with current tools. |
| [Playwright CLI](https://github.com/microsoft/playwright-cli) | Defer until this repository has an interface to test. | Apache-2.0; [0.1.25](https://github.com/microsoft/playwright-cli/releases/tag/v0.1.25), November 18. Microsoft's [MCP README](https://github.com/microsoft/playwright-mcp#playwright-mcp-vs-playwright-cli) recommends CLI/skills for coding-agent token efficiency. Browser binaries and test maintenance are additional work. |
| [Hallmark](https://github.com/Nutlope/hallmark) | Retain the downloaded reference; apply an audit to a named interface when one exists. | MIT. Current commit `04977e1` matches the download; no GitHub release found. Useful for preserving behavior while reviewing responsive layout and visual quality. |
| [Caveman](https://github.com/JuliusBrussee/caveman) | Skip for now; use concise answers and bounded retrieval first. | Apache-2.0; [4.2.0](https://github.com/JuliusBrussee/caveman/releases/tag/v4.2.0), November 22. Current default install is a broader six-part runtime, unlike the older screenshot. CLI telemetry is on by default with opt-out. Maintainer savings depend on workload and are not Stronghold results. |

## Avoid competing sources of truth

[mcp-memory-service](https://github.com/doobidoo/mcp-memory-service) offers local
SQLite/ONNX retrieval and deletion/update APIs (Apache-2.0, 13.0.0); evaluate only
if a shared service is needed. Its bootstrap profiles are not project-isolated.
The [official MCP memory server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)
is a simpler JSONL entity graph, but lacks document passage citations and source
freshness rules; current source requires Node 24 and its license is transitioning.
[Mem0](https://github.com/mem0ai/mem0) and
[Graphiti](https://github.com/getzep/graphiti) add inference and storage operations.
Both are Apache-2.0; Graphiti's reference MCP service explicitly lacks
authentication. None is needed for this small public starter today.

Keep Markdown as the canonical development record. Ruflo memory is an optional
derived cache, not authority or private school storage. A future local SQLite
FTS index can be rebuilt from the same files without changing that boundary.

## Measure before expanding

Test the same three questions before and after a change: installation recovery,
public/private boundaries, and the next useful tool. Record the source found,
stale/missing claims, retrieved characters, tool calls and actual model tokens
when the host exposes them. Keep failure diagnostics, citations and uncertainty.
A character cap is measurable; it is not an exact tokenizer or billing estimate.

The prior smoke test returned 394 Ruflo tool definitions. That is the advertised
catalog, not proof every host loads all definitions into model context. Codex's
documented [enabled_tools](https://developers.openai.com/codex/mcp) allowlist
now selects 12 names. It is a client exposure filter, not a server authorization
or file/network sandbox. No undocumented tool-search setting was added, and no
percentage token or cost saving is claimed.
