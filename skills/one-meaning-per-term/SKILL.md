---
name: one-meaning-per-term
description: Writing or reviewing a spec, PRD, design doc, API contract, or requirements list, and a key word (user, active, valid, complete, retry, session) could be read two ways. Signs: the spec is confusing, or two people read it differently. Each essential term MUST carry one meaning, or readers diverge and ship a bug no review catches. By the two-meanings test, if you can state two precise, different meanings for one term, split or disambiguate it. Not for prose polish, glossaries, or whether the design covers every case (that is design-completeness).
source: "recovered from git: chdr 9179710, 8a8ab60"
---

# one-meaning-per-term

## Statement

Every load-bearing term in a spec means one thing, and that meaning is pinned once. A term is load-bearing if a reader who takes it the wrong way would build the wrong thing. When one term carries two meanings, or two terms name one thing, two readers (or a human and a parser) silently diverge, and review shows nothing because each reader is sure they understood.

## Why

This is the spec-level form of [footgun-register](../footgun-register/SKILL.md)'s name-that-lies, caught before the code exists. A name in code that does something other than it says is a footgun; a term in a spec that means two things at once is the same trap one layer upstream, and far cheaper to fix there.

The danger is specific to *ambiguity*, not *vagueness*. A vague term ("fast enough") has no clear meaning and everyone knows to ask. An ambiguous term ("the active user") has two clear meanings, and each reader confidently picks one. The most dangerous term in any spec is the one both readers felt sure they understood.

## The two-meanings test

A term is ambiguous (not merely vague) if you can state two specific, different, clear meanings for how it is used:

- "active user" -> (a) currently logged in, or (b) has logged in within 30 days. Both precise, both plausible, behavior differs.
- "retry" -> (a) re-run the whole operation, or (b) resume from the last checkpoint.
- "complete" -> (a) every step ran, or (b) every step succeeded.

If you can write two such meanings, the term is a defect. If you cannot state even one clear meaning, that is vagueness, a different problem: ask for the missing meaning rather than splitting the term.

## What to do

1. **Pin one meaning.** Define the term once, where the spec points to it (a definitions block, a glossary, the first use), as an operational condition you could actually check.
2. **Or split it.** If it genuinely names two things, give them two names ("logged-in user" vs "recently-active user"). One name, one meaning.
3. **Check the inverse too.** Two terms for one thing ("client" / "customer" / "account") is the same defect reversed: it makes readers hunt for a distinction that isn't there. Collapse them.

## Anti-patterns

1. **Defining the obvious, missing the load-bearing.** A glossary full of trivial terms while "valid" quietly carries three meanings across the spec.
2. **Disambiguating with more ambiguity.** "By active we mean engaged" — "engaged" is no clearer. The definition must be operational, a condition with a yes/no answer.
3. **Treating vagueness as ambiguity.** Two readers who both say "I don't know what fast means" have found vagueness; fix it by adding the meaning, not by splitting the term.

## Mechanical enforcement

The judgment (which terms are load-bearing, whether two uses differ) is human; the structure is checkable. A glossary of load-bearing terms, each defined once, can be linted: every glossary term appears in the spec, every term flagged ambiguous in review is in the glossary, and no term is defined twice with conflicting wording. Advisory while the glossary is being built; blocking once the spec commits to its vocabulary.

## Related

- [footgun-register](../footgun-register/SKILL.md) — the same lie one layer down: a code name that contradicts its behavior. This is the spec term that carries two behaviors.
- [requirements-traceability](../requirements-traceability/SKILL.md) — a requirement written with an ambiguous term cannot be traced to a test that means the same thing by it.
- [design-completeness](../design-completeness/SKILL.md) — a complete design stated in ambiguous terms is still unbuildable; these compose.
