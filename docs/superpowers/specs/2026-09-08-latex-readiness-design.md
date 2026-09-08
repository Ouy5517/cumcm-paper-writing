# CUMCM LaTeX Readiness and Windows Build Design

## Objective

Make the CUMCM paper-writing skill explicit about environment limitations and
make its PDF builder reliable on Windows machines whose `PATH` contains a
directory that cannot be inspected. Install a real XeLaTeX engine (MiKTeX) on
the current computer, then verify a fresh PDF build end to end.

## Confirmed decisions

- Use MiKTeX as the Windows LaTeX distribution; install it with the existing
  `winget` package manager when available.
- Keep XeLaTeX as the default engine. A missing engine is a blocking rendering
  condition with an actionable installation message; it must never trigger a
  silent switch to ReportLab, Word, Markdown, or another renderer.
- Sanitize `PATH` entry-by-entry. A `PermissionError`, other `OSError`, or
  invalid path value while checking one entry is treated as an unusable entry,
  not as a failure of the whole build. The compiler lookup still fails clearly
  when no usable engine remains.
- Preserve the builder's two-pass compilation, `-no-shell-escape`, temporary
  build directory, log gate, PDF signature check, and atomic replacement of a
  previous PDF only after success.
- Add a CUMCM environment-readiness reference that separates `ready`,
  `ready_with_author_checks`, and `blocked`, and states exactly which claims
  require a real PDF and inspected selected-year authority.
- Keep ordinary artifact hashes out of the workflow. A hash may appear only
  when an inspected selected-year submission rule explicitly requires it.

## Scope

### In scope

1. A small Windows-safe PATH filtering helper and regression tests for an
   inaccessible entry.
2. Contract documentation and tests for missing-engine, missing-template,
   missing-authority, no-PDF, and synthetic-fixture limitations.
3. MiKTeX installation and a real XeLaTeX integration build on this computer.
4. Synchronization of the validated source skill into both local installed
   skill locations.

### Out of scope

- Changing CUMCM year-specific rules without inspecting that year's official
  notice or package.
- Adding a new runtime dependency, a silent renderer fallback, or a service
  that claims to detect AI-generated text or plagiarism.
- Importing Nature word counts, display-item quotas, figure rules, or journal
  submission policy.
- Requiring a hash for routine source, PDF, or support-package verification.

## Architecture and interfaces

### PDF builder

`scripts/build_pdf.py` retains `build(source, output, template=None,
engine='xelatex') -> Path`. It delegates PATH cleanup to a private helper that
returns a string suitable for `shutil.which`. The helper catches only path
inspection failures (`OSError` and `ValueError`) and preserves usable entries
in their original order.

### Skill readiness contract

`references/environment-readiness.md` is routed on demand for render,
preflight, template, or engine questions. It defines:

- `ready`: fresh compilation, PDF inspection, visual review, anonymity, and
  package checks all have evidence;
- `ready_with_author_checks`: the build is usable but selected-year authority,
  author fields, or another author-owned check is still unresolved;
- `blocked`: the engine, template, source, or required evidence is unavailable
  or the build gate failed.

The reference also states that a synthetic fixture demonstrates the toolchain,
not scientific validity or competition compliance; no visual pass may be
claimed from TeX source alone; and the current calendar year may not be used as
the selected CUMCM rule set.

### Integration verification

The source repository gets an engine-aware integration test that skips with an
explicit reason when `xelatex` is absent, and passes on this computer after
MiKTeX installation. The test compiles a minimal TeX document through the real
builder, checks the PDF signature and two compiler passes, and leaves no build
directory behind.

## Acceptance criteria

- A `PermissionError` raised while inspecting one Windows `PATH` entry does not
  abort an otherwise valid build.
- Existing PDF-builder tests and the new PATH regression test pass.
- The readiness reference is reachable from `manifest.yaml` and all limitation
  contract tests pass.
- `xelatex --version` resolves to the installed MiKTeX distribution.
- A fresh minimal document builds to a valid PDF with two XeLaTeX passes.
- The existing PDF is preserved after every failed build path.
- Both local installed copies contain the same validated files and version as
  the source skill.
- Full unit tests, structural validation, and `git diff --check` pass.
