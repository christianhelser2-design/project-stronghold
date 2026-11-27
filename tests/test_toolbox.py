"""Portable launcher checks using local fake tools; no package or model calls."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
LAUNCHER = SOURCE / "scripts/toolbox.py"


class ToolboxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "toolbox"
        self.root.mkdir()

    def fake(self, relative, body):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"#!{sys.executable}\n{body}\n")
        path.chmod(0o755)
        return path

    def project(self, config=None):
        project = Path(self.temp.name) / "invented-project"
        (project / "scripts").mkdir(parents=True, exist_ok=True)
        shutil.copy2(LAUNCHER, project / "scripts/toolbox.py")
        if config is not None:
            (project / ".codex").mkdir(exist_ok=True)
            (project / ".codex/config.toml").write_text(config)
        return project

    def invoke(self, *args, env=None, project=None):
        settings = {**os.environ, "STRONGHOLD_TOOLBOX_ROOT": str(self.root)}
        settings.update(env or {})
        launcher = project / "scripts/toolbox.py" if project else LAUNCHER
        return subprocess.run([sys.executable, str(launcher), *args],
                              cwd=self.temp.name, env=settings,
                              capture_output=True, text=True, timeout=10)

    def test_default_status_does_not_execute_present_tool(self):
        marker = self.root / "unexpected-execution"
        self.fake("qmd/qmd-local", f"from pathlib import Path\nPath({str(marker)!r}).touch()")
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("qmd", result.stdout)
        self.assertIn("present", result.stdout)
        self.assertIn("not verified", result.stdout)
        self.assertFalse(marker.exists())

    def test_missing_tool_does_not_attempt_package_download(self):
        marker = self.root / "unexpected-download"
        fake_bin = self.fake("fake-bin/npx", f"from pathlib import Path\nPath({str(marker)!r}).touch()")
        result = self.invoke("run", "markitdown", "--help",
                             env={"PATH": str(fake_bin.parent) + os.pathsep + os.environ.get("PATH", "")})
        self.assertEqual(result.returncode, 127)
        self.assertIn("missing", result.stderr.lower())
        self.assertFalse(marker.exists())

    def test_unknown_name_is_rejected(self):
        result = self.invoke("run", "../not-a-tool", "--version")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown", result.stderr.lower())

    def test_arguments_stay_literal_and_child_exit_is_preserved(self):
        self.fake("rtk/run.py", "import json, sys\nprint(json.dumps(sys.argv[1:]))\nsys.exit(7)")
        marker = self.root / "should-not-exist"
        arguments = ["--flag", "two words", f"$(touch {marker})", "; echo unrelated"]
        result = self.invoke("run", "rtk", *arguments)
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertEqual(json.loads(result.stdout), arguments)
        self.assertFalse(marker.exists())

    def test_root_override_selects_local_tool(self):
        self.fake("qmd/qmd-local", 'print("invented overridden root")')
        result = self.invoke("run", "qmd", "status")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "invented overridden root")

    def test_status_is_bounded_and_does_not_read_receipt_body(self):
        receipt = self.root / "qmd/ADOPTION.md"
        receipt.parent.mkdir()
        receipt.write_text("INVENTED_LARGE_RECEIPT_CONTENT " * 10000)
        result = self.invoke("list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLessEqual(len(result.stdout), 6500)
        self.assertNotIn("INVENTED_LARGE_RECEIPT_CONTENT", result.stdout)
        self.assertIn("ADOPTION.md", result.stdout)
        self.assertIn("sdk", result.stdout.lower())

    def test_reference_material_cannot_be_executed(self):
        path = self.root / "agency-agents/README.md"
        path.parent.mkdir()
        path.write_text("Wholly invented reference material")
        result = self.invoke("run", "agency-agents", "--help")
        self.assertEqual(result.returncode, 126)
        self.assertIn("reference", result.stderr.lower())

    def test_run_without_arguments_never_implicitly_starts_server(self):
        result = self.invoke("run", "mcp-memory")
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicit", result.stderr.lower())

    def test_explicit_server_start_uses_fixed_local_helper(self):
        self.fake("mcp-memory/launch.py", "import json, sys\nprint(json.dumps(sys.argv[1:]))")
        result = self.invoke("run", "mcp-memory", "--start")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])

    def test_fixed_server_help_cannot_accidentally_start_it(self):
        marker = self.root / "unexpected-server"
        self.fake("mcp-memory-service/launch.py", "# Invented server entry")
        self.fake("mcp-memory-service/.venv/bin/python", f"from pathlib import Path\nPath({str(marker)!r}).touch()")
        self.fake("mcp-memory/launch.py", f"from pathlib import Path\nPath({str(marker)!r}).touch()")
        for name in ("mcp-memory", "mcp-memory-service"):
            with self.subTest(name=name):
                result = self.invoke("run", name, "--help")
                self.assertEqual(result.returncode, 2)
                self.assertIn("--start", result.stderr)
                self.assertFalse(marker.exists())

    def test_context7_requires_explicit_start_marker(self):
        marker = self.root / "unexpected-context7"
        self.fake("context7/run-local.sh", f"from pathlib import Path\nPath({str(marker)!r}).touch()")
        for arguments in (("--port", "1234"), ("--experimental",)):
            with self.subTest(arguments=arguments):
                result = self.invoke("run", "context7", *arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("--start", result.stderr)
                self.assertFalse(marker.exists())

    def test_context7_explicit_start_retains_stdio_prefix(self):
        self.fake("context7/run-local.sh", "import json, sys\nprint(json.dumps(sys.argv[1:]))")
        result = self.invoke("run", "context7", "--start")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), ["--transport", "stdio"])

    def test_ruflo_uses_offline_cache_without_implicit_download(self):
        project = self.project('[mcp_servers.ruflo]\nargs = ["--yes", "ruflo@7.8.9"]\n')
        fake_bin = self.fake("fake-bin/npx", "import json, os, sys\nprint(json.dumps({'args': sys.argv[1:], 'cache': os.environ.get('npm_config_cache')}))")
        result = self.invoke("run", "ruflo", "--version", project=project,
                             env={"PATH": str(fake_bin.parent) + os.pathsep + os.environ.get("PATH", "")})
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(result.stdout)
        self.assertIn("--offline", record["args"])
        self.assertIn("ruflo@7.8.9", record["args"])
        self.assertEqual(record["args"][-1], "--version")
        self.assertEqual(Path(record["cache"]), project / ".claude-flow/npm-cache")

    def test_missing_ruflo_config_never_launches_npx(self):
        project = self.project()
        marker = self.root / "unexpected-npx"
        fake_bin = self.fake("fake-bin/npx", f"from pathlib import Path\nPath({str(marker)!r}).touch()")
        result = self.invoke("run", "ruflo", "--version", project=project,
                             env={"PATH": str(fake_bin.parent) + os.pathsep + os.environ.get("PATH", "")})
        self.assertEqual(result.returncode, 127)
        self.assertFalse(marker.exists())
        self.assertEqual(self.invoke("status", "ruflo", project=project).returncode, 0)

    def test_invalid_ruflo_config_never_launches_npx(self):
        marker = self.root / "unexpected-npx"
        fake_bin = self.fake("fake-bin/npx", f"from pathlib import Path\nPath({str(marker)!r}).touch()")
        for config in ('[mcp_servers', '[mcp_servers.ruflo]\nargs = ["--yes", "ruflo@latest"]\n'):
            with self.subTest(config=config):
                project = self.project(config)
                result = self.invoke("run", "ruflo", "--version", project=project,
                                     env={"PATH": str(fake_bin.parent) + os.pathsep + os.environ.get("PATH", "")})
                self.assertEqual(result.returncode, 2)
                self.assertIn("configuration", result.stderr.lower())
                self.assertFalse(marker.exists())
                self.assertEqual(self.invoke("status", "ruflo", project=project).returncode, 0)


if __name__ == "__main__":
    unittest.main()
