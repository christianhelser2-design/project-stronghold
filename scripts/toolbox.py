"""Inspect local toolbox entries, or explicitly run an installed tool without downloads."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib


def registry(project, root):
    """Fixed launch prefixes; receipts document checks beyond file presence."""
    def item(name, relative, runtime=None, kind="cli", env=None, base=None, receipt=None):
        entry = (base or root / name) / relative
        return {"entry": entry, "command": ([runtime] if runtime else []) + [str(entry)],
                "kind": kind, "env": env or {},
                "receipt": receipt or root / name / "ADOPTION.md"}

    def local(name, relative):
        return str(root / name / relative)

    tools = {
        "qmd": item("qmd", "qmd-local"),
        "markitdown": item("markitdown", ".venv/bin/markitdown"),
        "rtk": item("rtk", "run.py", sys.executable),
        "context7": item("context7", "run-local.sh", kind="fixed-server"),
        "playwright": item("playwright", "run-local.sh"),
        "caveman": item("caveman", "run-local.sh"),
        "hermes": item("hermes", "run-local.py", sys.executable, kind="manual-agent"),
        "mem0": item("mem0", ".venv/bin/python", kind="sdk",
                     env={"MEM0_TELEMETRY": "false", "MEM0_DIR": local("mem0", "state/config"),
                          "FASTEMBED_CACHE_PATH": local("mem0", "models"),
                          "HF_HOME": local("mem0", "hf-cache"), "HF_HUB_DISABLE_TELEMETRY": "1"}),
        "graphiti": item("graphiti", ".venv/bin/python", kind="sdk",
                         env={"GRAPHITI_TELEMETRY_ENABLED": "false"}),
        "mcp-memory": item("mcp-memory", "launch.py", sys.executable, "fixed-server"),
        "mcp-memory-service": item("mcp-memory-service", "launch.py",
                                   local("mcp-memory-service", ".venv/bin/python"), "fixed-server"),
        "hallmark": item("hallmark", ".agents/skills/hallmark/scripts/sloplint.mjs", "node", base=project),
        "agency-agents": item("agency-agents", "README.md", kind="reference"),
        "ruflo": item("ruflo", ".codex/config.toml", kind="configuration", base=project,
                      receipt=project / "docs/ruflo.md",
                      env={"ONNXRUNTIME_NODE_INSTALL": "skip",
                           "npm_config_cache": str(project / ".claude-flow/npm-cache")}),
    }
    tools["context7"]["command"] += ["--transport", "stdio"]
    tools["ruflo"]["command"] = ["npx", "--offline", "--yes"]
    return tools


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", choices=("list", "status", "run"), default="status")
    parser.add_argument("name", nargs="?", help="registered tool name")
    parser.add_argument("arguments", nargs=argparse.REMAINDER,
                        help="literal tool arguments; --start deliberately starts a stdio server")
    args = parser.parse_args(argv)
    project = Path(__file__).resolve().parents[1]
    root = Path(os.environ.get("STRONGHOLD_TOOLBOX_ROOT", project.parent / "toolbox")).absolute()
    tools = registry(project, root)
    if args.name is not None and args.name not in tools:
        parser.error("unknown tool name; use list")
    if args.action != "run":
        if args.arguments:
            parser.error("status/list do not accept tool arguments")
        print("File presence only; runtime/package health is not verified. Receipts are not executed.")
        names = [args.name] if args.name else sorted(tools)
        for name in names:
            tool = tools[name]
            presence = "present" if tool["entry"].is_file() else "missing"
            receipt = "present" if tool["receipt"].is_file() else "missing"
            print(f"{name}: {tool['kind']}, entry={presence}, receipt={receipt}; {tool['receipt']}"[:400])
        return 0
    if args.name is None:
        parser.error("run requires a registered tool name")
    tool = tools[args.name]
    if tool["kind"] == "reference":
        print("Reference material is status-only; open the source directly.", file=sys.stderr)
        return 126
    arguments = args.arguments
    if arguments and arguments[0] == "--":
        arguments = arguments[1:]
    if not arguments:
        parser.error("run requires explicit tool arguments; use --start for a stdio server")
    if tool["kind"] == "manual-agent" and arguments not in (["--status"], ["--version"], ["--help"]):
        parser.error("this manual-agent launcher accepts only --status, --version or --help")
    if tool["kind"] == "fixed-server" and arguments != ["--start"]:
        parser.error("this fixed stdio launcher requires exactly --start")
    if arguments == ["--start"]:
        if tool["kind"] not in {"server", "fixed-server"}:
            parser.error("--start is reserved for registered stdio servers")
        arguments = []
    if not tool["entry"].is_file():
        print("Local entry is missing; no download or installation was attempted.", file=sys.stderr)
        return 127
    if args.name == "ruflo":
        try:
            config = tomllib.loads(tool["entry"].read_text(encoding="utf-8"))
            package = config["mcp_servers"]["ruflo"]["args"][1]
            if not isinstance(package, str) or not re.fullmatch(r"ruflo@\d+\.\d+\.\d+", package):
                raise ValueError("unpinned package")
        except (OSError, ValueError, KeyError, IndexError, TypeError):
            parser.error("Ruflo configuration must contain a pinned numeric package")
        tool["command"].append(package)
    try:
        return subprocess.run(tool["command"] + arguments, cwd=project,
                              env={**os.environ, **tool["env"]}, shell=False).returncode
    except OSError:
        print("Local command could not start; inspect its installation receipt.", file=sys.stderr)
        return 127


if __name__ == "__main__":
    sys.exit(main())
