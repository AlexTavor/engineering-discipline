---
name: mutation-testing
description: Assessing whether a test suite catches bugs when line coverage is high but you do not trust it: grade the suite by injecting small bugs (mutants) and checking the tests fail on them, which coverage alone cannot. "Are my tests any good, do they catch bugs?" Every surviving mutant (an injected bug no test caught) is either a weak test (add a property or case) or dead code (delete it), so read each survivor before trusting the count. Use on engines, compilers, or parsers, and whenever a mutation run reports survivors.
source: "recovered from git: chdr b34409a, 6896469; PDD eefc0b1, ae0e9be"
---

# mutation-testing

## Statement

Grade a suite by injecting small bugs — mutants — and checking the tests catch them. A mutant the tests don't catch (a *survivor*) marks a place the suite doesn't actually constrain. It is the only check that grades the tests themselves rather than the code.

## Why

Line coverage tells you a line *ran*, not that a test would *fail* if the line were wrong. A suite can have 90% coverage and assert almost nothing — every line executed, no behavior pinned. Mutation closes that gap: if flipping `>` to `>=`, or deleting a branch, or returning a constant leaves every test green, the tests don't bite there.

## Triage every survivor

This is the step most people skip, and the count lies without it. A survivor is one of two things — read it (see [read-the-system](../read-the-system/SKILL.md)) and classify:

1. **Weak test.** The behavior is real and the suite just doesn't pin it. *Fixable* — add a [property](../property-based-testing/SKILL.md) or a case. This is the survivor worth chasing.
2. **Dead or inert code.** The mutated code can't change any observable output — it's unreachable, subsumed by an earlier check, or normalizes away. *No test can kill it*, because there's nothing to observe. The fix is to delete the code, not to write a test.

Worked case: a module showed seventeen survivors and looked like the richest target on the scoreboard. Reading them, sixteen were dead code — a predicate subsumed by an earlier check, sentinels that couldn't collide, an unused field. Counts mislead; the triage is the real output.

## How to run it

1. **Scope it.** Run mutation per module (`--mutate '<path>'`) so each test's effect is measured in isolation, before and after.
2. **Triage every survivor** into weak-test vs dead-code by reading it.
3. **Act on the split:** weak test → add a property/case and re-run to confirm the kill; dead code → route it for deletion (it's a cleanup, not a test gap).
4. **Hold the bar.** When a real survivor is hard to kill, strengthen the test — don't lower the threshold to make the number go green.

## Anti-patterns

1. **Count-without-reading.** Treating the survivor count as a to-do list. Until you've read them, you don't know which are killable.
2. **Lower-the-bar.** Dropping the threshold so the score passes. That hides exactly what the gate exists to show.
3. **Expecting a test to kill dead code.** No test kills an inert mutant; writing one to try is wasted effort. Delete the code instead.
4. **Score-chasing on a hardened subsystem.** Past a point, residual survivors are mostly dead code. There, mutation's value is behavior-lock and cleanup, not a higher number.

## Mechanical enforcement

Once established, mutation runs as a gate with a break threshold (e.g. 90%). Advisory while you burn down the first survivors; blocking once the suite is strong enough that new survivors mean new weakness.

## Related

- [property-based-testing](../property-based-testing/SKILL.md) — the strongest way to kill a weak-test survivor.
- [read-the-system](../read-the-system/SKILL.md) — how to classify a survivor (read it, don't count it).
