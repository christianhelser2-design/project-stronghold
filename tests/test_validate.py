"""Behavior checks using disposable synthetic files; no real private records."""
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts.validate import validate

SOURCE = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "starter"
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".swarm", ".claude-flow", "hallmark"))

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")

    def change_json(self, name, key, value):
        data = json.loads((self.root / name).read_text())
        data[key] = value
        self.write(name, json.dumps(data))

    def assert_rejected(self, category):
        errors = validate(self.root)
        self.assertTrue(any(category in error for error in errors), errors)

    def test_complete_synthetic_starter_passes(self):
        self.assertEqual(validate(self.root), [])

    def test_malformed_json_fails(self):
        self.write("examples/lesson.synthetic.json", "{")
        self.assert_rejected("invalid JSON")

    def test_missing_file_fails(self):
        (self.root / "prompts/lesson-readiness.md").unlink()
        self.assert_rejected("missing")

    def test_missing_lesson_target_fails(self):
        path = "examples/lesson.synthetic.json"
        data = json.loads((self.root / path).read_text())
        del data["target"]
        self.write(path, json.dumps(data))
        self.assert_rejected("fields")

    def test_real_data_flag_fails(self):
        self.change_json("examples/lesson.synthetic.json", "synthetic", False)
        self.assert_rejected("synthetic")

    def test_unknown_record_field_fails(self):
        self.change_json("examples/lesson.synthetic.json", "student_name", "Invented Example")
        self.assert_rejected("fields")

    def test_agent_cannot_be_enabled(self):
        self.change_json("agents/lesson-readiness.example.json", "enabled", True)
        self.assert_rejected("disabled")

    def test_agent_cannot_gain_tools(self):
        self.change_json("agents/lesson-readiness.example.json", "tools", ["send_mail"])
        self.assert_rejected("tools")

    def test_prompt_path_cannot_escape(self):
        self.change_json("agents/lesson-readiness.example.json", "prompt", "../outside.md")
        self.assert_rejected("reference")

    def test_agent_id_must_match_profile_filename(self):
        self.change_json("agents/room-reset.example.json", "id", "lesson-readiness")
        self.assert_rejected("id must match profile filename")

    def test_agent_prompt_must_match_its_input(self):
        self.change_json("agents/room-reset.example.json", "prompt", "prompts/lesson-readiness.md")
        self.assert_rejected("prompt must match agent profile")

    def test_agent_example_input_must_match_its_prompt(self):
        self.change_json("agents/room-reset.example.json", "example_input", "examples/lesson.synthetic.json")
        self.assert_rejected("example_input must match agent profile")

    def test_integrations_stay_disabled(self):
        self.change_json("config/stronghold.example.json", "integrations_enabled", True)
        self.assert_rejected("integrations")

    def test_project_ruflo_config_passes(self):
        self.write(".codex/config.toml", '''[mcp_servers.ruflo]
command = "npx"
args = ["--yes", "ruflo@3.80.8", "mcp", "start", "--transport", "stdio"]
startup_timeout_sec = 120
enabled_tools = ["system_info", "memory_search"]
[mcp_servers.ruflo.env]
ONNXRUNTIME_NODE_INSTALL = "skip"
npm_config_cache = ".claude-flow/npm-cache"
''')
        self.assertEqual(validate(self.root), [])

    def test_malformed_toml_fails(self):
        self.write(".codex/config.toml", "[mcp_servers")
        self.assert_rejected("invalid TOML")

    def test_ruflo_cannot_disable_host_sandbox_or_approvals(self):
        self.write(".codex/config.toml", 'sandbox_mode = "danger-full-access"\n')
        self.assert_rejected("Ruflo MCP configuration")

    def test_ruflo_requires_pinned_stdio_command(self):
        for package, transport in (("ruflo@latest", "stdio"), ("ruflo@3.80.8", "http")):
            with self.subTest(package=package, transport=transport):
                self.write(".codex/config.toml", f'''[mcp_servers.ruflo]
command = "npx"
args = ["--yes", "{package}", "mcp", "start", "--transport", "{transport}"]
startup_timeout_sec = 120
enabled_tools = ["system_info", "memory_search"]
[mcp_servers.ruflo.env]
ONNXRUNTIME_NODE_INSTALL = "skip"
npm_config_cache = ".claude-flow/npm-cache"
''')
                self.assert_rejected("pinned stdio")

    def test_unreviewed_toml_stays_unsupported(self):
        self.write("config/other.toml", "enabled = true\n")
        self.assert_rejected("unsupported")

    def test_brain_index_cannot_grow_into_full_history(self):
        self.write("docs/brain-index.md", "Invented development note. " * 120)
        self.assert_rejected("brain index exceeds")

    def test_ruflo_rejects_unreviewed_or_duplicate_tools(self):
        config = (SOURCE / ".codex/config.toml").read_text()
        for tools in ('["shell_execute"]', '["system_info", "system_info"]', '[]'):
            with self.subTest(tools=tools):
                candidate = re.sub(r"enabled_tools = \[[\s\S]*?\]", "enabled_tools = " + tools, config)
                self.write(".codex/config.toml", candidate)
                self.assert_rejected("reviewed tool")

    def test_forced_ruflo_runtime_state_is_rejected(self):
        def git(*args):
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
        git("init", "-q")
        git("add", ".")
        self.write(".swarm/notes.md", "Invented runtime state")
        git("add", "-f", ".swarm/notes.md")
        self.assert_rejected("private path")

    def test_installed_skill_payload_cannot_be_published(self):
        self.write(".agents/skills/hallmark/SKILL.md", "Invented cached third-party skill")
        self.assert_rejected("third-party runtime")

    def test_secret_is_rejected_without_echoing_value(self):
        fake = "ghp_" + "A" * 36
        self.write("docs/accidental.md", fake)
        errors = validate(self.root)
        self.assertTrue(any("credential" in e for e in errors), errors)
        self.assertNotIn(fake, "\n".join(errors))

    def test_private_workbook_link_fails(self):
        self.write("docs/accidental.md", "https://docs.google.com/" + "spreadsheets/d/fictional")
        self.assert_rejected("private link")

    def test_non_example_contact_address_fails(self):
        self.write("docs/accidental.md", "invented" + "@school.invalid")
        self.assert_rejected("contact")

    def test_capitalized_private_directory_fails(self):
        self.write("docs/Private/fictional.md", "Invented text")
        self.assert_rejected("private path")

    def test_capitalized_env_filename_fails(self):
        self.write("docs/.ENV.example.md", "Invented text")
        self.assert_rejected("private path")

    def test_broken_markdown_link_fails(self):
        self.write("docs/accidental.md", "[Guide](missing.md)")
        self.assert_rejected("link")

    def test_broken_markdown_link_with_title_fails(self):
        self.write("docs/accidental.md", '[Guide](missing.md "Optional title")')
        self.assert_rejected("link")

    def test_existing_markdown_link_with_title_passes(self):
        self.write("docs/accidental.md", '[Guide](../README.md "Optional title")')
        self.assertEqual(validate(self.root), [])

    def test_symlink_is_not_followed(self):
        (self.root / "docs/link.md").symlink_to("../README.md")
        self.assert_rejected("symlink")

    def test_binary_export_fails(self):
        (self.root / "examples/export.pdf").write_bytes(b"%PDF synthetic")
        self.assert_rejected("unsupported")

    def test_duplicate_json_keys_fail(self):
        self.write("config/stronghold.example.json", '{"version":1,"version":2}')
        self.assert_rejected("invalid JSON")

    def test_markdown_link_to_ignored_file_fails(self):
        subprocess.run(["git", "-C", str(self.root), "init", "-q"], check=True)
        self.write("local/synthetic.md", "invented local-only text")
        self.write("docs/accidental.md", "[Local](../local/synthetic.md)")
        self.assert_rejected("link")

    def test_git_scans_forced_private_files_but_ignores_local_files(self):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                                  capture_output=True, text=True)
        git("init", "-q")
        git("add", ".")
        self.write("private/synthetic.txt", "fictional private test")
        self.assertEqual(validate(self.root), [])
        git("add", "-f", "private/synthetic.txt")
        self.assert_rejected("private path")

    def test_staged_credential_is_checked_after_worktree_replacement(self):
        def git(*args):
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
        git("init", "-q")
        git("add", ".")
        fake = "ghp_" + "A" * 36
        self.write("docs/accidental.md", fake)
        git("add", "docs/accidental.md")
        self.write("docs/accidental.md", "Invented safe text")
        errors = validate(self.root)
        self.assertTrue(any("staged docs/accidental.md: possible credential" in e for e in errors), errors)
        self.assertNotIn(fake, "\n".join(errors))

    def test_staged_required_file_is_checked_when_worktree_copy_remains(self):
        def git(*args):
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
        git("init", "-q")
        git("add", ".")
        git("rm", "--cached", "prompts/room-reset.md")
        self.assertTrue((self.root / "prompts/room-reset.md").exists())
        self.assert_rejected("staged prompts/room-reset.md: missing required file")

    def test_empty_staged_tree_does_not_hide_required_worktree_files(self):
        def git(*args):
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
        git("init", "-q")
        git("add", ".")
        git("rm", "--cached", "-r", ".")
        self.assertTrue((self.root / "README.md").exists())
        self.assert_rejected("staged README.md: missing required file")

    def test_staged_link_cannot_depend_on_untracked_target(self):
        def git(*args):
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
        git("init", "-q")
        git("add", ".")
        self.write("docs/accidental.md", "[Target](uncommitted.md)")
        git("add", "docs/accidental.md")
        self.write("docs/uncommitted.md", "Invented text")
        errors = validate(self.root)
        self.assertTrue(any("staged docs/accidental.md: local Markdown link" in e for e in errors), errors)

    def test_cli_failure_returns_nonzero(self):
        self.write("examples/lesson.synthetic.json", "null")
        result = subprocess.run([sys.executable, "scripts/validate.py"], cwd=self.root,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
