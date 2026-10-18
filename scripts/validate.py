"""Small, dependency-free checks for public starter files; not a privacy guarantee."""
import ast
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

REQUIRED = {
    "README.md", "AGENTS.md", ".gitignore", "docs/privacy.md",
    "docs/working-guide.md", "docs/project-record.md",
    "prompts/lesson-readiness.md", "prompts/room-reset.md",
    "agents/lesson-readiness.example.json", "agents/room-reset.example.json",
    "config/stronghold.example.json", "examples/lesson.synthetic.json",
    "examples/room-reset.synthetic.json", "scripts/validate.py",
    "tests/test_validate.py", ".github/workflows/validate.yml",
    ".github/pull_request_template.md",
}
PRIVATE_PARTS = {"private", "data", "exports", "uploads", "local", ".venv", "node_modules"}
ALLOWED_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml"}
CREDENTIAL = re.compile(
    r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|"
    r"-----BEGIN (?:[A-Z ]*PRIVATE KEY)-----)"
)
PRIVATE_LINK = re.compile(
    r"https?://(?:docs\.google\.com/(?:spreadsheets|document|presentation)/d/|"
    r"drive\.google\.com/(?:file/d/|drive/folders/)|mail\.google\.com/)", re.I
)
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
FIELDS = {
    "config": {"version", "timezone", "data_policy", "integrations_enabled", "agents"},
    "agent": {"version", "id", "enabled", "invocation", "mode", "prompt", "example_input",
              "tools", "owner_role", "review"},
    "lesson": {"version", "synthetic", "scenario", "source", "duration_minutes", "target",
               "standard", "starting_point", "materials", "choice", "steps", "access_support",
               "cleanup", "reentry", "unknowns"},
    "room": {"version", "synthetic", "scenario", "observation", "prep_minutes", "materials",
             "goal", "unknowns"},
}


def candidates(root):
    """Use Git's candidate set, including force-added ignored files, when available."""
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            check=True, capture_output=True,
        )
        return sorted(set(result.stdout.decode("utf-8").strip("\0").split("\0")) - {""})
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                  if (p.is_file() or p.is_symlink()) and "__pycache__" not in p.parts)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def text_list(value):
    return isinstance(value, list) and bool(value) and all(nonempty(v) for v in value)


def safe_reference(value, names):
    return (nonempty(value) and "\\" not in value and
            not PurePosixPath(value).is_absolute() and ".." not in PurePosixPath(value).parts
            and value in names)


def check_contract(name, data, names):
    errors = []
    kind = ("config" if name == "config/stronghold.example.json" else
            "agent" if name.startswith("agents/") else
            "lesson" if name == "examples/lesson.synthetic.json" else
            "room" if name == "examples/room-reset.synthetic.json" else None)
    if kind is None:
        return ["unsupported JSON contract; review before extending"]
    if not isinstance(data, dict) or set(data) != FIELDS[kind]:
        return ["fields do not match the documented template"]
    if type(data["version"]) is not int or data["version"] != 1:
        errors.append("version must be integer 1")
    if kind == "config":
        if data["timezone"] != "America/Detroit" or data["data_policy"] != "synthetic-only":
            errors.append("configuration must retain synthetic-only defaults")
        if data["integrations_enabled"] is not False:
            errors.append("integrations must be disabled")
        refs = data["agents"]
        if (not text_list(refs) or len(refs) != len(set(refs)) or
                set(refs) != {n for n in names if n.startswith("agents/") and n.endswith(".json")}):
            errors.append("agent references must cover the available profiles exactly")
    elif kind == "agent":
        if data["enabled"] is not False or data["invocation"] != "manual" or data["mode"] != "draft-only":
            errors.append("agent must remain disabled, manual and draft-only")
        if data["tools"] != []:
            errors.append("tools must be empty")
        if not all(nonempty(data[k]) for k in ("id", "owner_role", "review")):
            errors.append("agent description fields must be nonempty text")
        for key, prefix, suffix in (("prompt", "prompts/", ".md"),
                                    ("example_input", "examples/", ".synthetic.json")):
            value = data[key]
            if not safe_reference(value, names) or not value.startswith(prefix) or not value.endswith(suffix):
                errors.append(f"{key} reference must point to a tracked public template")
    else:
        if data["synthetic"] is not True:
            errors.append("synthetic must be true")
        minutes = data["duration_minutes" if kind == "lesson" else "prep_minutes"]
        if type(minutes) is not int or not 1 <= minutes <= 180:
            errors.append("minutes must be an integer from 1 to 180")
        for key in ("materials", "unknowns"):
            if not text_list(data[key]):
                errors.append(f"{key} must be a nonempty list of text")
        texts = ("scenario", "source", "target", "starting_point", "choice", "access_support", "cleanup", "reentry") if kind == "lesson" else ("scenario", "observation", "goal")
        if not all(nonempty(data[key]) for key in texts):
            errors.append("scenario fields must be nonempty text")
        if kind == "lesson":
            if data["standard"] is not None:
                errors.append("synthetic example standard must remain unverified (null)")
            steps = data["steps"]
            if not isinstance(steps, list) or not steps or not all(
                isinstance(step, dict) and set(step) == {"do", "look", "check"}
                and all(nonempty(v) for v in step.values()) for step in steps
            ):
                errors.append("steps need nonempty do, look and check fields")
    return errors


def validate(root):
    root = root.resolve()
    try:
        names = set(candidates(root))
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return ["repository: cannot inspect candidate files"]
    errors = [f"{name}: missing required file" for name in sorted(REQUIRED - names)]
    for name in sorted(names):
        path = root / name
        parts = PurePosixPath(name).parts
        problems = []
        if (PRIVATE_PARTS.intersection(parts) or path.name.startswith(".env") or
                path.name.endswith(".local.json") or re.search(r"credentials|secrets", name, re.I)):
            errors.append(f"{name}: private path must not be published")
            continue
        # Check ancestors too: do not follow a directory symlink into private files.
        if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
            errors.append(f"{name}: symlink is not allowed")
            continue
        if path.suffix not in ALLOWED_SUFFIXES and name != ".gitignore":
            errors.append(f"{name}: unsupported file type")
            continue
        try:
            if path.stat().st_size > 200_000:
                errors.append(f"{name}: file exceeds starter size limit")
                continue
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"{name}: missing or unreadable UTF-8 file")
            continue
        if CREDENTIAL.search(content):
            problems.append("possible credential; inspect privately")
        if PRIVATE_LINK.search(content):
            problems.append("private link must not be published")
        if any(domain.lower() not in {"example.com", "example.org", "example.net"} for domain in EMAIL.findall(content)):
            problems.append("contact address outside reserved example domains")
        if path.suffix == ".json":
            try:
                data = json.loads(content, object_pairs_hook=unique_object)
                problems.extend(check_contract(name, data, names))
            except ValueError:
                problems.append("invalid JSON or duplicate keys")
        if path.suffix == ".py":
            try:
                ast.parse(content)
            except SyntaxError:
                problems.append("invalid Python syntax")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^\s)]+)\)", content):
                if target.startswith(("https://", "http://", "mailto:", "#")):
                    continue
                destination = (path.parent / target.split("#", 1)[0]).resolve()
                if not destination.is_relative_to(root) or not destination.exists():
                    problems.append("broken or escaping local Markdown link")
                else:
                    relative = destination.relative_to(root).as_posix()
                    prefix = "" if relative == "." else relative + "/"
                    if relative not in names and not (destination.is_dir() and any(n.startswith(prefix) for n in names)):
                        problems.append("local Markdown link targets a file excluded from publication")
        errors.extend(f"{name}: {problem}" for problem in problems)
    return errors


if __name__ == "__main__":
    if sys.version_info < (3, 11):
        raise SystemExit("Python 3.11 or newer is required")
    findings = validate(Path(__file__).resolve().parents[1])
    if findings:
        print("FAIL: starter validation")
        print("\n".join(findings))
        raise SystemExit(1)
    print("PASS: starter structure, templates, syntax, links and basic public-data checks")
