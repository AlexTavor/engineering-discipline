---
name: decompose-by-attention
description: Break a unit of work into pieces small enough to plan in about a minute and review in about a minute, so each piece fits a single pass of attention. Fires whenever you scope a task, turn a goal into a plan, or turn a plan into changes, and recursively whenever a scope feels too big to hold in one pass, spans more than about three distinct concerns, or mixes high-level design with low-level detail. Also when a user says 'break this down', 'this ticket is too big', 'split this work', or 'chunk the plan'. This sizes the work itself, not bundling finished changes into PRs (pr-sizing) or reviewing a grown module (cohesion-review).
source: "recovered from git: chdr 8f0a17f, 8500a04"
---

# decompose-by-attention

## When to apply

Any time you are scoping work — turning a goal into a plan, a plan into changes, or checking a single change before drafting it. The skill is recursive: apply it at every level until each unit is atomic.

## The attention-size principle

A work unit is correctly sized when both hold:

- **Planning takes ~1 minute of operator attention.** Long enough to encode intent; short enough to hold the whole scope in working memory.
- **Completion review takes ~1 minute.** Long enough to verify the artifact matches intent; short enough that no part of the review goes perfunctory.

"1 minute" is approximate — it anchors the discipline. What matters is that the scope fits a single attention episode, not that a stopwatch ratifies it. If you lose context mid-plan or mid-review, the scope is too big.

Why attention rather than lines of code, complexity, or hours: implementation capacity is cheap and expert attention is the bottleneck. Attention is the actual currency of review.

## Too-big heuristics

A scope is too big if any one is true:

1. **Distinct-concern count > 3.** Touching more than three distinct concerns (e.g. "schema for X, validator for X, migration for X, doc for X" = four) is a candidate to carve. The rule isn't "always carve at 4"; it's "at 4+, check whether they're truly cohesive or coincidentally bundled."
2. **Judgment-call density > 2 per minute of planning.** More than two non-trivial design decisions per planning minute is denser than the attention budget allows. Each decision deserves its own sub-unit where it's the centerpiece.
3. **Concern span across abstraction levels.** Mixing high-level architecture with low-level detail (design the schema AND choose the library AND write the migration) needs separation — one level per attention episode.

## Atomic-enough heuristics

A scope is correctly atomic when both hold:

1. **Artificial-seam test.** Carving further forces inventing seams that don't match natural concern boundaries (e.g. splitting "fields" from "invariants" when they're inseparable). Carving would create ceremony, not value.
2. **Natural cohesion.** One centerpiece — one schema, one skill, one script, one decision — even if it ships supporting artifacts (tests, examples, fixtures). Multiple centerpieces is a bundling smell.

When both hold, stop carving.

## Recursive carve protocol

1. **Top level** (goal → plan): too big → sub-units; atomic-enough → one unit.
2. **Mid level** (plan → changes): multiple distinct logic units → multiple changes; already atomic → one.
3. **Unit level**: a stopping check before drafting. A unit that fails the atomic-enough heuristics needs further carving first.

Terminates when every unit passes both atomic-enough heuristics. No fixed depth limit; deep nesting is allowed if the work has nested cohesion.

## Anti-pattern catalogue

1. **Count-targeting (Goodhart).** "The last plan had 7 units, so this one should too." The number is a by-product of the carve, not its goal; targeting it distorts the carve.
2. **Decomposing for ceremony.** Splitting trivially-small work (rename foo→bar / update bar's usages / update bar's tests) into separate units because the workflow expects several. Ceremony for no attention payoff.
3. **Bundling unrelated work.** Packing multiple unrelated concerns (schema validator AND CI pipeline AND deploy docs) into one unit to cut count. More concerns than one attention episode holds — exactly what carving prevents.
4. **Carving on lines-of-code.** "This file is big; split it." Lines are an output proxy; attention is the currency. A large file with one cohesive concern is fine; a small file spanning three concerns is not.
5. **Carving on file boundaries.** Treating "one file per unit" as the rule. If a single concern legitimately spans two files (a schema and its companion example), keep them together.

## Related

- [pr-sizing](../pr-sizing/SKILL.md) — the same principle at PR scope.
