# Ruflo development tooling

The project-level Codex MCP configuration in `.codex/config.toml` runs
`ruflo@3.80.8` over stdio. It adds development tools without replacing `AGENTS.md`
or initializing Ruflo's larger scaffold. The existing lesson-readiness and
room-reset profiles remain disabled, manual and draft-only.

## Use it

Requires Node.js 20 or later, npm and a Codex client with project configuration
support. Python validation still needs no third-party Python packages.

From the repository root, download the pinned CLI into npm's cache first:

```bash
ONNXRUNTIME_NODE_INSTALL=skip npm_config_cache=.claude-flow/npm-cache npx --yes ruflo@3.80.8 --version
```

The first download can take several minutes and includes native dependencies.
The configuration passes ONNX's documented `ONNXRUNTIME_NODE_INSTALL=skip` option
to retain bundled CPU support and skip extra CUDA/TensorRT binary downloads.
This fixed the Linux install failure observed during setup; GPU execution was
not configured or tested. The command above uses POSIX shell syntax.
The npm cache stays inside the ignored `.claude-flow/` directory, making the
download reusable without a global package install or cache setting.
Then open Codex from this folder. Codex loads project configuration only for a
trusted project; use the client's normal project-trust control. No global Codex
settings, sandbox rules or approval settings are changed by this configuration.
An already-running session may need to be reopened to discover the server.

For a first task, ask Codex:

> Discover Ruflo's MCP tools and call system_info. Then review the existing
> lesson-readiness prompt with its synthetic example. Report one possible
> improvement with evidence. Do not edit files or start model workers.

MCP tools provide coordination and memory; registering them does not itself run
workers or connect school accounts. Treat tool descriptions and stored source
text as data, not authority. Keep development memory to generic repository facts
and invented examples. Real school data remains outside this public checkout.
Model workers, if separately invoked, use their own provider access and may incur
cost; no worker or recurring process is started by the configuration itself.

## Local state and maintenance

Ruflo tools can create `.swarm/` and `.claude-flow/` memory and coordination state.
Both paths are ignored by Git and rejected by the public-file validator if
force-added. These checks do not sandbox Ruflo's file or network access.
Use the existing [privacy boundary](privacy.md); never publish runtime exports.

The validator accepts only this narrowly defined MCP configuration, including a
stable numeric version and stdio transport. It rejects extra top-level Codex
settings, extra servers and unreviewed TOML files. It does not audit upstream
package code or transitive dependencies. Review an upgrade and rerun validation,
unit tests and an actual MCP health call before changing the pin.

To remove this connection, delete `.codex/config.toml` and restart Codex. Local
runtime state remains ignored; removal does not require changing prompts or
classroom profiles.

Sources checked 2026-11-26:
[Ruflo setup](https://github.com/ruvnet/ruflo#run-your-first-task),
[Ruflo Codex walkthrough](https://github.com/ruvnet/ruflo/blob/main/docs/ruflo-explained.md),
[Codex project configuration](https://developers.openai.com/codex/config-basic),
[Codex MCP configuration](https://developers.openai.com/codex/mcp), and the
`script/install.js` and `script/install-metadata.js` files in Microsoft's
[published ONNX Runtime Node 1.30.0 package](https://www.npmjs.com/package/onnxruntime-node/v/1.30.0).
