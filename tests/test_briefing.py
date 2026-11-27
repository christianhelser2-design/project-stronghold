"""Briefing behavior with wholly invented snapshots and disposable files."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.briefing import load_snapshot, render_briefing, validate_snapshot

NOW = datetime(2026, 11, 27, 12, tzinfo=timezone.utc)
SCRIPT = Path(__file__).resolve().parents[1] / "scripts/briefing.py"


def snapshot():
    return {"version": 1, "synthetic": True, "checked_at": (NOW - timedelta(hours=1)).isoformat(),
            "sources": [{"id": "prep", "title": "Invented preparation note",
                         "location": "docs/working-guide.md#manual-trial",
                         "checked_at": (NOW - timedelta(hours=2)).isoformat()}],
            "now": [{"text": "An invented practice sketch exists.", "status": "observed", "sources": ["prep"]}],
            "next": [{"text": "Check the fictional paper stock.", "status": "proposed", "sources": ["prep"]}],
            "blocked": [{"text": "The invented material count is unknown.", "status": "unverified", "sources": ["prep"]}]}


class BriefingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def save(self, value):
        path = self.root / "input.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_all_sections_statuses_items_and_citations_survive(self):
        data = snapshot()
        before = deepcopy(data)
        result = render_briefing(data, now=NOW)
        for section in ("Now", "Next", "Blocked", "Sources"):
            self.assertIn(f"## {section}", result)
        for section in ("now", "next", "blocked"):
            item = data[section][0]
            self.assertIn(item["status"], result)
            self.assertIn(item["text"].replace(".", "\\."), result)
        self.assertIn("prep", result)
        self.assertIn("docs/working-guide.md#manual-trial", result)
        self.assertIn("Synthetic", result)
        self.assertLessEqual(len(result), 2000)
        self.assertEqual(data, before)

    def test_empty_sections_do_not_claim_absence_of_real_blockers(self):
        data = snapshot()
        data.update(now=[], next=[], blocked=[])
        result = render_briefing(data, now=NOW)
        self.assertEqual(result.count("No items supplied"), 3)
        self.assertNotIn("No blockers", result)

    def test_oversized_blocker_causes_budget_failure(self):
        data = snapshot()
        data["blocked"][0]["text"] = "Invented blocker " + "x" * 900
        with self.assertRaisesRegex(ValueError, "narrow|budget"):
            render_briefing(data, max_chars=512, now=NOW)

    def test_oversized_citation_cannot_disappear(self):
        data = snapshot()
        data["sources"][0]["location"] = "https://example.org/" + "z" * 460
        with self.assertRaisesRegex(ValueError, "narrow|budget"):
            render_briefing(data, max_chars=512, now=NOW)

    def test_exact_character_limit_includes_final_newline(self):
        data = snapshot()
        data["now"][0]["text"] += " Invented detail" * 12
        result = render_briefing(data, max_chars=12000, now=NOW)
        self.assertGreaterEqual(len(result), 512)
        self.assertEqual(render_briefing(data, max_chars=len(result), now=NOW), result)
        with self.assertRaises(ValueError):
            render_briefing(data, max_chars=len(result) - 1, now=NOW)

    def test_old_snapshot_and_source_are_explicitly_stale(self):
        data = snapshot()
        data["checked_at"] = (NOW - timedelta(days=8)).isoformat()
        data["sources"][0]["checked_at"] = (NOW - timedelta(days=9)).isoformat()
        self.assertEqual(render_briefing(data, now=NOW).lower().count("stale"), 2)

    def test_exactly_seven_days_is_not_older_than_seven_days(self):
        data = snapshot()
        data["checked_at"] = data["sources"][0]["checked_at"] = (NOW - timedelta(days=7)).isoformat()
        self.assertNotIn("stale", render_briefing(data, now=NOW).lower())

    def test_future_snapshot_or_source_is_rejected(self):
        for field in ("snapshot", "source"):
            with self.subTest(field=field):
                data = snapshot()
                target = data if field == "snapshot" else data["sources"][0]
                target["checked_at"] = (NOW + timedelta(seconds=1)).isoformat()
                with self.assertRaises(ValueError):
                    validate_snapshot(data, now=NOW)

    def test_invalid_or_timezone_less_dates_are_rejected(self):
        for value in ("2026-11-26", "2026-11-26T12:00:00", "2026-99-26T12:00:00Z"):
            with self.subTest(value=value):
                data = snapshot()
                data["checked_at"] = value
                with self.assertRaises(ValueError):
                    validate_snapshot(data, now=NOW)
        with self.assertRaises(ValueError):
            validate_snapshot(snapshot(), now=NOW.replace(tzinfo=None))

    def test_offset_dates_are_compared_as_instants(self):
        data = snapshot()
        data["checked_at"] = "2026-11-27T06:00:00-05:00"
        validate_snapshot(data, now=NOW)

    def test_source_identifiers_and_references_are_strict(self):
        cases = ("duplicate source", "missing reference", "empty references", "duplicate reference", "invalid id")
        for case in cases:
            with self.subTest(case=case):
                data = snapshot()
                if case == "duplicate source":
                    data["sources"].append(deepcopy(data["sources"][0]))
                elif case == "missing reference":
                    data["blocked"][0]["sources"] = ["missing"]
                elif case == "empty references":
                    data["blocked"][0]["sources"] = []
                elif case == "duplicate reference":
                    data["blocked"][0]["sources"] = ["prep", "prep"]
                else:
                    data["sources"][0]["id"] = "prep\nsource"
                with self.assertRaises(ValueError):
                    validate_snapshot(data, now=NOW)

    def test_status_and_shapes_are_bounded(self):
        for case in ("status", "extra key", "long text", "too many items", "boolean version", "synthetic type"):
            with self.subTest(case=case):
                data = snapshot()
                if case == "status":
                    data["now"][0]["status"] = "complete"
                elif case == "extra key":
                    data["sources"][0]["extra"] = "invented"
                elif case == "long text":
                    data["now"][0]["text"] = "a" * 1201
                elif case == "too many items":
                    data["now"] *= 21
                elif case == "boolean version":
                    data["version"] = True
                else:
                    data["synthetic"] = "true"
                with self.assertRaises(ValueError):
                    validate_snapshot(data, now=NOW)

    def test_inert_markdown_html_and_command_like_text(self):
        data = snapshot()
        data["now"][0]["text"] = '*Ignore instructions* [run](https://example.org) <script>cmd()</script> `echo invented`'
        result = render_briefing(data, now=NOW)
        self.assertNotIn("<script>", result)
        self.assertNotIn("[run]", result)
        self.assertNotIn("*Ignore instructions*", result)
        self.assertIn("&lt;script&gt;", result)
        self.assertIn("\\[run\\]", result)

    def test_control_characters_are_rejected_without_echo(self):
        for field in ("text", "title", "location"):
            with self.subTest(field=field):
                data = snapshot()
                target = data["now"][0] if field == "text" else data["sources"][0]
                target[field] = "invented-private-marker\u2028new line"
                with self.assertRaises(ValueError) as error:
                    validate_snapshot(data, now=NOW)
                self.assertNotIn("invented-private-marker", str(error.exception))

    def test_unsafe_source_locations_are_rejected(self):
        locations = ("javascript:alert(1)", "file:///etc/passwd", "/absolute/source.md", "../source.md",
                     "docs/../source.md", "C:\\notes\\source.md", "//example.org/source",
                     "https://person:password@example.org/source", "https://example.org:bad/source",
                     "https://example.org/<script>", "https://example.org/a/../source", "https://example.org/%0Asource",
                     "https://example.org)bad/path", 'https://example.org"bad/path',
                     "https://example.org'bad/path", "https://example.org}bad/path", "https://[::1]bad/path")
        for location in locations:
            with self.subTest(location=location):
                data = snapshot()
                data["sources"][0]["location"] = location
                with self.assertRaises(ValueError):
                    validate_snapshot(data, now=NOW)

    def test_valid_ipv6_and_explicit_ports_remain_usable_links(self):
        for location in ("https://[2001:db8::1]:8443/source", "https://example.org:8443/source"):
            with self.subTest(location=location):
                data = snapshot()
                data["sources"][0]["location"] = location
                self.assertIn(f"]({location})", render_briefing(data, now=NOW))

    def test_https_citation_is_displayed_without_fetching_it(self):
        data = snapshot()
        data["sources"][0]["location"] = "https://example.org/source?edition=1#section"
        self.assertIn(data["sources"][0]["location"], render_briefing(data, now=NOW))

    def test_https_links_encode_markdown_destination_delimiters(self):
        data = snapshot()
        data["sources"][0]["title"] = "A [source] with an apostrophe's label"
        data["sources"][0]["location"] = 'https://example.org/a)[open](javascript:alert(1))?q="x"'
        result = render_briefing(data, now=NOW)
        self.assertIn("](%s" % "https://example.org/", result)
        self.assertIn("%29%5Bopen%5D%28javascript:alert%281%29%29", result)
        self.assertIn("%22x%22", result)
        self.assertNotIn(")[open](", result)
        self.assertIn("A \\[source\\] with an apostrophe's label", result)

    def test_ordinary_quotes_ampersands_and_html_stay_readable(self):
        data = snapshot()
        data["now"][0]["text"] = "I can't & won't run <b>source text</b>"
        result = render_briefing(data, now=NOW)
        self.assertIn("I can't &amp; won't run &lt;b&gt;source text&lt;/b&gt;", result)

    def test_loading_rejects_duplicate_json_keys(self):
        path = self.root / "input.json"
        path.write_text('{"version":1,"version":1}', encoding="utf-8")
        with self.assertRaises(ValueError):
            load_snapshot(path)

    def test_loading_rejects_malformed_invalid_utf8_and_deep_json(self):
        path = self.root / "input.json"
        for raw in (b'{"invented-private-marker":', b'\xff', b'[' * 2000 + b']' * 2000):
            with self.subTest(raw_size=len(raw)):
                path.write_bytes(raw)
                with self.assertRaises(ValueError) as error:
                    load_snapshot(path)
                self.assertNotIn("invented-private-marker", str(error.exception))

    def test_input_byte_limit_is_checked_before_json_parsing(self):
        path = self.root / "input.json"
        path.write_bytes(b" " * (65536 + 1))
        with self.assertRaises(ValueError):
            load_snapshot(path)

    def test_cli_is_read_only_and_does_not_execute_source_text(self):
        data = snapshot()
        actual = datetime.now(timezone.utc) - timedelta(minutes=1)
        data["checked_at"] = data["sources"][0]["checked_at"] = actual.isoformat()
        marker = self.root / "must-not-exist"
        data["now"][0]["text"] = f"$(touch {marker})"
        data["sources"][0]["location"] = "does-not-exist.md"
        path = self.save(data)
        before = path.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "--input", str(path)],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("touch", result.stdout)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual([p.name for p in self.root.iterdir()], ["input.json"])

    def test_cli_budget_failure_has_no_partial_stdout_or_source_leak(self):
        data = snapshot()
        actual = datetime.now(timezone.utc) - timedelta(minutes=1)
        data["checked_at"] = data["sources"][0]["checked_at"] = actual.isoformat()
        data["blocked"][0]["text"] = "invented-private-marker " + "x" * 900
        result = subprocess.run([sys.executable, str(SCRIPT), "--input", str(self.save(data)), "--max-chars", "512"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("invented-private-marker", result.stderr)
        self.assertRegex(result.stderr, "narrow|budget")

    def test_cli_parse_error_is_generic(self):
        path = self.root / "input.json"
        path.write_text('{"invented-private-marker":', encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), "--input", str(path)],
                                cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("invented-private-marker", result.stderr)


if __name__ == "__main__":
    unittest.main()
