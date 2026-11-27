# On demand cited briefing

Format one explicitly supplied snapshot into **Now / Next / Blocked / Sources**:

```bash
python3 scripts/briefing.py --input examples/briefing.synthetic.json --max-chars 2000
```

The example is wholly invented and labeled synthetic. Real operational snapshots,
their assembly evidence and rendered briefings belong outside this public checkout
in approved private storage. The formatter reads only its supplied JSON file and
writes only stdout. It does not search directories, fetch cited locations, invoke
a model, execute source text, update records or schedule work.

## Assemble before formatting

The assistant selects the relevant existing records, opens them, checks the claims
and prepares one bounded snapshot. Keep the original source revision/hash, section
or page location and any effective/event dates in a separate assembly receipt.
Record what was actually inspected; do not turn a proposed action into an observed
completion. Reopening an old record does not establish current section progress.

`checked_at` means **inspection time**, not the effective date or truth of every
claim. This formatter validates structure and age; a citation or recently inspected
record is not proof of current classroom conditions. Source verification remains
the assembling assistant's task, with current classroom decisions kept separate.

## Exact snapshot contract

The top-level fields are exactly `version`, `synthetic`, `checked_at`, `sources`,
`now`, `next` and `blocked`. Version is integer `1`; `synthetic` is a boolean.
Dates are ISO 8601 strings with explicit timezone offsets or `Z`.

| Record | Exact fields and bounds |
| --- | --- |
| Snapshot sources | List of 0–24 source records |
| Source | `id`, `title`, `location`, `checked_at` |
| Source ID | Unique; lowercase letter followed by up to 31 lowercase letters, digits, underscores or hyphens |
| Source title/location | Nonempty title up to 120 characters; location up to 500 |
| Now/Next/Blocked | Each is a list of 0–20 items |
| Item | Exactly `text`, `status`, `sources` |
| Item text | Nonempty, single-line text up to 1,200 characters |
| Item status | Exactly `observed`, `proposed` or `unverified` |
| Item references | 1–12 unique IDs from the snapshot source list |

Missing/unknown fields, duplicate source IDs, bad or duplicate references and
duplicate JSON keys fail. Empty sections say **No items supplied**; they do not
claim that no real blockers or actions exist. All supplied sources are retained.

Locations are displayed evidence, never opened by the formatter. HTTP(S) sources
become clickable Markdown citations, with destination delimiters encoded and
titles escaped. Relative repository-style paths remain inline code. Userinfo or
passwords in URLs, executable schemes, absolute/Windows paths, traversal, raw
HTML/backticks, whitespace/control characters and malformed ports are rejected.
Path existence, domain ownership and publication/access rights are not verified.
Human text is Markdown/HTML escaped; control and formatting characters are rejected.
Instruction-like text remains displayed data rather than authority to act.

## Dates and output budget

Future or timezone-less inspection dates fail. A snapshot or source more than
seven days old receives an explicit stale label; exactly seven days is accepted
without that label. Inspection age is checked at render time using aware datetimes;
the supplied offset remains visible. Age flags do not replace event/pacing checks.

Input is limited to **65,536 bytes**, read with a 65,537-byte guard before decoding.
The output limit defaults to **2,000 characters**, with accepted limits 512–12,000.
It includes headings, escaping, citations and final newline. This is a character
budget, not an exact token measurement.

The formatter either returns the complete briefing or fails before writing any
partial stdout. It never truncates an item, drops a blocker, removes a source or
uses a top-k selection to fit. On budget failure, narrow the explicitly assembled
snapshot or deliberately raise `--max-chars`; do not silently discard unresolved
evidence. Errors identify a generic problem without echoing supplied source text.

## Small Python interface

- `load_snapshot(path) -> dict`: parse one explicitly supplied UTF-8 JSON object,
  rejecting excessive size and duplicate keys. It does not verify claims.
- `validate_snapshot(snapshot, *, now=None) -> None`: validate the contract and
  timestamps, raising `ValueError` on invalid input.
- `render_briefing(snapshot, *, max_chars=2000, now=None) -> str`: validate and
  return the complete Markdown briefing, or raise `ValueError`.

`now` may be an explicitly timezone-aware `datetime` for deterministic tests;
when omitted, the current UTC instant is used. The functions do not mutate the
snapshot. Public-example validation uses this same contract and additionally
requires `synthetic: true`. Classroom agent profiles remain disabled.

Focused checks:

```bash
python3 -m unittest discover -s tests -p test_briefing.py -v
python3 -m unittest discover -s tests -p test_validate.py -v
```
