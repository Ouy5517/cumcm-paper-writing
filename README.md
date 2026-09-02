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

## Project layout

    SKILL.md                 Router and core behavior
    manifest.yaml            Axis detection and lazy-loading map
    static/core/             Shared stance, workflow, output, and baseline
    static/fragments/        Task, delivery, and language fragments
    references/              Detailed rules, structure, evidence, and preflight
    agents/openai.yaml       Codex UI metadata

## Scope

This is a writing and quality-control workflow, not an official contest
template or legal interpretation. Authors remain responsible for checking the
current notice, division rules, data permissions, code execution, and the final
rendered files before submission.
