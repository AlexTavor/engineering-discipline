#!/usr/bin/env bash
# End-to-end verification of the engineering-discipline plugin hooks.
#
# Spins up a nested, headless Claude Code session that loads THIS plugin, has it
# write a test file, and checks that both hooks fire the way Claude Code runs
# them (not just that the scripts work in isolation):
#
#   SessionStart -> injects the standing SOP directive
#   PostToolUse  -> surfaces the test-adequacy reminder when a test file is written
#
# It proves the parts unit tests cannot: that hooks.json loads, that
# ${CLAUDE_PLUGIN_ROOT} expands, that the real stdin schema matches, and that our
# output reaches the model.
#
# Run it from an interactive shell where `claude` is logged in. (A claude spawned
# as a child of another Claude Code SDK session cannot reuse that session's OAuth,
# so the model leg 401s there; this script detects and reports that case.)
#
#   bash scripts/verify-hooks.sh
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WS="$(mktemp -d)"
LOG="$WS/debug.log"
trap 'rm -rf "$WS"' EXIT

if ! command -v claude >/dev/null 2>&1; then
  echo "FAIL: 'claude' not on PATH"; exit 2
fi

echo "plugin : $REPO"
echo "workdir: $WS"
echo "running nested headless claude (loads the plugin, writes a test file)..."

( cd "$WS" && claude -p \
    "Create a file named billing.test.ts containing one trivial Jest test that asserts 1 + 1 === 2. Then, in a final line beginning 'SOP-SEEN:', state whether any engineering-discipline standing directive is present in your context (yes/no)." \
    --plugin-dir "$REPO" \
    --permission-mode acceptEdits \
    --debug --debug-file "$LOG" \
    --output-format text ) > "$WS/out.txt" 2>&1

pass=0; fail=0
check() { # label ; condition already evaluated into $1==ok/no
  if [ "$2" = "ok" ]; then echo "  PASS  $1"; pass=$((pass+1)); else echo "  FAIL  $1"; fail=$((fail+1)); fi
}

echo
echo "results:"

# Auth reachable?
if grep -qiE '401|Invalid authentication|Failed to authenticate' "$WS/out.txt" "$LOG" 2>/dev/null; then
  auth=no; else auth=yes; fi

# 1. plugin hooks registered
grep -qE 'Registered [0-9]+ hooks from' "$LOG" && r1=ok || r1=no
check "plugin hooks registered by Claude Code" "$r1"

# 2. SessionStart fired + additionalContext accepted (mechanism proof, no model needed)
grep -qE 'session-directive\.py.*additionalContext|SessionStart.*success' "$LOG" && r2=ok || r2=no
check "SessionStart injected the standing directive" "$r2"

if [ "$auth" = "no" ]; then
  echo
  echo "  NOTE  model API was not reachable from this process (401 / OAuth)."
  echo "        SessionStart above still proves hooks.json loads, \${CLAUDE_PLUGIN_ROOT}"
  echo "        expands, and additionalContext is consumed. To exercise PostToolUse,"
  echo "        run this script from a normal logged-in terminal, not as a child of"
  echo "        another Claude Code session."
  echo
  echo "summary: $pass passed, $fail failed, PostToolUse skipped (no model auth)"
  exit 0
fi

# 3. the test file was actually written (model made the tool call)
[ -f "$WS/billing.test.ts" ] && r3=ok || r3=no
check "model wrote billing.test.ts (tool call happened)" "$r3"

# 4. PostToolUse fired for that write and produced our reminder
grep -qE 'sop-reminder\.py.*additionalContext' "$LOG" && r4a=ok || r4a=no
grep -qiE 'test-adequacy|assert-by-shape|boundary-tests' "$LOG" && r4b=ok || r4b=no
[ "$r4a" = ok ] || [ "$r4b" = ok ] && r4=ok || r4=no
check "PostToolUse surfaced the test-adequacy reminder" "$r4"

echo
echo "summary: $pass passed, $fail failed"
[ "$fail" -eq 0 ] || { echo; echo "debug log: $LOG (not deleted)"; trap - EXIT; }
[ "$fail" -eq 0 ]
