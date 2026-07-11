---
name: trace-requirements-to-tests
description: Every requirement, rule, or acceptance criterion a spec or design states MUST be traceable to at least one test that would fail if it were violated, through a mechanically checkable link — a shared identifier the test names, not a human's claim of coverage. Use when building from a spec, PRD, design doc, constitution, or numbered requirements; when a requirements artifact and a test suite both exist and you need to find requirements with no test (verification gaps) or tests tied to no requirement (scope drift); before trusting a green suite as evidence the spec is met. Not for exploratory or brownfield work with no stated spec (there the recovered characterization tests are the spec), and not for whether the design is complete enough to trace to in the first place — that is design-completeness; this rule starts once requirements are stated and checks that each carries a test.
---

# trace-requirements-to-tests

## Statement

Every requirement a spec states MUST map to at least one test that would fail if the requirement were violated, and the mapping MUST be mechanically checkable — a shared identifier the test names, not a human's claim that it is covered. A requirement with no such test is unverified. The reverse — a test that maps to no requirement — is scope drift or an unstated requirement; surface both.

## Why

A green suite only tells you the tests that exist pass. It is silent about a requirement that has no test at all: the suite is green, the requirement is unmet, and nothing makes the absence visible. It is the green-but-wrong failure the adequacy gates fight, moved up one level — from "this test does not bite" to "this requirement has no test." Line coverage cannot catch it: it counts executed lines, not requirements met, which is the same reason line coverage is a weak quality signal (see [mutation-grading](../mutation-grading/SKILL.md)). The link has to be mechanical because a reviewer reading "yes, that's covered" cannot tell a true claim from a false one — only a resolvable identifier can.

This is the design→test direction of provenance. [keep-properties-honest](../keep-properties-honest/SKILL.md) requires every property to cite a design source (test→design); this rule requires every design source to carry a test (design→test). Run both and the design↔test mapping is complete in both directions: nothing in the spec ships untested, and nothing in the suite is sourced from the code it tests.

## When this applies

- You are building from a stated spec: a PRD, acceptance criteria, a design doc, a numbered requirements list, a constitution.
- A requirements artifact and a test suite both exist and you need the gaps between them.
- Before trusting a green suite as evidence the spec is met.
- **Skip — explicitly, never silently** — when there is no stated spec to trace to. In exploratory or brownfield work the recovered characterization tests *are* the spec ([characterize-before-change](../characterize-before-change/SKILL.md)); this rule starts once requirements are stated.

## The check (mechanical)

1. **Enumerate** the requirements and give each a stable id (`R-001`, `AUTH-3`, a constitution clause number).
2. **Bind** each test to the requirement id(s) it verifies — in the test name, a tag/marker, a docstring, or a traceability map kept beside the suite.
3. **Resolve** mechanically: for each requirement id, search the test tree for a reference.
4. **Report two lists:** requirements with zero referencing tests (verification gaps), and tests referencing no requirement (scope drift or an unstated requirement).
5. **Route every gap:** each verification gap is either closed (write the test) or accepted by the operator with a recorded reason. Never leave it silent — an unrecorded gap reads identically to a covered requirement.

## Anti-pattern (do not do this)

A requirements doc and a test suite with no shared identifier between them, plus an assertion that everything is tested:

```
requirements.md:  "The cart rejects an order of more than 50 items."
tests/:           def test_cart_rejects_too_many(): ...   # no requirement id anywhere
# Nothing links the two. Delete or reword the requirement and not one test fails to notice.
# "We have 92% line coverage" is not evidence this requirement is met.
```

## Correct pattern

```
# requirements.md
R-014  The cart rejects an order of more than 50 items.

# tests/test_cart.py
def test_rejects_order_over_limit():        # verifies: R-014
    ...

# check (deterministic): every requirement id is referenced by some test
for id in $(grep -oE 'R-[0-9]+' requirements.md); do
  grep -rq "$id" tests/ || echo "GAP: $id has no test"
done
```

*(Illustrative; the rule is language- and tool-agnostic. The id scheme and the search are whatever the project already uses.)*

## Mechanical enforcement

A CI step parses requirement ids from the spec, searches the test tree for each, and fails — or warns — on any requirement with no referencing test, and lists any test bound to no requirement. Deterministic, with no model in the loop, which is exactly what lets it gate a build where a stochastic "did we cover everything?" review cannot. Advisory while ids are being adopted; blocking once the requirement set carries ids.

## Related

- [keep-properties-honest](../keep-properties-honest/SKILL.md) — the test→design direction (provenance); this is the design→test direction (coverage). The pair makes the design↔test mapping complete both ways.
- [mutation-grading](../mutation-grading/SKILL.md) — why a coverage number is not evidence the tests bite; this rule measures requirement-coverage, a different and necessary thing.
- [boundary-tests](../boundary-tests/SKILL.md), [no-op-paths](../no-op-paths/SKILL.md) — sibling adequacy gates for per-method test gaps; this one is spec-level.
