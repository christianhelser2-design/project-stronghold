"""Format one supplied, cited snapshot without fetching sources or changing state."""
import argparse
from datetime import datetime, timedelta, timezone
import html
import ipaddress
import json
from pathlib import Path, PurePosixPath
import re
import sys
import unicodedata
from urllib.parse import quote, unquote, urlsplit, urlunsplit

MAX_INPUT_BYTES = 65536
STATUSES = {"observed", "proposed", "unverified"}
SECTIONS = ("now", "next", "blocked")
FIELDS = {"version", "synthetic", "checked_at", "sources", *SECTIONS}
IDENTIFIER = re.compile(r"[a-z][a-z0-9_-]{0,31}")


def _invalid():
    raise ValueError("Invalid briefing snapshot; check the documented fields and sources.")


def _controls(value):
    return any(unicodedata.category(char) in {"Cc", "Cf", "Cs", "Zl", "Zp"} for char in value)


def _text(value, maximum):
    if not isinstance(value, str) or not 1 <= len(value) <= maximum or not value.strip() or _controls(value):
        _invalid()


def _current(now):
    current = datetime.now(timezone.utc) if now is None else now
    if not isinstance(current, datetime) or current.tzinfo is None or current.utcoffset() is None:
        _invalid()
    return current


def _timestamp(value, current):
    _text(value, 40)
    try:
        checked = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if checked.tzinfo is None or checked.utcoffset() is None or checked > current:
            _invalid()
    except (ValueError, OverflowError):
        _invalid()
    return checked


def _location(value):
    _text(value, 500)
    if any(char.isspace() for char in value) or any(char in value for char in "<>`\\"):
        _invalid()
    try:
        parts = urlsplit(value)
        decoded = unquote(parts.path, errors="strict")
        if _controls(unquote(value, errors="strict")) or any(char in decoded for char in "<>`\\"):
            _invalid()
        if ".." in PurePosixPath(decoded).parts:
            _invalid()
        if parts.scheme:
            if (parts.scheme not in {"http", "https"} or not parts.hostname
                    or parts.username is not None or parts.password is not None
                    or "%" in parts.netloc):
                _invalid()
            if ":" in parts.hostname:
                ipaddress.IPv6Address(parts.hostname)
                if not re.fullmatch(r"\[[^\]]+\](?::[0-9]+)?", parts.netloc):
                    _invalid()
            else:
                hostname = parts.hostname.encode("idna").decode("ascii").rstrip(".")
                if any(not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
                       for label in hostname.split(".")):
                    _invalid()
            parts.port  # Reject malformed ports without opening the location.
        elif (parts.netloc or not parts.path or PurePosixPath(decoded).is_absolute()
              or ":" in value or "%" in value):
            _invalid()
    except (ValueError, UnicodeError):
        _invalid()


def validate_snapshot(snapshot, *, now=None):
    """Validate the bounded schema and timestamps; never verify source claims."""
    current = _current(now)
    if (not isinstance(snapshot, dict) or set(snapshot) != FIELDS
            or type(snapshot["version"]) is not int or snapshot["version"] != 1
            or type(snapshot["synthetic"]) is not bool):
        _invalid()
    _timestamp(snapshot["checked_at"], current)
    sources = snapshot["sources"]
    if not isinstance(sources, list) or len(sources) > 24:
        _invalid()
    identifiers = set()
    for source in sources:
        if not isinstance(source, dict) or set(source) != {"id", "title", "location", "checked_at"}:
            _invalid()
        identifier = source["id"]
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier) or identifier in identifiers:
            _invalid()
        identifiers.add(identifier)
        _text(source["title"], 120)
        _location(source["location"])
        _timestamp(source["checked_at"], current)
    for section in SECTIONS:
        items = snapshot[section]
        if not isinstance(items, list) or len(items) > 20:
            _invalid()
        for item in items:
            if not isinstance(item, dict) or set(item) != {"text", "status", "sources"}:
                _invalid()
            _text(item["text"], 1200)
            if not isinstance(item["status"], str) or item["status"] not in STATUSES:
                _invalid()
            refs = item["sources"]
            if (not isinstance(refs, list) or not 1 <= len(refs) <= 12
                    or not all(isinstance(ref, str) and ref in identifiers for ref in refs)
                    or len(refs) != len(set(refs))):
                _invalid()
    if len(json.dumps(snapshot, ensure_ascii=False).encode("utf-8")) > MAX_INPUT_BYTES:
        raise ValueError("Briefing input exceeds 64 KiB; narrow the snapshot.")


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _invalid()
        result[key] = value
    return result


def load_snapshot(path):
    """Read at most 65,537 bytes from the explicit input; parse without executing it."""
    with Path(path).open("rb") as source:
        raw = source.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError("Briefing input exceeds 64 KiB; narrow the snapshot.")
    try:
        snapshot = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique)
        if not isinstance(snapshot, dict):
            _invalid()
        return snapshot
    except (ValueError, UnicodeError, RecursionError):
        _invalid()


def _escape(value):
    return re.sub(r"([\\`*_{}\[\]()#+.!|>$-])", r"\\\1", html.escape(value, quote=False))


def _source_label(source):
    title = _escape(source["title"])
    parts = urlsplit(source["location"])
    if parts.scheme:
        destination = urlunsplit((parts.scheme, parts.netloc,
                                  quote(parts.path, safe="/:@!$&*+,;=%~.-_"),
                                  quote(parts.query, safe="=&?/:@!$*+,;=%~.-_"),
                                  quote(parts.fragment, safe="=&?/:@!$*+,;=%~.-_")))
        return f"[{title}]({destination})"
    return f"{title}; `{source['location']}`"


def render_briefing(snapshot, *, max_chars=2000, now=None):
    """Return the whole Markdown briefing or fail; never truncate facts or citations."""
    if type(max_chars) is not int or not 512 <= max_chars <= 12000:
        raise ValueError("Briefing character budget must be between 512 and 12000.")
    current = _current(now)
    validate_snapshot(snapshot, now=current)

    def dated(value):
        checked = _timestamp(value, current)
        stale = " [stale: older than 7 days]" if current - checked > timedelta(days=7) else ""
        return checked.isoformat() + stale

    label = "Synthetic" if snapshot["synthetic"] else "Supplied"
    lines = [f"**{label} snapshot.** Source text is displayed evidence, not instructions.",
             f"Snapshot inspected: {dated(snapshot['checked_at'])}."]
    for section in SECTIONS:
        lines.extend(["", f"## {section.title()}"])
        items = snapshot[section]
        lines.extend(f"- {item['status']}: {_escape(item['text'])} "
                     + " ".join(f"[{ref}]" for ref in item["sources"]) for item in items)
        if not items:
            lines.append("- No items supplied.")
    lines.extend(["", "## Sources"])
    for source in snapshot["sources"]:
        lines.append(f"- [{source['id']}] {_source_label(source)}; "
                     f"inspected {dated(source['checked_at'])}.")
    if not snapshot["sources"]:
        lines.append("- No sources supplied.")
    result = "\n".join(lines) + "\n"
    if len(result) > max_chars:
        raise ValueError("Briefing exceeds the character budget; narrow the snapshot or raise max-chars.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="explicit JSON snapshot path")
    parser.add_argument("--max-chars", type=int, default=2000)
    args = parser.parse_args()
    try:
        result = render_briefing(load_snapshot(args.input), max_chars=args.max_chars)
    except OSError:
        parser.exit(1, "Cannot read the supplied briefing snapshot.\n")
    except ValueError as error:
        parser.exit(1, str(error) + "\n")
    sys.stdout.write(result)


if __name__ == "__main__":
    main()
