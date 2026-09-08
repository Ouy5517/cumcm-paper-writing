---
name: cumcm-paper-writing
description: "Use when planning, drafting, revising, validating, rendering, or packaging Chinese CUMCM papers."
---

# CUMCM Paper Writing

Produce source-grounded Chinese CUMCM manuscripts whose claims, models, code,
figures, layout, and submission files agree. Preserve canonical English method
names, mathematics, variables, units, and citations.

## Route the request

1. Load `manifest.yaml` and every `always_load` file.
2. Detect the implemented `task`, `delivery`, `section`, and `model_family`
   axes. Detect one or more model families actually used with deduplicated loading:
   load each matching fragment once. When multiple sections are requested, load
   their fragments in argument order. For `hybrid`, also load the component
   families actually used.
3. Record the competition year as case metadata. The current calendar year
   must not select a rule set; exact rules require an inspected year-specific
   authority. Read `references/year-selection.md` when the year is unresolved.
4. Apply authority in this order: official CUMCM source; supplied template or
   package; verified dated baseline; CUMCM guidance; non-binding high-impact-
   journal editorial practice.
5. Nature-derived practices may improve argument, evidence placement, captions,
   consistency, and readability. They do not impose journal word, display,
   reference, submission, data, language, landscape-page, or panel rules.

## Evidence gate

Before drafting, lock one sentence:

> In [problem context], we answer [question] using [model/algorithm], supported by [data, derivation, code, or citation], within [assumptions and identifiable boundary].

Record material claims as `VERIFIED`, `UNVERIFIED`, or
`AUTHOR_INPUT_NEEDED`. Never invent observations, parameters, citations, team
facts, validation scores, capacities, blind-test outcomes, or runtime claims.

## Paper contract

Build the shortest sufficient argument and place each result beside its method
and evidence. Do not assemble four independent tables into a 2-by-2 composite.
Normally place no more than two tables consecutively; add interpretation before
more tabular evidence. Bold only short key conclusions, decisive indicators,
objective functions, critical constraints, risks, or applicability boundaries.

For LaTeX delivery or formula repair, load
`references/latex-production-workflow.md`. Preserve structured mathematics and,
when LaTeX was explicitly requested, report missing dependencies without
silently changing renderers.

For engine, template, PDF, or platform-readiness questions, also load
`references/environment-readiness.md`. It distinguishes `ready`,
`ready_with_author_checks`, and `blocked`; a missing engine or fresh PDF is
never hidden by a renderer fallback or an older artifact.

## Submission gate

Load `references/preflight.md` for final PDF, Word, or archive checks. Apply only
verified page, identity, disclosure, and supporting-file rules. Ordinary
verification does not require SHA256 or source hashes. Return the status defined
in `static/core/output-format.md`; do not claim readiness before rendered and
cross-file checks pass.

Load `references/cumcm-practical-faq.md` on demand for practical preflight,
validation, appendix/support-package, or submission questions. Its normalized
guidance never overrides a verified selected-year CUMCM authority.
