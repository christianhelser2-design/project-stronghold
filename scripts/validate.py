"""Small, dependency-free checks for public starter files; not a privacy guarantee."""
import ast
import json
from pathlib import Path, PurePosixPath
import posixpath
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
AGENT_INPUTS = {
    "lesson-readiness": "examples/lesson.synthetic.json",
    "room-reset": "examples/room-reset.synthetic.json",
}
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
MARKDOWN_LINK = re.compile(r'''\]\(\s*([^\s)]+)(?:\s+(?:"[^"]*"|'[^']*'|\([^)]*\)))?\s*\)''')
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


def staged_files(root):
    """Return path, mode and blob ID from Git's index, without reading the worktree."""
    if not (root / ".git").exists():
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--stage", "-z"],
        check=True, capture_output=True,
    )
    files = {}
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, raw_name = entry.split(b"\t", 1)
        mode, object_id, stage = metadata.split(b" ")
        if stage != b"0":
            raise ValueError("unmerged index")
        files[raw_name.decode("utf-8")] = (mode, object_id.decode("ascii"))
    return files


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
        if not name.endswith(".example.json"):
            errors.append("agent profile filename must end in .example.json")
        else:
            profile_id = PurePosixPath(name).name.removesuffix(".example.json")
            if data["id"] != profile_id:
                errors.append("agent id must match profile filename")
            if data["prompt"] != f"prompts/{profile_id}.md":
                errors.append("prompt must match agent profile")
            if data["example_input"] != AGENT_INPUTS.get(profile_id):
                errors.append("example_input must match agent profile")
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


def path_problem(name):
    path = PurePosixPath(name)
    parts = {part.casefold() for part in path.parts}
    filename = path.name.casefold()
    if (PRIVATE_PARTS.intersection(parts) or filename.startswith(".env") or
            filename.endswith(".local.json") or re.search(r"credentials|secrets", name, re.I)):
        return "private path must not be published"
    if path.suffix not in ALLOWED_SUFFIXES and name != ".gitignore":
        return "unsupported file type"
    return None


def local_link_problem(root, name, target, names):
    if target.startswith(("https://", "http://", "mailto:", "#")):
        return None
    target = target.split("#", 1)[0]
    if root is None:
        relative = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
        if relative == ".." or relative.startswith(("../", "/")):
            return "broken or escaping local Markdown link"
        prefix = "" if relative == "." else relative + "/"
        if relative not in names and not any(n.startswith(prefix) for n in names):
            return "local Markdown link targets a file excluded from publication"
    else:
        destination = (root / PurePosixPath(name).parent / target).resolve()
        if not destination.is_relative_to(root) or not destination.exists():
            return "broken or escaping local Markdown link"
        relative = destination.relative_to(root).as_posix()
        prefix = "" if relative == "." else relative + "/"
        if relative not in names and not (destination.is_dir() and any(n.startswith(prefix) for n in names)):
            return "local Markdown link targets a file excluded from publication"
    return None


def content_problems(name, content, names, root):
    problems = []
    if CREDENTIAL.search(content):
        problems.append("possible credential; inspect privately")
    if PRIVATE_LINK.search(content):
        problems.append("private link must not be published")
    if any(domain.lower() not in {"example.com", "example.org", "example.net"} for domain in EMAIL.findall(content)):
        problems.append("contact address outside reserved example domains")
    suffix = PurePosixPath(name).suffix
    if suffix == ".json":
        try:
            data = json.loads(content, object_pairs_hook=unique_object)
            problems.extend(check_contract(name, data, names))
        except ValueError:
            problems.append("invalid JSON or duplicate keys")
    if suffix == ".py":
        try:
            ast.parse(content)
        except SyntaxError:
            problems.append("invalid Python syntax")
    if suffix == ".md":
        for target in MARKDOWN_LINK.findall(content):
            problem = local_link_problem(root, name, target, names)
            if problem:
                problems.append(problem)
    return problems


def validate(root):
    root = root.resolve()
    try:
        names = set(candidates(root))
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return ["repository: cannot inspect candidate files"]
    errors = [f"{name}: missing required file" for name in sorted(REQUIRED - names)]
    for name in sorted(names):
        path = root / name
        problem = path_problem(name)
        if problem:
            errors.append(f"{name}: {problem}")
            continue
        # Check ancestors too: do not follow a directory symlink into private files.
        if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
            errors.append(f"{name}: symlink is not allowed")
            continue
        try:
            if path.stat().st_size > 200_000:
                errors.append(f"{name}: file exceeds starter size limit")
                continue
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"{name}: missing or unreadable UTF-8 file")
            continue
        errors.extend(f"{name}: {problem}" for problem in content_problems(name, content, names, root))

    try:
        indexed = staged_files(root)
    except (OSError, subprocess.SubprocessError, UnicodeError, ValueError):
        return errors + ["repository: cannot inspect staged files"]
    if indexed is not None:
        index_names = set(indexed)
        errors.extend(f"staged {name}: missing required file" for name in sorted(REQUIRED - index_names))
        for name, (mode, object_id) in sorted(indexed.items()):
            problem = path_problem(name)
            if problem:
                errors.append(f"staged {name}: {problem}")
                continue
            if mode == b"120000":
                errors.append(f"staged {name}: symlink is not allowed")
                continue
            if mode not in {b"100644", b"100755"}:
                errors.append(f"staged {name}: unsupported file type")
                continue
            try:
                size = subprocess.run(["git", "-C", str(root), "cat-file", "-s", object_id],
                                      check=True, capture_output=True).stdout
                if int(size) > 200_000:
                    errors.append(f"staged {name}: file exceeds starter size limit")
                    continue
                content = subprocess.run(["git", "-C", str(root), "cat-file", "blob", object_id],
                                         check=True, capture_output=True).stdout.decode("utf-8")
            except (OSError, subprocess.SubprocessError, UnicodeError, ValueError):
                errors.append(f"staged {name}: missing or unreadable UTF-8 file")
                continue
            errors.extend(f"staged {name}: {problem}" for problem in
                          content_problems(name, content, index_names, None))
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
