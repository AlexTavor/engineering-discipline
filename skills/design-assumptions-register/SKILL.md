---
name: design-assumptions-register
description: Before building on a design or plan, surface the load-bearing assumptions it rests on — the beliefs about environment, dependencies, behavior, timing, and scale that were never consciously chosen — and record each in a committed register with a falsifying condition ("breaks if X"), a consequence-anchored fragility, and a detector that watches for the break. Use when committing a design, plan, or architecture; when a spec quietly assumes things about its world; or when a team keeps getting surprised by an assumption that turned out false. The high-fragility entries route to derisk-gate or decision-gate; the rest carry a recorded fallback. Not for choices you are explicitly deciding (decision-gate), proving a single high-fragility assumption end-to-end with a walking skeleton (derisk-gate), or name-vs-behavior lies in existing code (footgun-register). This is the wide inventory that feeds derisk-gate, not the spike itself.
source: "recovered from git: chdr d88f751, 4c5357e; PDD 8a75b12, 3dbbf74, fb59f9a"
---

# design-assumptions-register

A planning-time register: before work is built on a design, surface the load-bearing assumptions it rests on, give each one a falsifying condition and a detector, and size the response to how badly it hurts if it breaks. It is the wide net that feeds the [derisk-gate](../derisk-gate/SKILL.md) and the [decision-gate](../decision-gate/SKILL.md).

## When to apply

- **Primary:** once, before committing a design or plan (and before decomposition), on any work whose correctness depends on beliefs about its world that were never examined.
- **Recursive:** when a unit turns out to rest on its own assumptions — a new dependency's behavior, a timing or scale belief — register them before building on it.
- **Skip — explicitly, never silently:** work whose assumptions are already proven or trivially reversible. Record "no load-bearing assumptions" in the register. A recorded skip is fine; an absent register on assumption-heavy work is the failure.

## Why

An assumption is the [decision-gate](../decision-gate/SKILL.md)'s blind spot widened. A decision is a choice you know you made and can gate; an assumption is a belief you did not know you were holding, so nothing gates it. Either way the artifact reads the same whether the belief holds or not — the green-but-wrong failure, moved up from the test to the premise. The fix is the one the gates already use: make it externally checkable. State what would prove the assumption wrong, wire something to watch for that, and write down what it costs if it breaks, before anything is built on it.

This is judgment, not a tool — no checker can list the things you assumed without noticing. The contribution here is not to score assumptions with a model (the stochastic-panel path this rejects) but to force each surfaced assumption into a falsifiable, detectable, consequence-sized **structure**, and to check that structure mechanically.

## Entry format

Each entry captures one load-bearing assumption:

- **The assumption** — the belief, stated plainly ("the upstream API returns results in request order").
- **Category** — one of the five below; the set is a coverage checklist.
- **Breaks if** — the falsifying condition, an independent observable ("a response ever arrives out of order"), not a restatement of the belief.
- **Fragility** — the consequence if it breaks, anchored to consequence and not to your confidence (below).
- **Detector** — where the "breaks if" is actually watched: a test, an assertion, a metric, a scheduled check. A falsifier no one watches is a wish.
- **Response** — a recorded fallback (low fragility), or a reference to the de-risk spike / decision record that retires it (high fragility).

## The five categories (a coverage checklist)

Sweep all five; an empty category is either genuinely not-applicable (say so) or a blind spot.

- **Environmental** — the runtime, platform, filesystem, config, or deployment the code assumes.
- **Dependency** — what an external library, service, or API does, beyond what its declaration promises.
- **Behavioral** — how a human or another agent will act, or how callers will use the thing.
- **Temporal** — ordering, timing, freshness, clock, expiry, and "still true later" beliefs.
- **Scale** — volume, concurrency, size, and load the design silently assumes.

## Fragility, anchored to consequence

Score fragility by what happens if the assumption breaks, not by how confident you are that it won't:

- **High** — silently wrong output or total failure; no one notices until the damage is done.
- **Medium** — degraded or unreliable output; the system still runs.
- **Low** — cosmetic or easily caught; a named fallback covers it.

If every assumption lands in the same band, the scoring is uncalibrated — the most and least dangerous beliefs are not equally dangerous. Spread them.

## Routing by fragility

Match the response to the fragility — the same proportionate-proof logic as [decision-gate](../decision-gate/SKILL.md):

| Fragility | Response |
|---|---|
| **Low** | record a named fallback and the "breaks if"; move on |
| **Medium** | wire a detector now; accept with the fallback, tracked as residual |
| **High** | route to [derisk-gate](../derisk-gate/SKILL.md) (spike the belief end to end) or, if it is really an ungated choice, [decision-gate](../decision-gate/SKILL.md). Do not build on it until it is retired or operator-overridden |

An assumption with no statable "breaks if" is unfalsifiable: it is either not load-bearing (downgrade it) or genuinely unknowable (escalate; do not quietly build on it).

## Anti-patterns

1. **Assumption without a falsifier.** "We assume the queue is ordered" with no "breaks if" is an observation, not a guard — nothing can ever catch it being wrong.
2. **Falsifier no one watches.** A "breaks if" with no detector never trips; the assumption fails silently anyway.
3. **Confidence-anchored fragility.** Scoring by how sure you are instead of by the damage if wrong. The dangerous assumption is the one you are most confident about.
4. **Range compression.** Everything scored medium — the register looks complete and hides the one belief that will sink the design.
5. **Register-as-decision-log.** Recording choices you made; those are [decision-gate](../decision-gate/SKILL.md). This register is for beliefs you did not know you were making.

## Mechanical enforcement

The surfacing is judgment; the structure is checkable. A check over the committed register can verify that every entry has all six fields, the category is one of the five, every High and Medium entry names a detector (or a spike / decision reference), and no category is silently empty. Advisory while the register is being adopted; blocking once it is the gate that precedes decomposition.

## Related

- [decision-gate](../decision-gate/SKILL.md) — choices you make and can gate; this register is the beliefs you did not. High-fragility entries route here.
- [derisk-gate](../derisk-gate/SKILL.md) — proves a high-fragility assumption with a walking skeleton; this register is the wider net that feeds it.
- [footgun-register](../footgun-register/SKILL.md) — the same committed-register discipline, pointed at name-vs-behavior lies in existing code rather than forward design beliefs.
