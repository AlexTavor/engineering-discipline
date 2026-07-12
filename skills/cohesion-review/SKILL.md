---
name: cohesion-review
description: When a change appends to a module that already exists (a new function, another case, another gate), review the WHOLE resulting module for cohesion, not just the diff. Use this on any PR that GROWS a file rather than adding a new one, the moment a linter flags a file for size or complexity, or whenever you catch yourself copying a helper. Read the accreted module fresh and ask whether it still does one thing and does it once, or whether it has grown a second responsibility and now holds two helpers that compute the same thing under different names. Per-PR diff review optimizes the increment and never sees the artifact the increments accrete into, which is how a clean file becomes a duplicated monolith one reasonable diff at a time. This is the human cohesion checkpoint: the linter owns mechanical structure (size, complexity, token-identical copy-paste), test-adequacy grading owns whether the tests bite, this owns the semantic duplication and responsibility-drift neither can see. Reach for it even when the user only says a file feels big, that they are about to add yet another function to a growing module, or that a file is getting hard to hold in their head. Not for sizing a unit of work before doing it (that is decompose-by-attention) or for bundling changes into PRs (that is pr-sizing).
source: "recovered from git: chdr 9fbe493, 0532325; PDD 9b775a4, b01e619"
---

# cohesion-review

## Statement

When a change appends to a module that already exists, review the whole resulting module, not just the diff. The unit of review is the accreted file as it now stands, read fresh, not the lines this change touched. Ask one question: does this module still do one thing, and does it do it once? A module that has grown a second responsibility, or that holds two helpers computing the same thing under different names, is a defect even when every individual diff that built it was reasonable and every gate is green.

## Why

Per-PR review optimizes the increment, not the artifact. Each diff is small and sensible: add a gate, add a helper, handle one more case. The reviewer reads the diff, it looks fine, it ships. Nobody re-reads the whole file, because the whole file was reviewed "last time", except last time it was a different, smaller file. So the module accretes: a clean 120-line file becomes a 795-line monolith one reasonable diff at a time, and the duplication that crept in (the same setup copied for each new case, two helpers that drifted into the same logic under different names) is invisible in any single diff because each copy arrived in a different PR.

The mechanical tools do not catch this. A size or complexity linter fires only AFTER the file is already too big, and it cannot see that two short helpers compute the same thing. A copy-paste detector matches token-identical blocks, so it misses a `base_name` and a `leftmost_name` that walk the same chain with different variable names. Test-adequacy grading checks whether the code is tested, not whether it is cohesive. The one review that would catch accretion, reading the grown module as a whole, is the one no per-diff process performs. This skill is that review.

Worked case (real): a Python gate-pack's `run.py` grew across four PRs, one capability each (mutants, no-op-paths, boundary-tests, dead-branch). Every diff added one self-contained function and passed review. At 795 lines the accreted whole held the per-file `MetadataWrapper(...).resolve()` setup copied four times, `enclosing_fn` defined twice, and three pairs of same-logic helpers under different names (`base_name`/`leftmost_name`, `num`/`num_value`, `chain_to`/`within`). No diff introduced more than one copy, so no diff review could see the duplication. A cohesion read at the third append ("we are copying the parse loop again, and this file now does four jobs") would have carved the shared module then, instead of after it hit 795 lines.

## The cohesion read

When a change grows an existing module, before approving it:

1. **Read the whole module, not the diff.** Open the file as it will stand after the change and read it top to bottom as if for the first time. The diff is what changed; the module is what ships.
2. **State its job in one sentence.** If the honest sentence needs an "and" or an "also" ("parses the config AND runs the gates AND formats the report"), the module has grown past one responsibility. Each extra clause is a candidate to split out.
3. **Scan for two-names-one-logic.** Look for functions that compute the same thing under different names, the same loop or setup copied per case, two parsers of one shape. This is the duplication the tools miss; only a human reading the whole file sees that `base_name` and `leftmost_name` are the same walk.
4. **Check the shared scaffolding.** If the new case copied setup the earlier cases also have (the parse loop, the same guard, the same fixture builder), that scaffolding wants hoisting into one shared helper now, before the next case copies it again.

## The verdict

The read ends in one of three calls, made deliberately at the moment of growth:

- **Cohesive, ship it.** One job, no duplication. The append earned its place.
- **Carve a shared helper.** The append duplicated scaffolding or a helper; extract the shared piece. Often this rides as a small refactor in the same PR. If it is large, it is a logged fast-follow, so it is not forgotten.
- **Split the responsibility.** The module now does two jobs; separate them. Usually a follow-up PR, not a blocker on the feature, but the decision is recorded, not deferred by default.

The point is to make the call on purpose when the module grows, not to let "it is only one more function" run until the file is unreadable.

## When NOT to use

- **A brand-new file.** Nothing has accreted yet, so there is no whole-module history to review. Size it with [decompose-by-attention](../decompose-by-attention/SKILL.md) instead.
- **A change that does not grow a module** (a one-line fix, a rename, a config edit). Cohesion review is triggered by accretion, not by every change.
- **Duplication in prose or a spec.** Two terms for one concept in a design doc is [one-meaning-per-term](../one-meaning-per-term/SKILL.md); this is two helpers for one logic in code.

## Mechanical enforcement

The cue to run the review is mechanical; the review is human. A hook can flag a PR that adds lines to an existing module (rather than creating a new file), or a file that crossed a size or complexity threshold, and prompt "read the whole module for cohesion." It can even surface candidate duplicate helpers by structural similarity. But whether two helpers are truly the same logic, and whether a module's second cluster is a separate responsibility, is a judgment a tool cannot make. So flag and prompt mechanically, decide by a human read: advisory prompt, human verdict, never an auto-block.

## Related

- [decompose-by-attention](../decompose-by-attention/SKILL.md): sizes a unit of WORK to about a minute of planning plus a minute of review. This applies the same attention budget to the ARTIFACT the work accretes into: a module you can no longer hold in one read has grown too big or too multi-purpose.
- [one-meaning-per-term](../one-meaning-per-term/SKILL.md): the spec-level cousin, two terms for one concept (or one term for two). This is its code-level form, two helpers for one logic.
- [footgun-register](../footgun-register/SKILL.md): a name that lies about its behavior. The two-names-one-logic here is the adjacent defect, two honest names for the same behavior.
- [pr-sizing](../pr-sizing/SKILL.md): how to bundle changes into PRs (one operator milestone each). Cohesion review is what you run on the module a PR grows, however the PRs are bundled.
