---
name: silent-failure-census
description: Sweep a codebase for places that can fail without a trace — swallowed exceptions, ignored error returns, fire-and-forget tasks, unchecked subprocess exits — and record each with its location and a real-vs-benign classification. Use when assessing inherited or AI-generated code, or whenever you need to know where a system could be broken while still looking healthy.
source: "recovered from git: chdr 2fa9318, 2c418bd; PDD 06c467f, c3148b5, 909ce9c"
---

# silent-failure-census

## Statement

A trustworthy read of unfamiliar code MUST include a **census of silent-failure sites**: every place an error can be lost — a swallowed exception, an ignored failure return, an unwatched background task, an unchecked subprocess exit — located (`file:line`) and classified *real risk* vs *benign*.

## Why

A suite can be all-green while the system is broken, for two reasons. One is tests that do not actually constrain behavior. The other is a **visibility gap**: the error happened, but nothing surfaced it — no log, no metric, no failed return — so every check stays green. This census recovers the second case; it is the visibility half of the diagnostic.

## When to apply

- When assessing inherited, legacy, or AI-generated code, as the visibility half of the picture.
- Any time you need to know where a system could break while still looking healthy — before trusting a green suite on inherited code.

## Protocol — lexical seeds → read → classify

Seeds tell you where to look; reading decides whether it is real ([read-the-system](../read-the-system/SKILL.md) applies):

1. **Swallowed exceptions** — empty `catch {}`; a catch that logs at debug and continues; a catch-all (`catch (e) {}`, `except:`) that is not at a surfacing boundary.
2. **Ignored failure returns** — a value that signals failure (a status, `ok`, an error object, `-1`) discarded at the call site.
3. **Fire-and-forget** — a promise / future / goroutine / thread started with nothing awaiting or watching it finish (a floating `void` promise, a detached task).
4. **Unchecked subprocess** — a child process whose exit code and stderr are never inspected.
5. **Tests that hide a broken build** — a try / except around an import or collection that turns a failure into a pass.

For each hit: read it, then classify **real** (a failure here would go untraced) or **benign** (genuinely recovered with a visible trace, or a boundary whose job is to surface).

## Outputs

A census artifact: site, kind, classification, one-line rationale. Real-risk sites feed the risk register; the worst become the first fix targets ("handle it or let it propagate").

## Anti-patterns

1. **Count-without-reading.** "47 catch blocks" is not a census. A catch at a surfacing boundary is correct; only reading separates real from benign.
2. **Treat-all-catches-as-bugs.** A boundary catch that logs visibly and recovers to a known state is the *good* pattern, not a finding.
3. **Census-without-classification.** A flat list of sites with no real / benign verdict pushes the judgment downstream and buries the ones that matter.

## Mechanical enforcement

Several seeds are lintable: empty catch, floating promise, ignored return, missing subprocess exit check (rules in the `no-floating-promises` / unused-expression / unchecked-return families). The lint finds candidates; the census *classifies* them. Advisory at first; the real-risk subset becomes blocking.

## Related

- [read-the-system](../read-the-system/SKILL.md) — classify each seed by reading, not by pattern.
- [footgun-register](../footgun-register/SKILL.md) — the sibling sweep: names that lie about behavior.
