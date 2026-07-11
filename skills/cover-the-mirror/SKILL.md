---
name: cover-the-mirror
description: Every operation with a natural inverse implies that inverse exists. Create implies delete, open implies close, encode implies decode, acquire implies release, subscribe implies unsubscribe, authenticate implies authorize. When a design or codebase has one half of a mirror pair, the other half MUST exist or be explicitly marked absent-by-design, because a missing inverse is a silent gap — the resource you can create but never clean up, the token you issue but never revoke, the cache you fill but never invalidate. Use when reviewing a design, an API surface, a set of operations, or a resource lifecycle for operation/inverse symmetry (not whole-design completeness — that is design-completeness), and whenever you notice a create_ or open_ or add_ or start_ without its partner. Reach for this even when nobody mentioned symmetry, because the missing half is exactly what no one thought to bring up.
---

# cover-the-mirror

## Statement

Many operations come in pairs: each has a natural inverse or counterpart. When one half is present, the other must be present too, or explicitly declared absent-by-design with a reason. A present operation whose inverse is silently missing is a gap the structure itself points to, and it is usually the dangerous direction: you can create but not clean up, issue but not revoke, lock but not release.

## Why

This catches a class of incompleteness that requirement-by-requirement review misses, because the missing half was never written down to be reviewed. The structure implies it: five `add_*` methods and no `remove_*` is a louder signal than any single requirement could be. It is the design-time cousin of the resource leak and the lifecycle bug; most "we can create X but there's no way to delete it" production problems are a mirror that was never covered. Finding it costs a glance at the operation set. Finding it in production costs an incident.

## Common mirror pairs

Sweep the design for these and their domain-specific kin:

- create / delete, add / remove, insert / evict
- open / close, connect / disconnect, acquire / release, lock / unlock
- start / stop, begin / end, enable / disable, mount / unmount
- encode / decode, serialize / deserialize, compress / decompress
- subscribe / unsubscribe, register / deregister, attach / detach
- authenticate / authorize (a present authN with no authZ is the classic security mirror gap)
- set / clear, fill / invalidate (caches), allocate / free
- do / undo, commit / rollback, apply / revert

## What to do

For each present half, resolve its mirror one of three ways:

1. **Present** — the inverse exists and is specified and tested.
2. **Absent-by-design** — the inverse genuinely should not exist (an append-only audit log has no delete). Record that, with the reason, so the absence is a decision and not an oversight.
3. **Gap** — the inverse should exist and doesn't. Add it (and its tests), or route it to the backlog as a named gap.

The point is that every half is *consciously resolved*. An unresolved half is the bug.

## Anti-patterns

1. **Pairs on paper.** Listing create/delete in the design while only the create path has tests. The mirror exists in name, not in behavior. The inverse needs real coverage ([no-op-paths](../no-op-paths/SKILL.md), [boundary-tests](../boundary-tests/SKILL.md)).
2. **The authZ blind spot.** Treating "we authenticate" as security-complete. AuthN without authZ is the most common and most costly mirror gap.
3. **Mirror-theater.** Inventing inverses that don't belong (a delete for an immutable record) just to satisfy a checklist. Absent-by-design with a reason is a valid resolution; a forced inverse is noise.

## Mechanical enforcement

Largely checkable in a naming-disciplined codebase: for each prefix in the pair list, grep for the present half and its partner, and flag any present half whose partner is missing and not annotated absent-by-design. The judgment is which pairs apply and whether an absence is deliberate; the sweep itself is mechanical.

## Related

- [design-completeness](../design-completeness/SKILL.md) — the broader "does the design name everything a complete design must"; covering the mirror is its symmetry slice.
- [silent-failure-census](../silent-failure-census/SKILL.md) — a missing inverse (no cleanup, no rollback) is often exactly where a leak or silent failure lives.
