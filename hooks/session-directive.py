#!/usr/bin/env python3
"""SessionStart hook: inject the engineering-discipline standing SOP directive
into the session context, so the discipline skills are applied by reflex while
working on code rather than only when explicitly asked.

Emits hookSpecificOutput.additionalContext (the documented channel for adding
context). Fails open: any error prints nothing and exits 0, never blocking a
session.
"""
import os
import sys
import json


def main() -> None:
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not root:
        # Fall back to this file's plugin root: hooks/ -> plugin root.
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directive_path = os.path.join(root, "hooks", "SOP-DIRECTIVE.md")
    try:
        with open(directive_path, "r", encoding="utf-8") as handle:
            text = handle.read().strip()
    except OSError:
        sys.exit(0)
    if not text:
        sys.exit(0)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": text,
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Never let a context hook break a session.
        sys.exit(0)
