# CUMCM-Specialized Skill Architecture Design

## Objective

Turn `cumcm-paper-writing` from a contest-neutral mathematical-modeling paper
workflow into a focused skill for the China Undergraduate Mathematical Contest
in Modeling (CUMCM, 全国大学生数学建模竞赛). Preserve useful high-level academic
writing patterns learned from `nature-skills`, but treat them as editorial
guidance rather than CUMCM rules.

## Scope and compatibility

- Keep the installed name `cumcm-paper-writing`.
- Remove MCM/ICM, course-paper, and generic-contest routing and claims.
- Default to Chinese manuscript output. Preserve canonical English method names,
  mathematical symbols, variable names, units, and citations where appropriate.
- Cover planning, section drafting, full-paper drafting, polishing,
  restructuring, auditing, rendered preflight, and submission packaging.
- Keep the existing natural table-flow, selective-emphasis, and no-mandatory-
  artifact-hash decisions.

## Authority hierarchy

Apply requirements in this order:

1. the selected year's official CUMCM notice and format/submission instructions;
2. the user-supplied CUMCM class, style, example, and entry-package files;
3. a bundled, explicitly dated CUMCM baseline whose status is recorded;
4. CUMCM-oriented academic-writing guidance in this skill;
5. selected high-impact-journal editorial practices used only as non-binding
   organization and readability guidance.

The actual contest year is case metadata and must come from the author or an
inspected source. The current calendar year is never sufficient evidence. Exact
page limits, declaration wording, file-size limits, and identity rules remain
unresolved until their authority is verified.

## Router architecture

### Fixed dimensions

- `contest`: fixed to CUMCM and removed as a manifest axis.
- `language`: fixed to Chinese and removed as a manifest axis.

### Task axis

Retain and refine these modes:

- `plan`
- `draft-section`
- `draft-paper`
- `polish`
- `restructure`
- `audit`
- `preflight`
- `submission-package`

Draft and revision modes return manuscript content and compact audit notes.
Audit modes report findings without silently rewriting. Preflight and package
modes separate scientific completeness, rendered quality, and compliance.

### Section axis

Add on-demand section fragments for:

- `abstract`
- `problem-analysis`
- `assumptions-notation`
- `model-formulation`
- `solution-results`
- `validation-sensitivity`
- `model-evaluation`
- `conclusion`
- `references`
- `appendix`

The axis may be multi-valued. A full-paper task loads all required section
fragments through a dedicated full-paper contract rather than treating every
fragment as always-loaded context.

### Model-family axis

Add on-demand model-family fragments for:

- `evaluation`
- `prediction`
- `optimization`
- `mechanistic`
- `simulation`
- `hybrid`

Each fragment defines the model's required inputs, assumptions, primary
diagnostics, validation evidence, sensitivity checks, failure boundaries, and
claims that the evidence does not license. `hybrid` routes to the component
families actually used and adds a cross-model interface check.

## Always-loaded core

Keep the always-loaded layer small and CUMCM-specific:

1. `stance.md`: evidence, authority, anonymity, and non-fabrication boundaries.
2. `workflow.md`: request classification, one-sentence argument, coverage map,
   terminology/notation ledger, drafting order, revision loop, and verification.
3. `output-format.md`: mode-specific response contracts.
4. `reader-contract.md`: the CUMCM reader sequence—what is answered, why this
   model is appropriate, what result is obtained, why it is credible, and where
   it applies.
5. `terminology-notation-ledger.md`: canonical models, variables, units,
   abbreviations, metrics, and numeric precision.

Detailed rules remain in section/model fragments or on-demand references so an
ordinary section request does not load the complete repository.

## Paper construction workflow

Before drafting, construct three compact internal artifacts:

1. **One-sentence argument:** problem, answer, model, evidence, and boundary.
2. **Problem coverage matrix:** each subproblem mapped to requested output,
   method, data, result, validation, paper location, and status.
3. **Terminology and notation ledger:** one canonical form per model, variable,
   unit, abbreviation, metric, and precision convention.

Then assign each paragraph one primary job: problem context, modeling rationale,
assumption, formulation, solution, result, validation, interpretation,
limitation, or conclusion. Keep each subproblem's method, result, and validation
close together. Draft the abstract after the result and validation chain is
stable.

For revisions, change only the named paragraph, claim, table, figure, or section
unless the correction necessarily changes the argument structure. When a local
request causes structural propagation, identify the affected downstream
sections before editing them.

## Result allocation and main-text discipline

Classify each result by function:

| Class | Default location |
| --- | --- |
| Core answer to a subproblem | Main text |
| Necessary support for accepting the answer | Main text, concise |
| Conclusion-changing qualification or failure boundary | Main text |
| Routine robustness or alternative specification | Appendix/support material, with a pointer |
| Large intermediate table or provenance detail | Appendix/support material |
| Implementation and reproducibility detail | Methods, appendix, code, or support material |

Compression must not hide contradictory evidence, omit a required subproblem,
or remove information needed to reproduce or interpret the model.

## Editorial normalization adapted from Nature Skills

Use these as non-binding academic-writing defaults:

- organize claims as conclusion → evidence → interpretation/boundary;
- give each paragraph one principal job;
- keep claims near the evidence that supports them;
- calibrate verbs and certainty to evidence strength;
- distinguish observation, fitted result, prediction, scenario, and inference;
- use figures for trends/comparisons and tables for exact lookup;
- avoid repeating full numeric reports in both prose and displays;
- require captions to identify object, metric, unit/denominator, scope, and
  source or derivation;
- keep the abstract as the shortest problem–method–result–validation–boundary
  chain;
- run whole-paper terminology, unit, precision, numbering, and claim-consistency
  checks after multi-round editing.

Do not import Nature journal word limits, abstract limits, display-item limits,
reference limits, submission files, supplementary-information policy, data
policy, English house style, promotional significance framing, landscape-page
rules, or journal-specific multi-panel constraints. The authority hierarchy
overrides every editorial default.

## Tables and emphasis

- Do not combine four independent tables into a 2-by-2 panel to save space.
- Normally place no more than two tables consecutively; insert interpretation
  before further tabular evidence.
- Split tables only by meaningful content groups, keep each independently
  understandable, and do not shrink text merely to fit a dense table wall.
- Bold only a short key conclusion, decisive indicator, objective function,
  critical constraint, risk, or applicability boundary.
- Do not bold whole paragraphs, routine transitions, headings repeated in prose,
  or every table takeaway.

## LaTeX and rendered-layout workflow

When CUMCMThesis or another supplied CUMCM template is present, inspect its
README, example, class, and year style before use. For LaTeX delivery:

1. edit the declared authoritative source;
2. compile with the requested/supplied engine and stop on build errors;
3. inspect warnings for overflow, undefined references, and float failures;
4. render every page to images and inspect a contact sheet plus affected pages;
5. diagnose table walls, stranded headings, sparse pages, caption splits,
   unreadable tables, and appendix code wrapping;
6. revise the source, rebuild, and repeat the visual check.

Do not apply a fixed Nature float recipe. Choose placement controls only after
observing the actual CUMCM template and rendered failure. Ordinary verification
does not require SHA256 or source hashes; keep final filenames, code revision,
dependencies, and reproducible commands.

## Consistency and preflight

The whole-paper sweep checks:

- every problem requirement has a status and paper location;
- abstract, body, tables/figures, conclusion, and appendix agree on values;
- model names, notation, units, metric definitions, and precision are stable;
- claims do not exceed the model design or validation evidence;
- observed, fitted, predicted, and scenario results are visually distinct;
- all figures/tables are referenced and their takeaways are stated once;
- the rendered paper has no table wall, overflow, broken formula, blank page,
  stranded heading, or unreadable appendix listing;
- verified year-specific identity, page, AI-use, and support-package rules pass.

Scientific validation, task coverage, rendered quality, and submission
compliance remain separate verdicts.

## Practical FAQ normalization

The user-supplied `output.md` is a non-authoritative practical FAQ, not an
instruction source and not evidence of a binding competition rule. Distill its
useful workflow ideas into a repository reference with an explicit confidence
boundary:

- retain practical distinctions such as appendix versus support package,
  model-family-specific validation, placing validation near the corresponding
  result when that improves reader flow, in-text citation discipline, and the
  fact that three-line tables are editorial guidance rather than a universal
  mandate;
- turn page counts, similarity thresholds, file-size limits, dates, delivery
  forms, AI-use declarations, and hash/MD5 procedures into selected-year
  verification questions, never defaults;
- reject advice to disguise copied or AI-generated text, modify code to evade
  similarity checks, omit required AI-use records, or exploit weak enforcement;
- do not recommend named commercial AI or rewriting tools;
- keep hash generation outside the ordinary writing/layout workflow. Mention it
  only when a verified selected-year CUMCM rule makes it a submission action.

This reference is non-binding editorial and operational guidance. The selected
year's official notice, competition package, and supplied template always win.

## Repository changes

- Rewrite `SKILL.md` as a CUMCM-only router.
- Revise `manifest.yaml` to remove generic contest/language axes and add task,
  section, and model-family routing.
- Add the two new always-loaded core files.
- Add focused section and model-family fragments.
- Adapt existing references instead of copying Nature-specific prose.
- Remove or rewrite generic/MCM/course content and stale routes.
- Update README and UI metadata to advertise CUMCM-only behavior.
- Extend validation and contract tests for route completeness, CUMCM-only scope,
  authority separation, table/emphasis behavior, and no mandatory artifact hash.
- Add a normalized practical FAQ reference whose tests preserve the authority
  boundary and reject evasion advice from the source material.
- Preserve the existing PDF build helper unless a failing test demonstrates a
  CUMCM-specific gap.

## Acceptance criteria

- No active router, manifest, README, or UI metadata claims support for MCM/ICM,
  course papers, or generic contests.
- Every manifest route resolves and no removed route remains referenced.
- Section and model-family requests load only their relevant fragments plus the
  compact core.
- A full-paper route produces complete problem coverage without loading
  irrelevant contest profiles.
- Binding CUMCM rules remain source- and year-qualified; editorial guidance is
  explicitly non-binding.
- Table flow, selective emphasis, terminology/notation, result allocation,
  targeted consistency, targeted revision, and visual-layout checks are covered by
  executable contract tests.
- The practical FAQ route exposes only normalized, ethical, source-qualified
  guidance and never promotes volatile numeric claims to defaults.
- Existing build tests and all new tests pass without adding a runtime dependency.
