---
name: cumcm-paper-writing
description: "Use when drafting, reviewing, rendering or packaging mathematical modeling competition papers for CUMCM, MCM/ICM, other contests or course exercises, including model validation and concise code appendices."
---

# CUMCM Paper Writing

The installed name is retained for compatibility. This workflow is contest-neutral.
Read references/contest-profile.md before applying formatting or submission rules.
Only verified rules for the selected contest and year are binding; historical
CUMCM notes are not defaults for other contests. Read references/problem-coverage.md
and references/model-validation.md for full papers. For production and revision,
read references/artifact-consistency.md and references/code-appendix.md.

## Overview

Produce a source-grounded competition paper whose claims, code, figures, layout, and submission files agree. Apply the current official notice and a supplied template before generic writing conventions.

## Route the request

1. Read `manifest.yaml` and every `always_load` file.
2. Detect contest, task, delivery and language; record the actual year separately. Select `restructure` only for an existing manuscript revision. Read every matching fragment, deduplicating paths. Unknown contests use generic. Year-specific historical CUMCM references are loaded only for CUMCM.
   Unknown year remains unresolved: read `references/year-selection.md`; never infer an official rule from the current calendar year.
3. Apply authorities in this order:
   - current-year official notice and format specification;
   - user-supplied class/style/example files;
   - bundled year baseline;
   - general academic-writing advice.
4. When a `CUMCMThesis` or `cumcmthesis` folder is supplied, inspect its README, example source, class, and year style; then read `references/cumcmthesis-template.md`.
5. For LaTeX PDF delivery or formula repair, read `references/latex-production-workflow.md`. If LaTeX is explicitly requested, missing dependencies must be reported with the preserved source; do not silently switch renderers. Otherwise choose a math-capable renderer compatible with the requested format. Never flatten structured mathematics into formula-shaped text.

## Evidence gate

Before drafting, lock one sentence:

> In [problem context], we answer [question] using [model/algorithm], supported by [data, derivation, code, or citation], within [assumptions and identifiable boundary].

Record each material claim in the evidence ledger as `VERIFIED`, `UNVERIFIED`, or `AUTHOR_INPUT_NEEDED`. Never invent observations, parameters, citations, team facts, validation scores, capacities, blind-test outcomes, or runtime claims. Keep fitted and extrapolated results visually distinct from observations.

## Paper contract

Build the shortest sufficient chain:

problem restatement -> problem analysis -> assumptions -> notation -> model formulation -> solution -> results -> validation/sensitivity -> model evaluation -> conclusions/limitations -> AI-use statement -> references -> appendix.

- Draft the abstract after results are fixed; place title, summary, keywords and other front matter as the selected profile requires.
- Put each result beside its method and evidence. Number and reference equations, tables, and figures consistently.
- Use figures for patterns and comparisons, tables for exact lookup, and three-line tables when the supplied template does.
- Give every figure/table a neutral caption, units or denominator, and enough source/scope context to prevent overclaiming.
- Retain complete runnable code in the engineering project. Select full/core/no code listings using references/code-appendix.md and verified contest rules.

## Submission gate

For electronic delivery read `references/preflight.md` and the contest profile. Apply its verified page, identity, disclosure and supporting-file rules. Chinese CUMCM declarations apply only to a verified CUMCM requirement.

Return the required status from `static/core/output-format.md`. Do not claim readiness until the rendered PDF and support archive pass visual, size, anonymity, code, figure, and cross-file consistency checks.

## Quick reference

| Need | Read |
| --- | --- |
| Exact year limits and submission rules | `references/requirements.md` |
| Full paper architecture | `references/paper-structure.md` |
| Supplied `cumcmthesis` layout | `references/cumcmthesis-template.md` |
| LaTeX PDF, formula fidelity, and support packaging | `references/latex-production-workflow.md` |
| Claim provenance | `references/evidence-ledger.md` |
| Final rendered/package check | `references/preflight.md` |

## Common failures

- Copying a sample template's demonstration text, identity fields, or decorative boxes into the competition paper.
- Calling observed `d(c)` values a system rerun or causal policy effect.
- Using full-grid tables when the selected template expects three-line tables.
- Omitting figure captions, denominators, AI-use disclosure, complete code, or support-file inventory.
- Treating a successful source build as proof that the final PDF is readable.
- Replacing `\sum`, `\frac`, subscripts, or superscripts with `_()`, `^()`, or other plain-text approximations.
