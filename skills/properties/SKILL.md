---
name: properties
description: Pin behavior that ranges over structured input — parsers, validators, classifiers, rule engines, compilers, calculators — with a generated property over the input shape, not a handful of examples. Properties come from two sources: the data's schema (well-formed in → well-formed out, nothing dropped, references resolve) and the design (round-trip, conservation, idempotence, monotonicity, clamp, decision-totality). Use whenever you write or review tests for invariant-rich code — the example you didn't think to write is exactly where the bug hides.
---

# properties

## Statement

Where behavior ranges over many inputs, generate the inputs and assert an invariant that holds over their *shape*, instead of listing cases by hand. A property is the test that ranges over the whole input domain.

## Why

Example tests only cover the shapes you thought of. The bug lives in the shape you didn't — and no amount of hand-written cases reaches it reliably.

Worked case: a compiler step mirrored a `.value` path onto a `.max` path, anchored to the *end* of the string (`/\.value$/`). A plausible bug drops the anchor (`/\.value/`) and rewrites the *first* `.value` instead. Every example used a simple path like `heat.value`, where both behave identically — so no example could tell them apart. A generator that produces a mid-path `.value` (`a.value.b.value`) separates them on the first try. That is the property earning its keep: correctness ranged over the input *shape*, and the failing shape was one nobody would write down.

## When to apply

Highest on code with clean invariants — engines, calculators, parsers, validators, state machines, compilers. Low on glue and CRUD, where there's no relational invariant to state. If you can't name an invariant, a property isn't the tool; reach for examples and edges instead.

## Two sources of properties

- **Schema-derived (the data's shape).** Generate from the input schema and assert structural facts: a well-formed input produces a well-formed output, nothing is silently dropped, every reference resolves, ids stay stable.
- **Design-derived (relational).** Take the invariant from the design: *round-trip* (decode∘encode = identity), *conservation* (nothing created or lost), *idempotence* (applying twice = once), *monotonicity*, *clamping to a range*, *decision-totality* (every input lands in exactly one branch).

One tool runs both.

## Protocol

1. **Name the invariant first**, and take it from the design — not from reading the code (a property read off the implementation just restates it; see [keep-properties-honest](../keep-properties-honest/SKILL.md)).
2. **Generate the input over its real shape** — including the adversarial structure an example would skip (nesting, repetition, empties, ordering).
3. **Pin the seed.** An unseeded property that flakes in CI gets deleted, taking its coverage with it. Fixed seed, fixed run count.
4. **Assert the invariant**, not a restated computation.

## Anti-patterns

1. **Property-from-implementation.** Written by reading the code, so it passes even when the code is wrong — the tautology trap. Source it from the design.
2. **Example in a generator's clothing.** A "property" over a fixed three-element list is three examples with extra ceremony. If it doesn't range over the shape, it isn't a property.
3. **Unseeded flake.** Non-deterministic generation that fails intermittently erodes trust until someone deletes it. Seed it.
4. **Property where no invariant exists.** Forcing one onto glue code yields a vacuous assertion. No invariant → not the tool.

## Mechanical enforcement

No clean lint catches "is this a real property, or an example in disguise?" — that's a review judgment. Grade it instead with mutation testing ([mutation-grading](../mutation-grading/SKILL.md)): a property that kills no mutant is either too weak or aimed at dead code.

## Related

- [mutation-grading](../mutation-grading/SKILL.md) — grades whether a property actually bites.
- [keep-properties-honest](../keep-properties-honest/SKILL.md) — provenance, refutation, and stopping on counterexamples.
- [boundary-tests](../boundary-tests/SKILL.md) — the example-level companion for numeric limits.
