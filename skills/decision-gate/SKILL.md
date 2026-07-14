---
name: decision-gate
description: You are committing to a choice other work will be built on and that is costly or near-impossible to reverse: picking a technology, datastore, or library, fixing a module boundary, a requirement that fixes a solution, or a scope cut. Require an observable kill-condition (what would prove the choice wrong), a detector watching for it, and proof matched to blast radius and reversibility, ending in a GREEN / RED / OVERRIDE verdict. Triggers on a plain "a call we need to make". Not for beliefs you never consciously chose (design-assumptions-register), for merely recommending the best option, or for local, reversible choices with a cheap fallback: skip those explicitly.
source: "recovered from git: chdr 328e07d, ef5a64b; PDD 9746c82, 4aee2fe"
---

# decision-gate

A gate on **commitment**: before work is built on a load-bearing decision, require that it state what would prove it wrong, wire something to watch for that, and carry proof matched to the cost of being wrong. Operator-driven, with a mandatory sign-off on the high-stakes cell.

## When to apply

- **Primary:** any decision whose reversal would force rework *beyond the local change* — a technology or library choice, an architectural commitment (a module boundary, a concurrency model), a requirement that fixes a solution, a scope cut.
- **Skip — explicitly, never silently:** local, reversible choices with a cheap fallback. Record the decision and its fallback in one line. A recorded skip is fine; an *absent* record on a load-bearing decision is the gate failure.

## Why

A decision you can't show to be wrong is the green-but-wrong failure moved up a layer: the record reads identically whether the choice was right or wrong, so no reviewer can catch it. A coding agent makes this worse — its training rewards a confident, plausible choice, not a justified one. The fix is the one the test gates already use: don't trust the producer's claim, make the decision externally checkable. The value is temporal — proof is only worth something *before* the work assumes the decision.

## What a decision must carry

1. **A kill-condition** — an observable signal that, if it holds, means the decision was wrong and must be revisited. It has to be an *independent* observable (a metric, an event, a threshold), not a restatement of the choice.
   - Falsifiable: *"Postgres stays our store while write load holds under 2k/s at p95; revisit if it sustains above that for a week."*
   - Not: *"switch off Postgres if it stops being good enough"* — circular; restates the decision, traps nothing.
2. **A detector** — where the kill-condition is actually watched: a CI metric, a cost report, a scheduled review. A kill-condition no one watches is a wish.
3. **Proportionate proof** (below), produced before commitment.

If no falsifiable kill-condition can be stated, the decision is either not load-bearing (downgrade, skip the gate) or unfalsifiable (escalate — don't commit).

## Proportionate proof

Match proof to blast radius × reversibility. Both under-proving the costly cell and over-proving the cheap one are defects — naming both is the point.

| | Two-way door (cheap to undo) | One-way door (entrenches) |
|---|---|---|
| **Local** (rework stays in the unit) | named fallback + cited reason | alternatives weighed (real disqualifiers) + kill-condition |
| **Cross-cutting** (rework spans units) | alternatives weighed + kill-condition + fallback | **de-risk spike: a walking skeleton exercising the kill-condition's risk + operator sign-off** |

The operator sets where the thresholds sit — what counts as "cross-cutting", what counts as "one-way". That classification is theirs; it is the confidence dial. The top-right cell *is* the [derisk-gate](../derisk-gate/SKILL.md); this gate generalizes it to every load-bearing decision and adds the cheaper tiers.

## Verdict → action

| Verdict | Meaning | Action |
|---|---|---|
| **GREEN** | kill-condition stated, detector wired, proof matches the cell | commit; the kill-condition carries forward as a watched tripwire |
| **RED** | no falsifiable kill-condition, or proof below the cell | don't commit — downgrade, escalate, or produce the missing proof, then re-run |
| **OVERRIDE** | operator accepts an under-proven decision | proceed; recorded with a reason, tracked as residual, operator-owned |

## Outputs

A committed decision record (e.g. `decisions/<date>-<slug>.md`): the claim, its kill-condition + detector, the blast/reversibility cell, the proportionate proof (evidence / fallback / skeleton reference), and the verdict + sign-off. Surface the decision and what would reverse it — not a narrative of how you arrived at it.

## Anti-patterns

1. **Unfalsifiable decision.** "We chose X, it's more scalable." No kill-condition is statable → it reads the same whether right or wrong.
2. **Wish, not detector.** A kill-condition is stated but nothing watches for it, so it never trips.
3. **Uniform ceremony.** Full options-table rigor on a trivially reversible choice — it buries the one one-way door under twenty harmless ones and trains the operator to rubber-stamp. Cheap decisions get cheap proof.
4. **Reverse-sourced kill-condition.** Writing the trip to match the choice already made — the decision-layer form of sourcing a property from the implementation instead of the design.
5. **Solution-as-requirement.** A "requirement" that is really an ungated decision ("shall use SQLite"). Gate it; don't let it ride unproven inside the spec.
6. **Retroactive proof.** Naming the kill-condition or running the spike after the work already assumes the decision. The proof is already spent.

## Related

- [derisk-gate](../derisk-gate/SKILL.md) — the high-stakes (cross-cutting × one-way) cell of this gate, in full.
- [decompose-by-attention](../decompose-by-attention/SKILL.md), [pr-sizing](../pr-sizing/SKILL.md) — sizing and decomposition are themselves load-bearing decisions; gate the ones whose reversal spans units.
