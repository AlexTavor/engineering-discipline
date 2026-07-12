---
name: characterize-before-change
description: Before changing code you don't fully trust — legacy, inherited, or AI-generated — pin its current behavior in tests first, so a regression turns them red and the tests become the recovered spec. Hold those characterization tests to the same adequacy bar as any other (boundary, no-op, value-pinning) — an example-shaped characterization locks nothing. Use before any refactor or rewrite of code whose behavior is written down nowhere but the code itself. For proving a change didn't drift over the whole output (replay / golden-master), reach for reproducibility-baseline.
source: "recovered from git: chdr 7f56740, ef5a64b; PDD 1ab0a1f, 395ba1c, d4ad74e"
---

# characterize-before-change

## Statement

Before you touch code whose behavior you can't fully trust, you MUST pin its current behavior in tests that would fail if that behavior changed — captured against the code *as it is*, before you edit. Those tests are your safety net (a regression turns them red) and your recovered spec (the only written record of what the code actually does). Hold them to the same adequacy bar as any other test: an example-shaped characterization locks nothing.

## Why

In brownfield work the code is the only source of truth — there is no spec to diff a change against. Change first and test later, and you've lost the baseline: you cannot prove the change preserved behavior, because you never captured what the behavior was.

And a characterization test only protects you if it bites. An example-shaped one that asserts the happy path locks nothing — the behavior change hides in the boundary, the no-op branch, or the value you didn't pin.

The classic miss: a team pins a pricing function it doesn't trust with three characterization tests, all at typical inputs. A refactor changes the rounding at the `.5` boundary; every test stays green, because none sits at the boundary. The suite handed them the confidence to ship the exact behavior change they meant to rule out.

## When to apply

- Before any refactor or rewrite of code you don't fully trust.
- Before deleting or rewriting a function whose call paths you haven't fully traced.
- Whenever the only spec is the code itself — legacy, inherited, AI-generated.

## Protocol

1. **Capture current behavior first** — write the tests against the code *as it is*, and run them green, before you edit anything. If you've already started changing it, revert and pin first; a baseline captured after the change is not a baseline.
2. **Source the cases by reading** ([read-the-system](../read-the-system/SKILL.md)) and from the ranked risk register your assessment produced — not from what you assume the code does.
3. **Hold them to the adequacy bar** — boundary, no-op, value-pinning, the documented negatives and edges. An example-shaped characterization test locks nothing.
4. **Lock found bugs, don't bless them.** Characterization pins current behavior *including* its bugs — correct — but a bug you discover gets flagged and routed (an expected-fail test asserting the right behavior), not silently canonized.
5. **Keep them as the recovered spec** — name and place them so the next person reads them as the documentation of what this code does.

## Anti-patterns

1. **Change-then-test.** Tests written after the edit can't prove preservation against a baseline you never captured.
2. **Happy-path characterization.** Pinning only typical inputs; the change hides at the boundary / no-op / edge you skipped.
3. **Restate-the-implementation.** A test that re-computes the code's own logic and asserts the two match passes by construction — it can't fail when the code is wrong.

## Mechanical enforcement

Partly checkable. Coverage shows what's exercised; mutation grading ([mutation-testing](../mutation-testing/SKILL.md)) shows whether the characterization actually bites — a suite that survives mutants isn't pinning behavior. But "did you pin *before* you changed" is a process discipline — the git history (test commit before change commit) shows it, not a lint.

## Related

- [reproducibility-baseline](../reproducibility-baseline/SKILL.md) — the other half of locking behavior: proving a change didn't drift.
- [boundary-tests](../boundary-tests/SKILL.md), [no-op-paths](../no-op-paths/SKILL.md) — the adequacy bar a characterization test is held to.
- [read-the-system](../read-the-system/SKILL.md) — source the cases by reading, not assuming.
- [mutation-testing](../mutation-testing/SKILL.md) — grades whether the characterization suite bites.
