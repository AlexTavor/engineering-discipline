---
name: keep-properties-honest
description: A property suite can be all-green and still prove nothing: the tautological property passes because it was written by reading the same code it tests. Guard against it with three checks — source every property from the design or a written constraint (never from the implementation), have a separate pass try to beat the suite with a deliberately wrong implementation, and stop on any counterexample to classify it instead of quietly weakening the property. Use before trusting a green property suite, in property review, or whenever a property passes too easily — mutation grading cannot catch this for you.
source: "recovered from git: chdr 8bc1230, 3435cc7; PDD d40159e, e10352c, b662455"
---

# keep-properties-honest

## Statement

A property is only as trustworthy as where it came from and how hard it's been pushed. Three guards keep a green property suite meaningful: source from design, try to beat it, and stop on a counterexample.

## Why

Mutation grading has one blind spot it can't see past: the **tautological property** — one that passes even when the code is wrong, because it was written by reading that same code. It restates the implementation, so the implementation always satisfies it, mutants and all. These three guards close that hole, because no amount of grading will.

## When to apply

Run these before signing off on a property suite. Run guard 2 (try to beat it) at least once per subsystem, and look hard at any property that has passed from the day it was written without ever once failing.

## The three guards

### 1. Source from the design, not the implementation

Write each property from the spec, a constraint, a decision record, or a footgun — something that says what the code *should* do. A property derived from reading the code just encodes what it *does*, and passes even when that's wrong.

If you can't cite a source, mark the property unverified rather than trusting it. Cite it inline (`[constraint: …]`, `[decision: …]`, a footgun, an LLD section) so a reviewer can check the property against its source, not against the code.

Worked case: a design doc described a rewrite informally as replacing the *first* `.value`, while the code anchored to the *trailing* one. A property copied from the code would have locked the bug in. Sourcing it from the stated *intent* — and flagging the loose wording for clarification — made it a real test instead of a mirror.

### 2. Have something try to beat it

A separate pass — another agent or person — writes a deliberately wrong implementation and runs it against the properties. Anything that still passes reveals a property you're missing. It's the adversarial complement to mutation: it perturbs the code *intelligently*, aiming at gaps a random mutant won't hit.

### 3. Stop on a counterexample — classify, never quietly weaken

When a property fails, halt and classify it: a real bug, a wrong property, or a gap in the spec. Each routes differently — fix the code, fix the property, or clarify the spec. What you never do is loosen the property until it goes green; that converts a finding into a silent regression.

A clean way to hold a found bug without auto-fixing it: assert the *correct* behavior in a test marked expected-fail. The suite stays green today, and the test flips to a real failure the moment someone fixes the code.

## Anti-patterns

1. **Provenance-from-implementation.** A property read off the code — the tautology trap, and the single most common way a property suite lies.
2. **Skip-the-beat.** Never running an adversarial pass, so the gaps no random mutant happens to hit stay invisible.
3. **Auto-relax / silent-fix.** Making a failure go away without classifying it — weakening the property, or quietly changing the code it caught. Either way the finding is lost.

## Related

- [property-based-testing](../property-based-testing/SKILL.md) — what these guards protect.
- [mutation-testing](../mutation-testing/SKILL.md) — grades strength; these guard against tautology, its blind spot.
