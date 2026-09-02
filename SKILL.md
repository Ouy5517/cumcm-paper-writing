---
name: cumcm-paper-writing
description: "Use when planning, drafting, restructuring, reviewing, formatting, or packaging a China Undergraduate Mathematical Contest in Modeling (CUMCM) paper. It covers source-grounded claims, mathematical-model sections, anonymity, citations, runnable code, appendices, physical/electronic submission separation, and current-year preflight."
---

# CUMCM Paper Writing - Router

This skill follows a static-core plus dynamic-fragments design modeled on the
local nature-skills-main project. The router keeps default context small:
contest rules, evidence guidance, and preflight checks are loaded on demand.
Treat the current year's official notice and format specification as
authoritative; use the bundled 2026 baseline only when no newer rule is supplied.

## Route the task

Follow these steps every time this skill is invoked.

### 1. Load the manifest and core

Read manifest.yaml and every file listed under always_load. The manifest
declares the supported axes and the file paths for each selected fragment.

### 2. Detect the request axes

Classify and state one short line with:

- task: plan, draft-section, draft-paper, restructure, audit, preflight, or
  submission-package.
- year: the named year, or current when the official year is not supplied.
- delivery: source, rendered, electronic, physical, or both.
- language: normally zh for a Chinese request; preserve canonical English
  algorithm and method names.
- problem/group/stage: selected problem (A-E when applicable), undergraduate
  group, and physical/electronic stage.

Ask only when an ambiguity changes the paper structure or submission package.
If the user asks for immediate drafting, proceed with explicit placeholders.

### 3. Load only the selected fragments

Read the mapped task, delivery, and language fragments. Read on-demand
references only when their conditions in the manifest are met:

- exact year rules -> references/requirements.md;
- full outline -> references/paper-structure.md;
- claim provenance or reproducibility -> references/evidence-ledger.md;
- final PDF/Word/archive check -> references/preflight.md;
- exact Chinese labels/declarations -> references/chinese-quick-reference.md.

Do not read every reference file. This is part of the token-efficiency
contract.

### 4. Apply the evidence gate

Before long prose, establish a claim-evidence-boundary record:

> In [problem context], we answer [question] using [model/algorithm],
> supported by [evidence], within [assumptions and boundary].

For each material claim, record its evidence/source, derivation or code
location, scope, and status: VERIFIED, UNVERIFIED, or AUTHOR_INPUT_NEEDED.
Do not invent observations, coefficients, model outputs, citations, team
facts, validation scores, or runtime claims. Use an explicit author-input
placeholder for missing Chinese inputs and [MISSING: ...] for missing English
inputs.

### 5. Build and draft the paper map

Use the shortest sufficient chain:

problem restatement -> assumptions -> notation -> model formulation ->
solution/algorithm -> results -> validation/sensitivity ->
conclusions/limitations -> references -> appendix.

Define every symbol and unit before reuse. Keep each paragraph focused on one
job. Put a result beside the method and evidence that support it. Draft the
abstract after the result ledger is stable; never add unsupported numbers to
the abstract or conclusion.

### 6. Enforce contest boundaries

Apply the selected year's official notice. The bundled 2026 baseline uses
white A4, margins of at least 2.5 cm, an abstract-only first electronic page,
no table of contents, a body limit of no more than 30 pages, and an appendix
with the file list and complete runnable source programs. The electronic paper
is one uncompressed PDF/Word file within the selected 20MB limit; supporting
files are one anonymous ZIP/RAR within the selected 20MB limit.

Separate physical and electronic packages:

- physical-only consent and numbering pages stay out of electronic files;
- anonymous sections, metadata, filenames, archive paths, and code comments
  must not reveal contestant, institution, or division;
- current-year entry and AI-use notices override this baseline when supplied;
- unspecified font, size, line spacing, and color must not be invented as
  universal contest rules.

### 7. Return the mode-specific contract

Use static/core/output-format.md. Every result must include assumptions or
missing inputs and a status of ready, ready_with_author_checks, or blocked.
Use ready_with_author_checks when author verification, official notice
confirmation, citation verification, code execution, rendered-layout
inspection, or file-size checking remains.

### 8. Run preflight before claiming completion

For final or submission-related work, read references/preflight.md, inspect
the rendered artifact when layout is in scope, and report PASS, FAIL, or
AUTHOR CHECK for each check group. A paper is not ready merely because its
Markdown or LaTeX source looks complete.

## Revision rule

When the author flags a paragraph or result, make a targeted edit and preserve
unflagged material. Return to the alignment gate only if the correction
changes the central claim, section architecture, or evidence boundary.
