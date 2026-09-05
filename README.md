# CUMCM Paper Writing

A source-grounded Codex Skill for planning, drafting, reviewing, formatting,
and packaging papers for the China Undergraduate Mathematical Contest in
Modeling (CUMCM).

## What it does

- Routes requests by task, contest year, delivery format, and language.
- Supports planning, section drafting, full-paper drafting, restructuring,
  audit, preflight, and submission-package preparation.
- Separates physical-paper and electronic-submission requirements.
- Enforces claim/evidence/boundary tracking and prevents fabricated results,
  citations, team facts, or validation.
- Covers anonymity, reproducible source programs, appendices, references, and
  supporting ZIP/RAR archives.
- Applies supplied `CUMCMThesis` class/style/example conventions, including
  three-line tables, numbered figures, and current-year AI-use placement.
- Provides a reproducible `paper.tex` → XeLaTeX → PDF workflow with formula
  fidelity checks, every-page rendering, anonymity scans, and SHA256 recording.
- Loads detailed references on demand to keep context usage small.

## Installation

Copy this directory into the Codex skills directory:

    %CODEX_HOME%\skills\cumcm-paper-writing

If CODEX_HOME is not set, use:

    %USERPROFILE%\.codex\skills\cumcm-paper-writing

## Usage

Invoke it explicitly with:

    $cumcm-paper-writing

For a final paper or submission check, provide the contest year and the
current official notice when available. The official notice and
division-specific requirements override the bundled baseline.

For PDF generation, also provide the `CUMCMThesis` template directory when it
is not already in the project. The workflow expects XeLaTeX (MiKTeX or TeX Live),
Poppler tools such as `pdfinfo` and `pdftoppm`, and the project's analysis/test
runtime. It produces `paper.tex`, `paper.pdf`, rendered QA pages, a support
archive, and verification hashes.

## Project layout

    SKILL.md                 Router and core behavior
    manifest.yaml            Axis detection and lazy-loading map
    static/core/             Shared stance, workflow, output, and baseline
    static/fragments/        Task, delivery, and language fragments
    references/              Detailed rules, LaTeX workflow, evidence, and preflight
    tests/                   Skill workflow contract tests
    agents/openai.yaml       Codex UI metadata

## Scope

### Validation and build tools

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python scripts/build_pdf.py path/to/paper.tex --output path/to/paper.pdf --template-dir path/to/CUMCMThesis
```

The builder requires XeLaTeX on PATH (or `--engine`), resolves figures relative
to the TeX directory, checks two compilation passes, and preserves an existing
PDF on failure. Visual and scientific validation remain separate checks.
Historical competition limits are unverified notes until tied to the selected
year's original notice; see [year selection](references/year-selection.md).

The student-advisor example integration currently has design and implementation
plans only. Its data and runnable case have not yet been published in this repo.

This is a writing and quality-control workflow, not an official contest
template or legal interpretation. Authors remain responsible for checking the
current notice, division rules, data permissions, code execution, and the final
rendered files before submission.
