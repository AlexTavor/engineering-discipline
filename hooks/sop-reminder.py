#!/usr/bin/env python3
"""PostToolUse hook: surface the matching engineering-discipline SOP at the
coding moment it applies.

Fires after Edit / Write / MultiEdit. Classifies the edited path and, when it
matches, injects a short reminder naming the discipline skill(s) to invoke:

  - a test file            -> the test-adequacy skills
  - unfamiliar source      -> read-the-system (and fix-what-you-find)
  - a code file grown past a language-aware, env-configurable line threshold
    (default 200) -> cohesion-review

Each category shows at most once per session (per file for cohesion), so the
reminders stay quiet. Fails open: any error prints nothing and exits 0.

Disable entirely by creating a `.no-engineering-sop` file in the project root,
or by removing this plugin's hooks/hooks.json.
"""
import os
import re
import sys
import json
import hashlib

# The cohesion-review reminder fires when an edited code file exceeds a line
# threshold. A single hardcoded number would be wrong for most stacks (200 lines
# of Python is large; 200 of Go or Java often is not), so the threshold is
# language-dependent and read from the environment:
#
#   ENGINEERING_DISCIPLINE_COHESION_MAX_LINES              global override
#   ENGINEERING_DISCIPLINE_COHESION_MAX_LINES_<LANGUAGE>   per-language override
#                                        (e.g. _PYTHON, _GO, _TYPESCRIPT, _JAVA)
#
# Resolution order: per-language env, then global env, then the default below.
DEFAULT_COHESION_MAX_LINES = 200

CODE_EXTENSIONS = (
    ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".rb", ".c",
    ".cc", ".cpp", ".h", ".hpp", ".cs", ".swift", ".kt", ".kts", ".scala",
    ".php", ".ex", ".exs", ".clj", ".cljs", ".sh", ".bash", ".m", ".mm",
    ".dart", ".lua", ".pl", ".r",
)

# Maps a file extension to a language token used as the per-language env-var
# suffix, so `.ts` and `.tsx` both read
# ENGINEERING_DISCIPLINE_COHESION_MAX_LINES_TYPESCRIPT. Keys stay in step with
# CODE_EXTENSIONS; an extension absent here falls back to the global default.
EXT_LANGUAGE = {
    ".py": "PYTHON",
    ".js": "JAVASCRIPT", ".jsx": "JAVASCRIPT",
    ".ts": "TYPESCRIPT", ".tsx": "TYPESCRIPT",
    ".go": "GO",
    ".rs": "RUST",
    ".java": "JAVA",
    ".rb": "RUBY",
    ".c": "C", ".h": "C",
    ".cc": "CPP", ".cpp": "CPP", ".hpp": "CPP",
    ".cs": "CSHARP",
    ".swift": "SWIFT",
    ".kt": "KOTLIN", ".kts": "KOTLIN",
    ".scala": "SCALA",
    ".php": "PHP",
    ".ex": "ELIXIR", ".exs": "ELIXIR",
    ".clj": "CLOJURE", ".cljs": "CLOJURE",
    ".sh": "SHELL", ".bash": "SHELL",
    ".m": "OBJC", ".mm": "OBJC",
    ".dart": "DART", ".lua": "LUA", ".pl": "PERL", ".r": "R",
}

TESTS_MSG = (
    "You are editing a TEST file. engineering-discipline test-adequacy SOPs apply, "
    "invoke the matching Skill(s) before you finish: assert-by-shape (compare the whole "
    "returned value against one fixture, not field by field), boundary-tests (a case exactly "
    "at each numeric limit), no-op-paths (a case where the trigger condition is not met and "
    "nothing changes), property-based-testing (generate over the input shape for parsers, "
    "validators, classifiers, and rule engines), and keep-properties-honest / mutation-testing "
    "when judging whether the suite would actually fail on a bug."
)

SOURCE_MSG = (
    "You are editing source code. If any of it is code you did not just write and do not fully "
    "trust (legacy, inherited, AI-generated), engineering-discipline SOP read-the-system applies: "
    "read the actual implementation before asserting how it behaves, since a name, type, or grep "
    "hit is a lead, not a fact. If you surface a real defect while here, apply fix-what-you-find "
    "rather than preserving-and-noting it."
)


def emit(message=None):
    if message:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": message,
            },
            "suppressOutput": True,
        }))
    sys.exit(0)


def is_test_path(path):
    base = os.path.basename(path).lower()
    low = path.lower()
    return bool(
        re.search(r"\.(test|spec)\.[a-z0-9]+$", base)
        or re.search(r"(^|/)test_[^/]+\.py$", low)
        or re.search(r"_test\.[a-z0-9]+$", base)
        or re.search(r"_spec\.[a-z0-9]+$", base)
        or re.search(r"(^|/)(tests?|__tests__|specs?)/", low)
    )


def marker_dir(session_id):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id or "nosession")
    path = os.path.join(
        os.environ.get("TMPDIR", "/tmp"), "engineering-discipline-sop", safe
    )
    os.makedirs(path, exist_ok=True)
    return path


def once(mdir, key):
    """Return True the first time `key` is seen this session, else False."""
    marker = os.path.join(mdir, hashlib.sha1(key.encode("utf-8")).hexdigest())
    if os.path.exists(marker):
        return False
    try:
        open(marker, "w").close()
    except OSError:
        pass
    return True


def line_count(path):
    try:
        with open(path, "r", errors="ignore") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return None


def _env_positive_int(name):
    raw = os.environ.get(name)
    if raw is None:
        return None
    try:
        value = int(raw.strip())
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None


def cohesion_threshold(path):
    """Line count above which cohesion-review is worth a reminder for this file.

    Language-dependent and env-configurable; a hardcoded universal number would
    misfire on most stacks. Resolution: per-language env, then global env, then
    DEFAULT_COHESION_MAX_LINES.
    """
    ext = os.path.splitext(path)[1].lower()
    language = EXT_LANGUAGE.get(ext)
    if language:
        per_language = _env_positive_int(
            "ENGINEERING_DISCIPLINE_COHESION_MAX_LINES_" + language
        )
        if per_language is not None:
            return per_language
    global_override = _env_positive_int("ENGINEERING_DISCIPLINE_COHESION_MAX_LINES")
    if global_override is not None:
        return global_override
    return DEFAULT_COHESION_MAX_LINES


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        emit()

    cwd = data.get("cwd") or os.getcwd()
    if os.path.exists(os.path.join(cwd, ".no-engineering-sop")):
        emit()

    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not path or not isinstance(path, str):
        emit()

    is_code = path.lower().endswith(CODE_EXTENSIONS)
    mdir = marker_dir(data.get("session_id", ""))
    reminders = []

    if is_test_path(path):
        if once(mdir, "tests"):
            reminders.append(TESTS_MSG)
    elif is_code:
        if once(mdir, "source"):
            reminders.append(SOURCE_MSG)

    if is_code:
        count = line_count(path)
        if count is not None and count > cohesion_threshold(path) and once(mdir, "cohesion:" + path):
            reminders.append(
                "%s is now %d lines. engineering-discipline SOP cohesion-review applies: read the "
                "WHOLE grown module fresh for a second responsibility, or two helpers that compute the "
                "same thing under different names, not just the lines your change touched."
                % (os.path.basename(path), count)
            )

    if reminders:
        emit("\n\n".join(reminders))
    emit()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Never let a reminder hook break the tool result.
        sys.exit(0)
