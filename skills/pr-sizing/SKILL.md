---
name: pr-sizing
description: Decide whether to bundle multiple changes into one PR or ship them standalone. PR size targets the operator's attention (one milestone per PR), not the agent's construction unit (one logical change per PR). Use when composing PRs for structurally similar work — multiple units, multiple amendments, or many files with the same transformation.
source: "recovered from git: chdr 8f0a17f, 2c418bd"
---

# pr-sizing

## When to apply

Any time you are composing PRs that ship more than one structurally similar unit of work — a change that produces several units, an amendment touching several files, a refactor repeating one pattern.

## The attention-unit principle

PR size targets the **operator's attention unit**, not the **agent's construction unit**.

- The agent's construction unit is "one logical change" — easy to construct atomically, easy to explain in isolation, satisfying to ship.
- The operator's attention unit is "one milestone the operator might genuinely halt at" — review fatigue is real, mechanical `lgtm` cycles signal over-fragmentation, and cumulative review cost grows with PR count.

When the two are treated as equivalent, the agent optimizes locally and the operator pays globally.

The same principle one level up — sizing the work itself — lives in [decompose-by-attention](../decompose-by-attention/SKILL.md). This skill applies it at PR scope.

## Bundle when (all three hold)

1. **Consecutive changes share shape.** The diffs look alike; a reviewer groks the pattern once and skims repetitions.
2. **Individual review value is low.** No single change is a structural decision; each is a mechanical instance of the pattern.
3. **Operator unlikely to veto any one in isolation.** If the response would be `lgtm` to each in turn without engagement, bundling captures the same outcome in one cycle.

## Standalone when (any one holds)

1. **Real milestone.** Something downstream depends on this landing first — a new gate going live, a breaking change.
2. **Divergent review focus.** Needs a different reviewer mindset than its neighbours (security vs docs).
3. **Decision affecting downstream plan structure.** Adding/removing units, changing the plan's shape. Plan-shape decisions are the operator's call and merit their own PR.

## Catch-it-sooner heuristic

**Two consecutive `lgtm`-with-no-engagement cycles signal the unit is wrong.** A smooth `lgtm`-stream is NOT a success signal — it means the agent isn't earning each review cycle. Treat mechanical approval as evidence the unit is wrong; re-evaluate bundling for the next 3–5 atoms.

## Concrete bound

Default budgets per milestone: **≤ 4 implementation PRs**, **≤ 8 docs-only PRs**. If you need more, the scope is probably mis-sized — apply [decompose-by-attention](../decompose-by-attention/SKILL.md) before continuing. Defaults, not hard caps: high decision-density work may need more; mechanical work fewer.

## Anti-pattern catalogue

1. **One logical change = one PR (mechanical).** Three tiny amendments to the same scope, each trivial, none worth standalone review — 3× the cumulative review cost. Bundle into one "amendments" PR.
2. **Bundling across plan boundaries.** Bundling a plan-shape decision (adding a unit) with the implementation that follows it. The plan change deserves standalone review; split them.
3. **Reading smoothness as success.** Three mechanical `lgtm`s in a row is the catch-it-sooner heuristic firing — re-evaluate bundling, don't read it as the process working.

## Related

- [decompose-by-attention](../decompose-by-attention/SKILL.md) — the same principle at the scoping level. The two compose: decompose-by-attention chooses what units exist; pr-sizing chooses how they ship.
