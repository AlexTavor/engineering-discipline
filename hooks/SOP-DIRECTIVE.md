# engineering-discipline: standing SOPs

These skills are standard operating procedure. Apply them by reflex while working on code, not only when explicitly asked. At each moment below, if the situation in front of you matches, invoke the named Skill before moving on.

**Writing or reviewing tests**
- `assert-by-shape`: compare the whole returned value against one fixture, not field by field.
- `boundary-tests`: include a case exactly at each numeric limit, not only either side of it.
- `no-op-paths`: include a case where the trigger condition is not met and nothing changes.
- `property-based-testing`: for parsers, validators, classifiers, and rule engines, generate over the input shape instead of a few examples.
- `keep-properties-honest`, `mutation-testing`: when judging whether a green suite would actually fail on a bug.

**Reading or changing unfamiliar code (legacy, inherited, AI-generated)**
- `read-the-system`: read the implementation before claiming how it behaves; a name is a lead, not a fact.
- `footgun-register`: record any name, type, or signature that lies about its behavior.
- `silent-failure-census`: sweep for errors that vanish without a trace.
- `characterize-before-change`, `reproducibility-baseline`: pin current behavior before you touch it.
- `fix-what-you-find`: close a real defect you surface, do not preserve-and-note it.

**Structuring code**
- `cohesion-review`: when a file grows, read the whole module for a second responsibility or duplicated helpers.
- `guard-clauses`: keep the happy path flat with early exits.
- `name-and-bundle`: never repeat a meaningful literal; name it once and derive the rest.
- `decompose-by-attention`: size work to about a minute of planning plus a minute of review.

**Design and delivery**
- `design-completeness`, `one-meaning-per-term`, `requirements-traceability`, `design-assumptions-register`: when writing or reviewing a spec, design, or plan before code.
- `pr-sizing`, `decision-gate`, `derisk-gate`: before committing a change or a costly, hard-to-reverse choice.

To silence the per-edit reminders, create a file named `.no-engineering-sop` in the project root.
