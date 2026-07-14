---
name: boundary-tests
description: You are writing tests for code that compares a value against a limit (less-than, less-or-equal, greater-than, greater-or-equal): the suite MUST include a case exactly at the boundary, x equal to the limit, not only values on either side, since that equality case is what pins which operator is correct. Covers cost ceilings, retry counts, timeouts, age thresholds, any numeric-boundary comparison. Plain cue: "did I test the value right at the limit?" This is for authoring a test at the limit value, not design-review of edge cases (that is design-completeness).
source: "recovered from git: chdr 36146b1, 86d34c3; PDD 43b7a2d, 299e638"
---

# boundary-tests

## Statement

Any predicate `x op limit` where `op` is one of `<`, `<=`, `>`, `>=` MUST have a dedicated test at `x == limit`, not only on either side of the boundary. The equality case is the test that pins which operator is canonical.

## Why

Re-implementors — model or human — plausibly pick the wrong operator when the equality boundary isn't asserted. Spec text like "exceeds the ceiling", "above the threshold", "past the limit" is genuinely ambiguous between `>` and `>=`. Without an explicit `==` test, both interpretations pass every "strictly above" assertion, and the impl ships with the wrong operator.

Worked case: a budget ledger whose rule was "reserving *at or above* the cap raises". The contract pinned only strictly-above cases, so `reserve(10.0, cap=10.0)` *not* raising slipped through — the impl picked `>` where the canonical rule was `>=`.

## Indicators a method needs a boundary test

- It raises / returns False / takes an alternate path when an input crosses a numeric limit (cost ceiling, retry count, timeout, age threshold).
- The spec describes the behaviour with "exceeds / above / past / beyond / below / under" without specifying `==` semantics.
- It has a sibling `_can_*` / `_should_*` / `_is_*` predicate using the same boundary value.
- Equality at the boundary is cheap to test but rarely tested. (If you find yourself writing `reserve(11, cap=10)` instead of `reserve(10, cap=10)`, ask why.)

## Minimum coverage

For each boundary, two tests:

1. `x == limit` — pins the operator.
2. `x == limit ± epsilon` on the "OK" side — pairs with (1) to discriminate `>` from `>=` (or `<` from `<=`).

## Anti-pattern (do not do this)

```python
# WRONG — passes whether the impl uses > or >=
with pytest.raises(BudgetExhaustedError):
    ledger.reserve(11.0, cap=10.0)   # 11 > 10 AND 11 >= 10
```

## Correct pattern

```python
def test_reserve_at_exactly_cap_raises():
    with pytest.raises(BudgetExhaustedError):
        ledger.reserve(10.0, cap=10.0)        # 10 == 10; only >= raises

def test_reserve_just_below_cap_succeeds():
    ledger.reserve(9.999_999, cap=10.0)       # < 10; OK side
```

*(Examples are Python; the rule is language-agnostic.)*

## Mechanical enforcement

An AST test-quality lint can count `==`-boundary tests per method whose name or docstring carries a boundary phrase. Advisory at first; blocking once the rule is established.

## Related

- [no-op-paths](../no-op-paths/SKILL.md) — the other re-implementor failure mode boundary tests don't address.
