---
name: design-completeness
description: Before code is written, a design MUST name three things for every behavior it specifies, the three a complete design of its type always has. Its contract (inputs, outputs, invariants), its failure modes (what can go wrong and what happens then), and its edges (boundary, empty, zero, and maximum cases). A design that states only the happy path is not finished, and a section that is present but empty (TBD, TODO, to be detailed) is a gap wearing the costume of completeness. Use when writing or reviewing a design doc, PRD, RFC, or technical plan before implementation, when a design feels thin but you cannot say why, or before committing a plan, to get its contract, failure modes, and edges concrete enough that requirements can later be traced to tests (this rule produces what requirements-traceability consumes). Reach for this even when the design looks complete, because the missing failure mode is invisible precisely because no one wrote it down.
source: "recovered from git: chdr ef5a64b, 468f636"
---

# design-completeness

## Statement

A complete design names, for every behavior it specifies: (1) its **contract** — the inputs it accepts, the outputs it produces, the invariants it preserves; (2) its **failure modes** — what can go wrong, and what the system does when it does; (3) its **edges** — the boundary, empty, zero, and maximum cases. A design that states only what happens when everything goes right is not finished. It has deferred the hard half to implementation, where it will be decided by accident.

## Why

Implementation is cheap; the expensive errors come from the design that never said what should happen when the input is empty, the dependency is down, or the limit is hit. Those gaps are invisible in review because absence has no anchor — you cannot see the failure mode that isn't written. This rule makes absence visible by naming what a complete design of its type must contain, so a missing failure-modes section becomes a finding instead of a production surprise.

It is the precondition for the verification rules. [requirements-traceability](../requirements-traceability/SKILL.md) can only trace requirements that exist; "cover the negatives and edges the spec names" can only cover failure modes the design named. Design-completeness is what gives those rules something to bite on.

## The completeness check

For each behavior in the design, confirm three blocks are present and concrete:

- **Contract** — inputs (types, ranges, required vs optional), outputs, and the invariants that hold before and after.
- **Failure modes** — each way it can fail (bad input, dependency down, contention, timeout) paired with the defined response (reject, retry, degrade, escalate). An unlisted failure mode is a decision handed to chance.
- **Edges** — empty, zero, one, maximum, boundary, and concurrent cases relevant to this behavior.

A behavior missing any block is incomplete. A block present but empty (TBD / TODO / placeholder) counts as missing — it is worse than an honest omission, because it reads as done.

## Anti-patterns

1. **Happy-path-only design.** Every success case specified, not one failure response. The design looks thorough and says nothing about the cases that cause incidents.
2. **Vestigial sections.** An "Error handling" heading with "TODO" beneath it. The structure claims a completeness the content doesn't have. Treat present-but-empty as absent.
3. **Contracts without invariants.** Listing inputs and outputs but never what must stay true (the balance never goes negative, the list stays sorted). The invariants are the part that tests and properties lock; omitting them leaves nothing to verify.

## Mechanical enforcement

Partly checkable: a design of a known type can carry a required-sections template (contract / failure-modes / edges per behavior), and a check can flag any behavior missing a block and grep for placeholder tokens (TBD, TODO, ???, "to be detailed") inside sections marked complete. The judgment — is this failure list actually exhaustive — stays human; the presence and non-vestigiality of the blocks is mechanical.

## Related

- [requirements-traceability](../requirements-traceability/SKILL.md) — traces the requirements this rule makes sure exist; design-completeness gives it something to trace.
- [design-assumptions-register](../design-assumptions-register/SKILL.md) — completeness names what the design *says*; the register names what it silently *assumes*.
