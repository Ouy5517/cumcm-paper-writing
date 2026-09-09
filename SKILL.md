---
name: cumcm-paper-writing
description: "Solve and write Chinese CUMCM problems from task decomposition, data or parameter audit, model formulation and computation through validation, paper drafting, rendering and submission packaging. Use for 国赛建模、数模全流程、模型选择、求解验证、论文写作与审查."
---

# CUMCM Modeling and Paper Workflow

Develop source-grounded CUMCM solutions and Chinese manuscripts whose claims, models, code,
figures, layout, and submission files agree. Preserve canonical English method
names, mathematics, variables, units, and citations.

## Route the request

1. Load `manifest.yaml` and every `always_load` file.
2. Detect the implemented `task`, `delivery`, `section`, and `model_family`
   axes. Detect one or more model families actually used with deduplicated loading:
   load each matching fragment once. When multiple sections are requested, load
   their fragments in argument order. For `hybrid`, also load the component
   families actually used.
   Use `full-workflow` for an end-to-end problem; load its next task fragment
   as each subquestion advances. Several independent models do not by themselves
   require `hybrid`. A local polish needs only its affected passage and claims;
   do not require a new whole-paper plan or ledger for a one-sentence edit.
3. Record the competition year as case metadata. The current calendar year
   must not select a rule set; exact rules require an inspected year-specific
   authority. Read `references/year-selection.md` when the year is unresolved.
4. Apply verified selected-year official CUMCM sources to competition rules.
   Supplied templates implement typography; case papers and dated summaries
   supply examples or research pointers. Neither proves an official rule.
   User formatting preferences apply within the official requirements.
5. Nature-derived practices may improve argument, evidence placement, captions,
   consistency, and readability. They do not impose journal word, display,
   reference, submission, data, language, landscape-page, or panel rules.

## Evidence gate

Before solving, write a provisional one-sentence argument with unknown answers
explicit. Stabilize it after results and validation, before final prose:

> In [problem context], we answer [question] using [model/algorithm], supported by [data, derivation, code, or citation], within [assumptions and identifiable boundary].

Record material claims as `VERIFIED`, `UNVERIFIED`, or
`AUTHOR_INPUT_NEEDED`. Never invent observations, parameters, citations, team
facts, validation scores, capacities, blind-test outcomes, or runtime claims.
For formal competition work, preserve team ownership of the core reasoning and
record actual human review of AI-assisted steps. Never mark a review complete
on the team's behalf. Check the selected-year AI rules before packaging.

When a problem contains multi-object geometric design, nested composition data,
sampling-driven decisions or rework accounting, load `references/distilled-playbooks.md`
and only the case whose operational structure applies. A simple production
quantity problem does not need a historical rework case merely because both
mention production. These are conditional lessons, not award rules or ready-made solutions.
A new topic can use the common workflow without a matching case. Keep source
files outside the installed skill.
For time-dependent physical equations, event scheduling, or dated forecasts,
load the applicable section of `references/temporal-validation.md`; it links
the matching archive case without requiring every historical paper.

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

## Submission gate

Load `references/preflight.md` for final PDF, Word, or archive checks. Apply only
verified page, identity, disclosure, and supporting-file rules. Ordinary
verification does not require SHA256 or source hashes. Return the status defined
in `static/core/output-format.md`; do not claim readiness before rendered and
cross-file checks pass.

Load `references/cumcm-practical-faq.md` on demand for practical preflight,
validation, appendix/support-package, or submission questions. Its normalized
guidance never overrides a verified selected-year CUMCM authority.
