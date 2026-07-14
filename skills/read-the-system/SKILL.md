---
name: read-the-system
description: Read the actual implementation before you state, design against, or test how any code you did not just write behaves, especially legacy, inherited, or AI-generated code. A name, type, signature, schema, or grep hit is a lead, not a fact; in these codebases they routinely lie, so open the file and trace the real path before concluding. Fires whenever you are about to claim 'this function does X', 'this parameter means Y', or 'this path is dead or live', and whenever a user asks how existing code actually works or whether it does what its name says.
source: "recovered from git: chdr db40616, bbca3f9; cave-public 61e8f29, e4d6c25"
---

# read-the-system

## Statement

Treat a symbol name, parameter name, type, schema, or grep hit as a **lead, not a fact**. Before you assert, design against, or characterize how code you did not just write behaves at runtime, read the implementation that produces that behavior. In the codebases this is for, names have drifted from behavior — so any load-bearing behavioral claim MUST ship with a `file:line` anchor or be marked unverified.

## Why

The codebases this is for — legacy, inherited, AI-generated — are exactly the ones where names have drifted from behavior. A reviewer cannot see the gap, because the name reads correctly. Acting on the name ships the bug.

Worked cases, all real, all from one codebase's footgun register:

- A parameter named `healthMultiplier` actually scales **comfort**, not health — the caller passes `comfortMultiplier` into it.
- An ability named `assignment` does not control whether a unit is assignable; any unit is assignable regardless. The ability only configures slots.
- A field `trait.rules` is parsed and typed, but never executed — dead config that reads as live.

Each is invisible to grep, types, and review. Only reading the call path reveals it.

## When to apply

- **When you begin assessing a codebase**, on every subsystem you will characterize or change.
- Before any claim of the form "this function does X", "this parameter means Y", "this path is dead / live".
- When a `grep` or a type *suggests* an answer — that is the moment to read, not to conclude.

## Protocol

1. **Treat the lead as unverified.** A name / type / grep hit tells you *where to look*, not *what it does*.
2. **Read the path, not the signature.** Follow the actual call and data path that produces the behavior — caller to callee — not just the declaration.
3. **State the verified behavior with an anchor** (`file:line`). A claim without an anchor is still a lead.
4. **When the name contradicts the behavior, record it** as a footgun ([footgun-register](../footgun-register/SKILL.md)). The contradiction is the highest-value finding of the whole assessment.
5. **Spot-check, don't trust, existing docs.** A prior map or comment is itself a lead — verify load-bearing claims against the current code rather than inheriting them.

## Anti-patterns

1. **Infer-from-name.** "It is called `validate`, so it validates." The name is the hypothesis, not the result.
2. **Grep-as-proof.** A grep hit count answers "where", never "what" or "whether it runs".
3. **Type-as-behavior.** A type constrains shape, not semantics; a typed field can be dead.
4. **Schema-as-behavior.** A schema says what is well-formed, not what the code does with it.
5. **Trust-the-doc.** An inherited doc or comment can be stale; a stale map is worse than none, because it reads authoritative.

## Mechanical enforcement

This is a discipline, not a lint — there's no AST check for "did you actually read it." It's enforced socially, through the anchor rule in the Statement: a claim with a `file:line` is checkable, one without is just a lead. That is why every claim in the assessment is anchored.

## Related

- [footgun-register](../footgun-register/SKILL.md) — where name-vs-behavior contradictions are recorded.
- [silent-failure-census](../silent-failure-census/SKILL.md) — the sibling read: where errors vanish without a trace.
