---
name: fix-what-you-find
description: When a refactor, a review, or a test-adequacy pass surfaces a real defect — a bug, a gap, a surviving mutant, a swallowed error — close it, don't preserve-and-note it. Behavior-preservation is the right default for a refactor, but it yields to correctness the moment the behavior you would preserve is a bug; the discipline is to fix it and call out the change where reviewers will see it, not to re-implement the bug behind a TODO. Use when a "pure refactor" turns up a latent defect, when characterization reveals current behavior is wrong, or when you catch yourself commenting a problem instead of fixing it. Not a license to scope-creep.
---

# fix-what-you-find

## Statement

When work you are doing surfaces a genuine defect, fix it — and surface the fix. "Preserve behavior" is the correct reflex for a mechanical refactor and the wrong one the instant the behavior you would preserve is a bug. A found defect is either closed now, with the behavior change called out where reviewers will see it, or — if closing it is genuinely out of scope — filed as tracked work. It is never faithfully re-implemented with a comment noting that it is broken.

## Why

A bug preserved-and-noted is a bug shipped, now wearing a comment that makes it look deliberate. And the person best placed to fix a defect is the one who just read the code closely enough to find it; deferring hands the fix to someone with none of that context, behind a TODO that tends to outlive everyone who could act on it. "Behavior-preserving" is a means — don't break working code — not an end. When the behavior is wrong, preserving it protects nothing worth protecting.

Worked case: refactoring a discount calculator reveals the old code applied the cap *before* tax instead of after, understating every total. Preserving it means re-implementing the wrong order and adding `// legacy: cap applied pre-tax`. Fixing it means correcting the order and writing, in the PR, "behavior change: cap now applied post-tax; prior order was a bug, see test X." The second is the entire payoff of having read the code.

## When to apply

- A refactor surfaces a latent bug in the code being moved.
- [characterize-before-change](../characterize-before-change/SKILL.md) reveals current behavior is wrong.
- A surviving mutant ([mutation-grading](../mutation-grading/SKILL.md)) exposes logic that is both untested and incorrect.
- A [silent-failure-census](../silent-failure-census/SKILL.md) finds a swallowed error that actually matters.
- You are about to write a comment describing a problem instead of fixing the problem.

## Fix, but keep it separate

Fixing what you find is not license to add features or re-architect. Close the specific defect, keep it reviewable — its own commit, its own line in the PR description — and let a genuinely large fix become tracked work rather than riding hidden inside an unrelated diff. The rule is fix-what-you-find, not rewrite-what-you-touch. The two failures are symmetric: preserving a known bug is one, smuggling an unreviewable rewrite in beside the fix is the other.

## Interaction with characterize-before-change

These do not conflict. Characterization pins current behavior *including its bugs* so you have a baseline to prove your change against. When it reveals a bug, you pin the buggy behavior **and** add a failing test asserting the correct behavior, then fix — so the diff proves the fix is the only change. Pinning the bug is how you make the fix provable; it is not a decision to keep the bug.

## Anti-patterns

1. **Preserve-and-note.** Re-implementing a known bug faithfully with a TODO or comment — the defect ships, dressed as considered.
2. **Silent fix.** Correcting a behavior without telling reviewers — the opposite failure; a fix nobody was told about is a change nobody reviewed.
3. **Scope-creep.** Using a found bug as cover for unrelated rework the diff was never meant to carry.

## When NOT to use

If the "behavior" is a contract other code deliberately relies on rather than a bug, changing it is a breaking change, not a drive-by fix — route it as a decision, not an in-passing edit. And a mechanical refactor that surfaces nothing wrong stays behavior-preserving; this rule triggers on a real found defect, not on the general urge to improve code you happen to be near.

## Mechanical enforcement

Not lintable — "is this preserved behavior a bug or a contract?" is judgment. Enforced in review: a diff that adds a comment documenting a defect, or a characterization test named for behavior that reads as wrong, is the cue to ask "why note it instead of fixing it?"

## Related

- [characterize-before-change](../characterize-before-change/SKILL.md) — pin the bug, add the failing test for the right behavior, then fix; don't bless it.
- [mutation-grading](../mutation-grading/SKILL.md) — a surviving mutant is often a found defect, not just a missing test.
- [silent-failure-census](../silent-failure-census/SKILL.md) — swallowed errors you turn up are candidates to close, not just to catalogue.
- [cohesion-review](../cohesion-review/SKILL.md) — carve the duplication you find rather than noting it; the same close-it-now reflex, pointed at structure.
