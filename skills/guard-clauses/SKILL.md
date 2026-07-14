---
name: guard-clauses
description: Writing or reviewing a function nested past two levels, a loop body wrapped in one big `if`, or a chain of force-unwraps standing in for missing checks; you think "flatten this nesting." Prefer a guard clause: an early exit on the negative case (`if (!ok) return`, `continue`, `throw`), so the happy path stays at base indentation and each precondition reads as a flat checklist at the top. A non-null assertion or force-unwrap (`x!`, `x!!`) covering for an absent check is a guard in disguise: narrow it, do not silence it. About one function's control-flow shape, not module cohesion (cohesion-review) and not behavior.
source: "recovered from git: PDD b2ab939"
---

# guard-clauses

## Statement

When a conditional's only purpose is to skip, reject, or bail, write it as an early exit — `if (!precondition) return` / `continue` / `throw` — not as `if (precondition) { ...the real work... }`. The happy path belongs at the base indentation; the preconditions belong above it as a flat sequence of guards. A non-null assertion or force-unwrap (`x!`, `x as T`, `x!!`) used in place of a check is a missing guard wearing a costume: replace it with a real early-out that narrows the value, never silence the check.

## Why

Nesting buries the main line under its exceptions. Every `if (cond) {` pushes the real work one level deeper and asks the reader to hold an open brace and an unstated "else" in their head until the bottom of the function. Guards remove that load: read the top, see every way the function can bail, then read the body knowing all preconditions already hold. Deep nesting is also where a forgotten `else` quietly changes behavior, and where a force-unwrap hides the case the author never handled.

Worked case: `if (user) { if (user.active) { if (order) { …30 lines… } } }` reaches the real work at four levels of indentation and three conditions the reader must keep live. Inverted — `if (!user) return; if (!user.active) return; if (!order) return;` then thirty lines flat at the base — the preconditions are a checklist and the body has nothing held over it.

## When to apply

- A function past ~2 levels of nesting whose inner block is the real work.
- A loop body wrapped in one big `if` — invert to `if (!x) continue`.
- A trailing `else` that exists only because the `if` branch didn't exit.
- A `!` / `as` / `!!` / force-unwrap standing in for a guard that was never written.

## Patterns

1. **Invert and exit.** Turn `if (ok) { work }` into `if (!ok) return; work`.
2. **Hoist the guards.** Collect the preconditions at the top as consecutive early-outs, so the body runs with every invariant established.
3. **`continue` over nest in loops.** Skip the iteration up front instead of indenting its body.
4. **Narrow, don't assert.** Replace `value!` with `if (value == null) return;` — the guard both documents and enforces what the assertion only claimed.

## Anti-patterns

1. **The arrow.** Ever-deeper nesting that marches the real work to the right; the shape itself is the smell.
2. **Else-after-exit.** `if (!ok) return; else { … }` — the `else` is dead weight once the `if` exits.
3. **Assertion-as-guard.** `x!` where a check belongs; it silences the compiler instead of handling the case.
4. **Guard with hidden work.** A guard that mutates state or logs on the way out. A guard rejects; it should not do the function's job on the side.

## When NOT to use

A genuine two-branch decision where both arms do real work is an honest `if/else`, not a guard to invert. Forcing an early-out onto a symmetric branch (both sides compute and return a value) just hides one real path. A single level of nesting is fine; this rule triggers on depth and on skip/reject branches, not on every conditional.

## Mechanical enforcement

Partly lintable. Max-depth and cyclomatic-complexity rules fire on deep nesting; `no-else-return` catches the redundant else; `no-non-null-assertion` and no-force-unwrap rules catch the assertion-as-guard smell. The tools flag the shape; the inversion itself is a human edit, because whether a branch is a guard or a real arm is a judgment.

## Related

- [cohesion-review](../cohesion-review/SKILL.md) — the whole-module readability read; deep nesting in a grown function is one of its cues.
- [decompose-by-attention](../decompose-by-attention/SKILL.md) — a function too nested to hold in one read is often also doing too much.
