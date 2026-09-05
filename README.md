# Mathematical Modeling Competition Paper Writing

A contest-aware paper workflow for CUMCM, MCM/ICM, other mathematical modeling
competitions and course exercises. The existing name `cumcm-paper-writing`
is retained for installation compatibility; version 0.5.0 introduces generic
profiles rather than universal CUMCM rules.

## Use

Install this directory under your agent's skills directory and invoke
`$cumcm-paper-writing`. Provide the contest, year, problem, data and any official
instructions. Unverified rules stay explicitly unresolved.

Example: “使用 $cumcm-paper-writing，按课程作业要求撰写论文，附录仅保留核心算法，完整代码单独交付。”

## Workflow

- [Contest profile](references/contest-profile.md): front matter, page-count scope,
  identity, disclosure, support files and code policy.
- [Problem coverage](references/problem-coverage.md): one status per requested output.
- [Model validation](references/model-validation.md): descriptive/predictive/
  optimization/simulation checks and evidence boundaries.
- [Artifact consistency](references/artifact-consistency.md): one authoritative
  manuscript, generated figures, code and reproducible build record.
- [Code appendix](references/code-appendix.md): full/core/none/unresolved policy;
  concise readable excerpts from tested source without losing complete code.

Historical CUMCM rules are research pointers requiring original-source checks.
No universal page limit, anonymity requirement or mandatory full-code appendix
is asserted for all contests. Templates are external prerequisites.

## Validation

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python scripts/build_pdf.py path/to/paper.tex --output path/to/paper.pdf
```

The compiler defaults to XeLaTeX; `--engine` selects another compatible executable.
Use `--template-dir` for a directory of template files. Build failures preserve
existing output. Bibliographies needing BibTeX/Biber require a separate documented
build workflow; this two-pass helper is not a complete bibliography orchestrator.
Visual/scientific checks remain separate from compilation tests.

## Layout and example

`SKILL.md` routes tasks; `manifest.yaml` maps references; `static/` holds common
and task/delivery guidance; `references/` holds focused rules; `scripts/` and
`tests/` hold executable tools and verification. CI runs metadata and unit checks.

The student-advisor case is maintained separately at
[student_advisor_case](https://github.com/Ouy5517/student_advisor_case).
Its reviewed limitations are recorded in the artifact-consistency reference.
This repository does not bundle its raw data or promise its paper is fully validated.
