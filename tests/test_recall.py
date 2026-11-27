"""Recall behavior using wholly invented, disposable source documents."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.recall import recall


class RecallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_relevant_fact_has_source_line_and_heading(self):
        self.write("README.md", "# Starter\n\nThe garden uses wooden boxes.\n")
        self.write("docs/project-record.md", "# Decisions\n\n## Sprout trial\n\nUse blue trays for seed sorting.\n")
        result = recall(self.root, "seed sorting")
        self.assertIn("docs/project-record.md:5", result)
        self.assertIn("Sprout trial", result)
        self.assertIn("blue trays", result)
        self.assertNotIn("wooden boxes", result)
        self.assertIn("untrusted", result)

    def test_topic_installation_evidence_outranks_fenced_recall_examples(self):
        self.write("README.md", '# Starter\n\nRecall example:\n\n```bash\n'
                   'python3 scripts/recall.py "Ruflo installation"\n```\n')
        self.write("docs/brain-index.md", '# Project memory\n\n```bash\n'
                   'python3 scripts/recall.py "Ruflo installation"\n```\n')
        self.write("docs/ruflo.md", '# Ruflo development tooling\n\n## Setup\n\n'
                   'Install with bundled CPU binaries and skip extra GPU downloads.\n')
        result = recall(self.root, "Ruflo installation", limit=1)
        self.assertIn("docs/ruflo.md:5", result)
        self.assertIn("bundled CPU binaries", result)
        self.assertNotIn("python3 scripts/recall.py", result)

    def test_fenced_code_is_not_recalled_as_evidence(self):
        for fence in ("```", "~~~~"):
            with self.subTest(fence=fence):
                self.write("README.md", f'# Starter\n\n{fence}\n# zircon-marker\n'
                           f'Invented zircon-marker command\n{fence}\n')
                self.assertIn("No matching", recall(self.root, "zircon-marker"))

    def test_citation_after_code_fence_keeps_original_line_number(self):
        self.write("README.md", '# Starter\n\n```\nignored command\n```\n\n'
                   'Invented zircon-marker evidence.\n')
        self.assertIn("README.md:7", recall(self.root, "zircon-marker"))

    def test_current_file_is_read_again_after_change(self):
        self.write("docs/brain-index.md", "# Current\n\nSeed tray color is blue.\n")
        self.assertIn("blue", recall(self.root, "tray color"))
        self.write("docs/brain-index.md", "# Current\n\nSeed tray color is orange.\n")
        result = recall(self.root, "tray color")
        self.assertIn("orange", result)
        self.assertNotIn("blue", result)

    def test_unlisted_and_private_sources_are_not_searched(self):
        for name in ("private/notes.md", ".swarm/notes.md", "docs/private/notes.md", "docs/unlisted.md"):
            self.write(name, "Invented zircon-marker data.\n")
        result = recall(self.root, "zircon-marker")
        self.assertIn("No matching", result)
        self.assertNotIn("Invented", result)

    def test_source_file_symlink_is_skipped(self):
        outside = self.write("private/notes.md", "Invented zircon-marker data.\n")
        (self.root / "README.md").symlink_to(outside)
        self.assertIn("No matching", recall(self.root, "zircon-marker"))

    def test_source_ancestor_symlink_is_skipped(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "brain-index.md").write_text("Invented zircon-marker data.\n")
        (self.root / "docs").symlink_to(outside, target_is_directory=True)
        self.assertIn("No matching", recall(self.root, "zircon-marker"))

    def test_budget_is_hard_and_clipping_is_explicit(self):
        self.write("docs/project-record.md", "# Trial\n\nSeed trays " + "invented detail " * 600)
        result = recall(self.root, "seed trays", max_chars=256)
        self.assertLessEqual(len(result), 256)
        self.assertIn("docs/project-record.md:3", result)
        self.assertIn("clipped", result.lower())

    def test_long_line_match_near_end_is_visible(self):
        self.write("README.md", "# Trial\n\n" + "ordinary " * 200 + "zircon seed trays.\n")
        self.assertIn("zircon", recall(self.root, "zircon", max_chars=400))

    def test_multiline_window_cites_the_actual_start_line(self):
        self.write("README.md", "# Trial\n\n" + "ordinary " * 200 + "\n" +
                   "mundane " * 40 + "zircon seed trays.\n")
        result = recall(self.root, "zircon", max_chars=400)
        self.assertIn("README.md:4", result)
        self.assertIn("zircon", result)

    def test_result_limit_and_no_match(self):
        self.write("README.md", "# Trial\n\nSeed trays are blue.\n\nSeed trays are orange.\n")
        result = recall(self.root, "seed trays", limit=1)
        self.assertEqual(result.count("README.md:"), 1)
        self.assertIn("clipped", result.lower())
        no_match = recall(self.root, "volcano")
        self.assertIn("No matching", no_match)
        self.assertIn("narrow", no_match.lower())

    def test_invalid_programmatic_limits_fail(self):
        for kwargs in ({"limit": 0}, {"limit": 11}, {"max_chars": 255}, {"max_chars": 12001}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                recall(self.root, "seed", **kwargs)

    def test_cli_rejects_invalid_limits(self):
        command = [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts/recall.py")]
        for args in (("seed", "--max-chars", "1"), ("seed", "--limit", "11")):
            with self.subTest(args=args):
                result = subprocess.run([*command, *args], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)

    def test_cli_stdout_respects_character_budget(self):
        command = [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts/recall.py")]
        result = subprocess.run([*command, "ruflo", "--max-chars", "256"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertLessEqual(len(result.stdout), 256)


if __name__ == "__main__":
    unittest.main()
