---
name: assert-by-shape
description: You are writing or reviewing a test that pokes at 3+ fields of one returned object, checking each field one by one ("the test checks many fields separately"). For a function that returns a structured value, a config loader, parser, mapper, builder, serializer, or classifier, the test MUST compare the whole produced value against one expected fixture (input to output) in a single deep-equality assertion, not a column of per-field assertions on the same object. This is about test SHAPE (readable, non-brittle), distinct from adequacy.
source: "recovered from git: PDD f4170cc, 0413b06"
---

# assert-by-shape

## Statement

When a function returns a structured value (object, array, record), assert the WHOLE value against one expected fixture in a single deep-equality check. Do NOT assert it field by field. The test should read as `input to exact output`: a spec, not a checklist of pokes.

This is about test SHAPE, not adequacy. boundary-tests, mutation-testing, and keep-properties-honest check whether a test catches a bug. This checks that the test is readable and non-brittle. A field-by-field test can be perfectly adequate (mutation-graded, boundary-covered) and still be the wrong shape.

## Why

Field-by-field assertions carry three costs:

- **They under-assert silently.** `assertEqual(cfg.version, 1)` says nothing about the twelve other fields. The bug hides in the field nobody thought to poke. A whole-value deep-equal pins every field, including the ones you would never have written a line for.
- **They read as noise, not a spec.** Ten `assertEqual(x.a, ...)` lines force the reader to reconstruct the expected object in their head. One fixture IS the expected object, on the page.
- **They rot.** When the shape changes, you hunt-and-peck across scattered assertions instead of editing one fixture.

Worked case: a config loader's migration test was a column of `assertEqual(cfg.version, 1); assertEqual(cfg.flows.length, 1); assertEqual(cfg.flows[0].id, "typescript"); assertEqual(cfg.flows[0].paths.source, "src"); ...` and so on down the object. It was mutation-graded and pinned concrete values, so it was adequate. It was also unreadable, brittle, and silent about every field nobody happened to poke. Rewritten as one `deepEqual(loadConfig(dir), {version: 1, flows: [...], ...})`, it became the spec for "v1 file in, this exact config out" and started pinning the whole shape.

## Patterns

**1. Whole-value deep-equal.** One assertion comparing the entire return value to a literal fixture. This is the default for anything that returns an object or array.

**2. Table-driven for mappings.** A pure function over many inputs is a `[input, expected][]` table compared in one shot, not N assertions:

```ts
assert.deepEqual(cases.map(([i]) => [i, fn(i)]), cases);
```

The row carries the input, so a failure points straight at the offending case.

**3. Pin a derived or bulky default literally ONCE.** A big default (a gate map, a config skeleton) spelled into every fixture is brittle: add one field and every fixture breaks. But deriving the expected value from the same code under test is tautological: it can no longer fail. Resolve both: pin the default literally in its own dedicated test, then reference the source helper everywhere else. The single literal test guards the default; the references stay concise and honest.

**4. Normalize away `undefined`-key noise.** When the type has many optional fields, a strict deep-equal forces `{key: undefined}` into every fixture. Strip them so the fixture reads as the meaningful shape:

```ts
const shape = (x: unknown) => JSON.parse(JSON.stringify(x)); // drops undefined-valued keys
assert.deepEqual(shape(result), { /* only the keys that carry meaning */ });
```

## When NOT to use whole-shape

Shape is the default, not dogma:

- **Error assertions.** `assert.throws(() => f(bad), /message/)` is already the right shape; there is no value object to compare.
- **A genuinely single-behavior test.** One behavior, one targeted assertion is fine. `assert.equal(detectRunner(root), "vitest")` pinning exactly one decision is not field-by-field, it is one fact. The anti-pattern is 3+ pokes reconstructing one object, not a single focused assert.
- **Serialization minutiae.** Do not assert exact key order or internal key sets. If the serialized form IS the contract, express that as one fixture comparison of the parsed output, not an `Object.keys().sort()` poke.

## Anti-pattern

```ts
// WRONG: field-by-field. Under-asserts, reads as noise, brittle.
const cfg = loadConfig(dir);
assert.equal(cfg.version, 1);
assert.equal(cfg.flows.length, 1);
assert.equal(cfg.flows[0].id, "typescript");
assert.equal(cfg.flows[0].language, "typescript");
assert.equal(cfg.flows[0].paths.source, "src");
// ... and nothing at all about the other fields
```

## Correct pattern

```ts
// RIGHT: one fixture. The spec, the whole shape, on the page.
assert.deepEqual(shape(loadConfig(dir)), {
  version: 1,
  flows: [{ id: "typescript", language: "typescript", paths: { source: "src" }, gates: { "boundary-tests": "warn" } /* , ... */ }],
  // legacy mirrors, etc.
});
```

*(Examples are TypeScript; the rule is language-agnostic: a deep-equal against a fixture, a comparison table for mappings.)*

## Mechanical enforcement

A test-quality lint can flag a test block with 3+ equality assertions whose left-hand sides share a receiver (`x.a`, `x.b`, `x.c`) and suggest a single deep-equal. Heuristic, so advisory: shape is hard to detect precisely, and the throws and single-behavior cases are legitimate. Warn, never block.

## Related

- [property-based-testing](../property-based-testing/SKILL.md): pin behavior over a generated input space. A property is this rule taken to "all inputs," not one fixture.
- [keep-properties-honest](../keep-properties-honest/SKILL.md): the tautology trap (expected derived from the code under test) that pattern 3 guards against.
- [boundary-tests](../boundary-tests/SKILL.md), [mutation-testing](../mutation-testing/SKILL.md): adequacy (does the test catch a bug), the axis orthogonal to shape.
