---
name: reproducibility-baseline
description: Before changing behavior-critical code, establish a baseline that can prove the change didn't alter behavior — replay-and-diff if the system is deterministic, else golden-master/snapshot or injected seams for the clock, RNG, and I/O. Determinism is the easy case, not an assumption: when a snapshot or replay test flakes, inject the seam that makes it reproducible instead of deleting the test. Use to build the no-drift baseline before you change behavior-critical code; the later preservation check diffs against it, and making the system reproducible is itself a remediation deliverable. For pinning specific behaviors as the recovered spec, see characterize-before-change — this is the baseline they're checked against.
---

# reproducibility-baseline

## Statement

Before you change behavior-critical code, you MUST establish a baseline that can prove the change didn't alter behavior — by the strongest means the system admits: replay-and-diff if it's deterministic; golden-master, snapshot, or injected seams for the clock, RNG, and I/O if it isn't. Determinism is the easy case, not an assumption you get to make.

## Why

To prove *nothing broke*, you need something to diff against. When the system is deterministic, replay-and-diff is the gold standard: run the same inputs before and after, assert identical output. But most real systems leak nondeterminism — a clock, a seed, an I/O call, a `Map` iteration order — so naive replay flakes, and the reflex is to give up and test by a handful of examples. That throws away the strongest proof you had.

The move is the opposite: make the system reproducible. Pin the seed, inject the clock / RNG / I/O as seams, normalize the ordering, snapshot the output as a golden master. **Making it reproducible is itself a remediation deliverable** — it's the capability every later preservation check diffs against.

Worked case: a reconciler is "tested" by snapshotting its output and diffing each run. The snapshots flake — the output embeds `Date.now()` and a `Map` whose order isn't stable. The reflex is to delete the snapshot as flaky. The right move is the inverse: inject the clock as a seam and sort the collection, turning a flaky snapshot into a golden master strong enough to prove any future change preserved behavior.

## When to apply

- On behavior-critical code you're about to change — to capture the no-drift baseline.
- When proving the change preserved behavior, the baseline is what the preservation diff runs against — this skill builds that capability; running the diff is the change's own job.
- Whenever a snapshot or replay test flakes — that's the signal to inject a seam, not to delete the test.

## Protocol

1. **Pick the strongest means the system admits.** Deterministic → replay-and-diff. Non-deterministic → make it reproducible (seams + golden master); don't drop to examples.
2. **Find the nondeterminism** — clock, RNG, I/O, environment, iteration / `Map` order, ids and addresses. Each is a seam to inject or a value to normalize.
3. **Capture the baseline on the unchanged code** — a golden master of current output, or a recorded replay, taken *before* you edit.
4. **Diff against the baseline** by structural equality, not resemblance — first to confirm the baseline reproduces, then to prove the change preserved behavior.
5. **Keep the reproducibility as a deliverable** — the injected seams and pinned seeds stay in the codebase; they are what every later preservation check relies on.

## Anti-patterns

1. **Assume-determinism.** Treating the system as deterministic without checking — then replay flakes and the test takes the blame.
2. **Delete-the-flaky-snapshot.** Removing a snapshot / replay test because it flakes, instead of injecting the seam that makes it reproducible — throwing away the strongest proof you had.
3. **Fall-back-to-examples.** Abandoning replay / golden-master for a few example assertions because reproducibility "is hard" — examples can't prove no-drift over the whole output.
4. **Diff-by-eyeball.** "It looks the same" — preservation is an equality check, not a vibe.

## Mechanical enforcement

Strong, once built: a replay or golden-master diff runs in CI and fails on any drift, automatically. The judgment is up front — which seams to inject, what counts as the canonical output. Seed-pinning and banning `Math.random` / `Date.now` in the engine are lintable (one codebase enforces exactly this). *(`Date.now` / `Math.random` / `Map` are JS; the seams are language-agnostic.)*

## Related

- [characterize-before-change](../characterize-before-change/SKILL.md) — the other half of locking behavior: pinning specific behaviors in tests.
- [properties](../properties/SKILL.md) — a determinism property (same input → same output, ids stable) is a reproducibility baseline.
- [read-the-system](../read-the-system/SKILL.md) — finding the seams means reading where nondeterminism enters.
