# Natural Table Flow and Emphasis Design

## Goal

Make generated mathematical-modeling papers read like deliberately edited
academic work: tables appear beside the argument they support, four independent
tables are not assembled into a 2-by-2 montage or an uninterrupted table wall,
and bold text marks only genuinely important content.

## Layout rules

- Do not combine four independent tables into a 2-by-2 composite merely to save
  space, and do not place four tables consecutively without explanatory prose.
- Keep each retained table close to the method, result, or subproblem it supports.
  Normally place no more than two tables consecutively; insert interpretation
  before the next table.
- Prefer a figure when the reader needs to see a trend or comparison. Retain a
  table when exact values are necessary.
- Split an oversized table by semantic grouping only when the resulting tables
  remain independently understandable. Never shrink text simply to force a
  dense table block onto one page.

## Emphasis rules

- Bold only key conclusions, decisive indicators, core objectives or constraints,
  and important risks or applicability boundaries.
- Keep the emphasized span short, normally a phrase or one sentence.
- Do not bold whole paragraphs, repeat heading emphasis inside the body, bold
  routine transitions, or mechanically bold every table takeaway.
- Bold text must remain sparse and must not replace clear argument structure.

## Verification

Add repository contract tests that require the authoritative skill and layout
references to contain these rules. The tests check policy presence rather than
attempting to score prose style automatically.

## Hash policy

Remove mandatory SHA256/source-hash recording from ordinary manuscript,
typesetting, code-excerpt, and submission-package checks. Builds must still be
reproducible and final artifacts must still pass compilation, visual, anonymity,
archive, and cross-file consistency checks. A source authority may retain a
supplied filename or hash as optional provenance; it is not a required artifact
validation step.

## Scope

Modify `SKILL.md`, `references/paper-structure.md`,
`references/cumcmthesis-template.md`, `references/artifact-consistency.md`,
`references/code-appendix.md`, `references/latex-production-workflow.md`, and
the relevant contract tests. Do not add a formatter, parser, or AI-style scorer.
