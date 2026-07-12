---
name: name-and-bundle
description: Never repeat a literal that carries meaning. The first time a string or number means something, name it; the second time you would type the same literal, reference the name. Bundle constants that must change together into one structure, and derive any dependent value from its source instead of restating it. Use when writing or reviewing code with a magic number or string appearing more than once, parallel literals that must stay in sync (a limit and its message, a key and its default), or a value computed by hand that the code could compute. About one source of truth for every data value — the DRY cousin of cohesion-review.
source: "recovered from git: chdr 6efc97a, 328e07d; PDD cf96cac, 0413b06"
---

# name-and-bundle

## Statement

A literal that carries meaning gets a name. A literal that appears twice gets one name, referenced twice. Constants that must move together are bundled into one structure that is the single place they are defined. A value that depends on another is derived from it, not restated by hand. One source of truth for every data value — the discipline [cohesion-review](../cohesion-review/SKILL.md) applies to behavior, applied to data.

## Why

A repeated literal is a latent mismatch. The second occurrence is invisible to whoever changes the first, so the two drift, and the resulting bug is an inconsistency no single diff reveals. A hand-computed dependent value is the same trap pre-armed: a buffer sized `1024` beside a comment "1KB", a total that restates the sum of its parts, a mask spelled out next to the width it should derive from — change the source and the copy silently lies. Naming makes the meaning explicit and the change atomic. Bundling makes the coupling visible. Deriving makes the dependency the compiler's job, not the next reader's memory.

Worked case: a retry limit `3` lives in the loop condition, in the log line "retrying up to 3 times", and in a test expecting three attempts. Someone raises it to `5`, fixes the loop, and leaves the message and the test asserting the old number. Named once as `MAX_RETRIES` and referenced in all three, the change is one edit and nothing can drift.

## When to apply

- The same meaningful literal appears twice or more — name it once, reference it.
- Two constants must stay in sync (a limit and its error text, a key and its default, a width and its mask) — bundle them into one record, enum, or config object.
- A value is computed by hand that the code could compute — derive it from its source.
- A default is spelled into several call sites — define it once, reference it everywhere.

## Patterns

1. **Name on first meaning.** Give the value a name where it first means something, not at second use.
2. **Bundle what changes together.** Related constants become one structure — the one place they are defined and the one place they change.
3. **Derive, don't restate.** Compute the dependent value from its source so it cannot fall out of sync.
4. **Pin bulky defaults once.** A large default belongs in exactly one place, referenced elsewhere — the same single-source rule [assert-by-shape](../assert-by-shape/SKILL.md) uses for fixtures.

## Anti-patterns

1. **Magic-literal-twice.** The same `3` or `"admin"` typed in two places; a change to one leaves the other stale.
2. **Parallel literals out of sync.** A limit and the message that quotes it, defined apart; they drift on the first edit.
3. **Hand-computed dependent.** Restating a sum, a length, or a bitmask the code could derive.
4. **Over-naming.** Naming a one-use, self-evident literal (`nextIndex = i + 1`) adds indirection without removing any drift. Name for meaning and reuse, not for ceremony.

## When NOT to use

A literal used exactly once whose meaning is obvious in place — `arr[0]`, `* 2`, an HTTP `200` at the single point it is returned — does not need a name; the indirection buys nothing because there is no second copy to drift. The rule triggers on repetition or on non-obvious meaning, not on the mere presence of a literal.

## Mechanical enforcement

Partly lintable. `no-magic-numbers` flags repeated numerics; duplicate-string rules flag repeated string literals. The tools catch the repetition; whether two equal literals are the same concept (share a name) or a coincidence (must not) is a human call — `200` the status code and `200` the pixel width are not the same constant.

## Related

- [cohesion-review](../cohesion-review/SKILL.md) — one source of truth for behavior; this is its data cousin.
- [assert-by-shape](../assert-by-shape/SKILL.md) — pin a bulky default once and reference it, rather than re-spelling it in every fixture.
- [one-meaning-per-term](../one-meaning-per-term/SKILL.md) — one name per concept in a spec; this is one name per value in code.
