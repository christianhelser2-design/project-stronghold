"""Behavior checks using disposable synthetic files; no real private records."""
import json
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
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

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

    def test_integrations_stay_disabled(self):
        self.change_json("config/stronghold.example.json", "integrations_enabled", True)
        self.assert_rejected("integrations")

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

    def test_broken_markdown_link_fails(self):
        self.write("docs/accidental.md", "[Guide](missing.md)")
        self.assert_rejected("link")

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

    def test_cli_failure_returns_nonzero(self):
        self.write("examples/lesson.synthetic.json", "null")
        result = subprocess.run([sys.executable, "scripts/validate.py"], cwd=self.root,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
