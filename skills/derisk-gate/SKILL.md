---
name: derisk-gate
description: Before committing a plan, prove the riskiest architectural assumptions with a thin end-to-end walking skeleton, then emit a ranked risk register and a GREEN / RED / OVERRIDE verdict. Use before decomposing work into units — on a new package boundary, an unproven integration, a cross-cutting concern, or a load/latency assumption. Skip explicitly (never silently) for incremental work over a proven architecture.
---

# derisk-gate

A planning-time gate: before the work is decomposed into units, prove the architecture's riskiest assumptions with a runnable walking skeleton — *before* anything is built against them. Operator-driven, with a mandatory sign-off.

## When to apply

- **Primary:** once, before the first decomposition, on any work whose architecture carries non-trivial risk.
- **Recursive:** when decomposition reaches an architecturally-significant unit — a new package boundary, an unproven dependency, a cross-cutting concern, a concurrency/state model, or a load/latency assumption — re-run the gate on that unit before carving it further.
- **Skip — explicitly, never silently:** incremental work over a proven architecture. Record "no architectural risk" in the register. A recorded skip is fine; an *absent* register is a gate failure.

## Why

Decomposition is the expensive commitment: once work is a unit tree and you start building against it, an architectural assumption that proves wrong forces re-architecting across already-built units, not a local fix. The gate's value is **temporal** — it only retires a risk if it runs *before* the construction that assumes it. Retroactive de-risking is not deferral, it is skipping.

## Protocol

1. **Enumerate architectural risks** — every assumption whose failure would force *re-architecting*, not just re-coding. Sweep:
   - **Integration** — an external system/library behaves as assumed.
   - **Structural** — the dependency graph holds, no hidden cycle.
   - **Performance** — latency/throughput/memory hold under real load, not a toy input.
   - **Concurrency/state** — the chosen model is sound.
2. **Rank** by `P(assumption is wrong) × cost-to-fix-if-found-late`. Keep it short — a register of low-impact entries buries the one that matters.
3. **Find the riskiest seam** — the thinnest end-to-end path that exercises the top risks *simultaneously*. Not a feature; the seam you are least sure of, wired end to end with everything off the risk path stubbed.
4. **Build the skeleton — directly, with a capable model.** It MUST run and exercise the risky seam with the real thing (real external call, real concurrency, real data shape). Mocking the risk away proves nothing.
5. **Read the result against each top risk** — **retired** (proven), **residual** (un-retired but accepted with a named mitigation), or **invalidated** (assumption was wrong). An invalidated top risk means the *architecture* is wrong → revise the law, do not proceed.
6. **Verdict + sign-off** (below). The operator may override an un-retired risk, recorded with a reason.

## Verdict → action

| Verdict | Meaning | Action |
|---|---|---|
| **GREEN** | every top risk retired or accepted-with-mitigation | proceed to decompose; residual risks + mitigations carry forward as architecture-decision updates or plan notes |
| **RED** | a top risk invalidated the architecture | revise the architectural law; do **not** decompose; re-run the gate afterward |
| **OVERRIDE** | operator accepts an un-retired top risk | record the reason in the register header; proceed; the risk is tracked as residual, owned by the operator |

## Outputs

- **Risk Register** — a committed markdown artifact (e.g. `docs/derisk/<scope>.md`): the ranked risks, each with status, the skeleton evidence, and residual mitigations. Surface *decisions* (which risks accepted, which mitigations), not a narrative of what was built ("report decisions, not actions").
- **Walking skeleton** — committed spike code, referenced from the register. It is *evidence, not product*: don't build on it unless explicitly promoted.
- **Verdict** — GREEN / RED / OVERRIDE + sign-off, in the register header.

## Anti-patterns

1. **Skeleton-as-feature.** Building the easy, visible feature instead of the riskiest seam. The skeleton must hurt — it targets what you are least sure of.
2. **Mocking the risk away.** Stubbing the exact thing under test (the external call, the real concurrency). If the risk path is mocked, the gate proves nothing.
3. **Retroactive de-risking.** Running the gate after the work is already built against the assumption — the risk is already spent.
4. **Risk-theater.** A long register of low-impact risks that looks thorough and buries the one re-architecting risk. Rank by re-architecting cost; keep it short.
5. **Green-by-omission.** Declaring GREEN because the skeleton passed when it didn't actually exercise the risk. The skeleton needs the same adequacy scrutiny as a contract test: did it exercise the risky *dimension*, or only a happy shape?

## Related

- [decompose-by-attention](../decompose-by-attention/SKILL.md) — de-risk first, then decompose.
