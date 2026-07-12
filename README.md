# engineering-discipline

Portable, stack-independent software-engineering discipline, packaged as Claude Code skills. Each skill is one rule a careful engineer applies by reflex — test shape, failure honesty, one concern per file, reading before claiming — written so an LLM (or a person) retrieves it at the moment it applies and can act on it.

These are judgment rules, retrieved by trigger, not a linter. Where a rule is also mechanically checkable, the skill says so and names the lint family that catches it; the skill covers the part a tool cannot see.

## Install

Local, for one session or project:

```
claude --plugin-dir /path/to/engineering-discipline
```

Via marketplace:

```
/plugin marketplace add /path/to/engineering-discipline
/plugin install engineering-discipline
```

Skills load on demand: when your prompt, or the work in progress, matches a skill's trigger, its guidance is pulled into context. Nothing is always-on.

## What's inside — 23 skills

### Test adequacy — does the test actually catch a bug?
- **assert-by-shape** — compare the whole returned value to one fixture, not field by field.
- **boundary-tests** — a case exactly at every limit, not only to either side of it.
- **no-op-paths** — a test where the trigger condition is not met and nothing changes.
- **mutation-testing** — inject small bugs; a suite that never reddens is not testing.
- **property-based-testing** — pin invariant-rich code over generated inputs, not a handful of examples.
- **keep-properties-honest** — source each property from the design, not the code it tests.

### Code structure — one thing, once, readable
- **cohesion-review** — read the whole grown module for a second responsibility, not just the diff.
- **decompose-by-attention** — size work to about a minute of planning plus a minute of review.
- **guard-clauses** — early exits over nested `if`; keep the happy path flat.
- **name-and-bundle** — never repeat a literal; name it once, bundle what changes together, derive the rest.

### Failure & change safety — don't ship a silent break
- **silent-failure-census** — sweep for errors that vanish without a trace; classify real vs benign.
- **characterize-before-change** — pin current behavior in tests before touching code you don't trust.
- **reproducibility-baseline** — build something a change can be diffed against to prove no drift.
- **fix-what-you-find** — close a defect you surface; don't preserve-and-note it.

### Reading unfamiliar code — the name is a lead, not a fact
- **read-the-system** — read the implementation before claiming how it behaves.
- **footgun-register** — record every name that lies about its behavior, anchored and dated.

### Spec & design hygiene — before code exists
- **design-completeness** — every behavior names its contract, its failure modes, and its edges.
- **one-meaning-per-term** — a key term in a spec carries exactly one meaning.
- **requirements-traceability** — every requirement maps to a test that fails if it is violated.
- **design-assumptions-register** — surface the beliefs a design rests on; give each a falsifier and a detector.

### Delivery & de-risk — commit deliberately
- **pr-sizing** — one operator milestone per PR.
- **decision-gate** — gate a costly, hard-to-reverse choice on an observable kill-condition.
- **derisk-gate** — prove the riskiest architectural assumption with a walking skeleton first.

## How the skills relate

Skills cross-reference one another — a surviving mutant in **mutation-testing** feeds **fix-what-you-find**; **read-the-system** produces the contradictions **footgun-register** records; **cohesion-review** is the code cousin of **one-meaning-per-term**. The links are relative, so they resolve wherever the plugin is installed.

## Provenance

These skills were extracted and generalized from a verification-first development methodology, then stripped of any project-specific vocabulary so they stand alone on any codebase and any stack. Code examples are illustrative (some TypeScript, some Python); every rule is language-agnostic.
