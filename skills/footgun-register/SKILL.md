---
name: footgun-register
description: When reading reveals that a name, type, or signature contradicts the real runtime behavior, record it as a footgun — the misleading appearance, the verified reality, a file:line anchor, and a last-verified date — in a committed register. Use while mapping legacy or AI-generated code, whenever a symbol turns out not to do what it says.
---

# footgun-register

## Statement

Every place where a name / type / signature **contradicts verified behavior** MUST be captured as a footgun entry: the misleading appearance, the verified reality, a `file:line` anchor, and a *last-verified* date. The register is a committed artifact, not a scratch note.

## Why

A name-lie you recover by reading (see [read-the-system](../read-the-system/SKILL.md)) is expensive knowledge. Left unrecorded, it is re-discovered by the next person — or silently re-broken by the next change, because the misleading name invites the wrong edit. The register turns one-time recovery into a standing guardrail.

A footgun is also an **invariant in disguise**: "X looks like it does A but really does B" is a constraint a downstream characterization test or property can lock.

## Entry format

Each entry captures one verified trap:

- **The appearance** — what the name / type / signature implies (`healthMultiplier` → "scales health").
- **The reality** — what it actually does, verified by reading (`scales comfort; the caller passes comfortMultiplier into it`).
- **Anchor(s)** — `file:line` for the claim and its key call site.
- **Last verified** — a date; the entry is only as trustworthy as its freshness.

## Protocol

1. **Source from reading, never from names.** An entry is created only after the contradiction is verified on the actual path (read-the-system).
2. **Anchor every claim.** No anchor → it is a rumor, not a footgun.
3. **Keep it to contradictions.** The register is for name-vs-behavior traps, not general documentation. A correct, well-named thing is not a footgun.
4. **Maintain it.** When an entry proves wrong or the code changes, fix it. A stale footgun is worse than none — it reads authoritative while lying.
5. **Date the sweep,** so readers can judge the decay.

## Anti-patterns

1. **Register-as-changelog.** Listing every quirk or TODO. Only verified name-vs-behavior contradictions belong.
2. **Anchorless entries.** "Assignment is confusing" is useless. Cite the `file:line` and the verified behavior.
3. **Write-once.** A register never re-verified rots into misinformation; un-maintained, it fails its own purpose.

## Mechanical enforcement

Partly checkable: a doc-freshness gate can verify the anchors still resolve and the verified-date is not stale (one codebase does this with a `code-map:check` over its anchored sections). The *content* — is this really a contradiction? — is judgment, sourced from read-the-system.

## Related

- [read-the-system](../read-the-system/SKILL.md) — produces the contradictions this register holds.
- [silent-failure-census](../silent-failure-census/SKILL.md) — the sibling sweep: where errors vanish without a trace.
