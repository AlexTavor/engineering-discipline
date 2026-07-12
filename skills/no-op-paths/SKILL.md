---
name: no-op-paths
description: For any method that mutates state conditionally (cleanup, eviction, pruning, GC, expiry, retraction, compaction, vacuum), the test suite MUST contain a test where the trigger condition is NOT met and post-state equals pre-state. Use when authoring tests for prune_* / evict_* / expire_* / gc_* / cleanup_* / compact_* / vacuum_* methods.
source: "recovered from git: chdr 36146b1, 23606ac; PDD 9004289, 43b7a2d, ad56541"
---

# no-op-paths

## Statement

Any method that mutates state *conditionally* (cleanup, eviction, pruning, GC, expiry, retraction, compaction, vacuum) MUST have at least one test where the trigger condition is NOT met. Post-state MUST equal pre-state.

## Why

Re-implementors write the "do the work" branch correctly and frequently *omit the gate that protects the no-op branch*. The result is an over-aggressive impl that mutates every call regardless of whether the condition held. This is by far the most common failure mode for cleanup-shaped methods, and it does not surface in any test that only exercises the trigger-met case.

Worked case: a lock registry's `prune_stale()`. The contract pinned only the "stale lock removed" path, so the impl shipped a `for path in holds: del holds[path]` sweep — every healthy lock died, and no test caught it.

## Indicators a method needs a no-op test

- Name matches `prune_* / evict_* / expire_* / gc_* / cleanup_* / compact_* / vacuum_*`.
- Docstring describes a *condition* under which it mutates ("older than", "past TTL", "stale", "expired").
- Takes no value arguments (acts on internal state); both branches need tests.
- Returns a count of items affected (the count when nothing was eligible MUST be tested).

## Minimum coverage (three tests)

1. **Trigger met → mutation happens.** State satisfies the condition; the affected entries change.
2. **Trigger NOT met → no-op.** State does not satisfy the condition; post-state equals pre-state, return value indicates zero work.
3. **Mixed state → discrimination.** Some entries satisfy, some don't; only the matching subset mutates.

Test (2) is *the cheap one* — call the method on freshly-initialized state. Always cheap, always required, almost always missing.

## Anti-pattern (do not do this)

```python
# WRONG — pins only the active path; a clear-everything impl passes it
def test_prune_removes_stale():
    reg = LockRegistry(stale_after=60); reg.acquire("/x")
    advance_clock(120); reg.prune_stale()
    assert not reg.is_locked("/x")
```

## Correct pattern

```python
def test_prune_leaves_healthy_alone():
    reg = LockRegistry(stale_after=60); reg.acquire("/x")
    reg.prune_stale()                      # no clock advance; lock is fresh
    assert reg.is_locked("/x"), "no-op required when nothing is stale"

def test_prune_returns_zero_when_nothing_pruned():
    reg = LockRegistry(); reg.acquire("/x")
    assert reg.prune_stale() == 0
```

*(Examples are Python; the rule is language-agnostic.)*

## Mechanical enforcement

An AST lint can flag any test file referencing a `prune_*` / `evict_*` / etc. method whose tests lack a `no_op` / `leaves_alone` / `idempotent` token. Advisory at first; blocking once established.

## Related

- [boundary-tests](../boundary-tests/SKILL.md) — the other re-implementor failure mode.
