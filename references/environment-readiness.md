# CUMCM environment readiness

Use this reference for LaTeX engine, template, render, PDF, or submission
preflight questions. It describes toolchain readiness; it does not replace the
selected-year official CUMCM notice, supplied template/package, or scientific
validation.

## Status contract

- `ready`: a fresh build produced the intended PDF, the log and PDF structure
  checks passed, every page was visually reviewed, anonymity and package checks
  passed, and the selected-year authority was inspected.
- `ready_with_author_checks`: the build and technical checks are usable, but an
  author-owned item such as the selected-year notice, identity fields,
  disclosure wording, page rule, or support-file allowlist remains unresolved.
- `blocked`: XeLaTeX or the requested engine, the supplied template, the source,
  required evidence, or a build gate is unavailable or failed.

## Hard limitations

1. Resolve the selected-year official authority before enforcing page,
   anonymity, disclosure, file-size, date, or support-package rules. The
   current calendar year must not select a CUMCM rule set.
2. Check the requested engine before rendering. If XeLaTeX is missing, report
   `blocked` with the platform-specific installation command and preserve the
   source; do not silently switch to ReportLab, Word, Markdown, or another
   renderer.
3. A missing template or year style is an author input gap, not permission to
   invent a class, page limit, declaration, or layout rule.
4. A failed build, an absent PDF, or an older PDF left in place is `blocked`.
   Source compilation alone cannot claim visual pass, table-flow pass,
   overflow pass, font pass, or submission readiness; those checks are
   `UNVERIFIED` until a fresh PDF is rendered and inspected.
5. A synthetic fixture proves only that the local toolchain can compile a small
   document. It is not scientific validity, model validation, CUMCM compliance,
   or evidence that a real paper's tables, formulas, fonts, or page count pass.
6. The skill cannot certify plagiarism/AIGC-detector outcomes, promise an
   acceptance result, or recommend evasion. Preserve required disclosures and
   author review.

## Windows XeLaTeX preflight

Run `xelatex --version` (or the explicitly requested engine) and record the
resolved executable. On Windows, the builder ignores only PATH entries whose
directory inspection raises `OSError`/`ValueError`; this does not hide a missing
compiler. Install MiKTeX from its official source, for example:

```powershell
winget install --id MiKTeX.MiKTeX --exact --silent `
  --accept-source-agreements --accept-package-agreements
```

Open a new shell after installation, rerun the version check, and compile the
declared TeX source through `scripts/build_pdf.py`. Do not call a build passed
because an older PDF exists.

## Evidence record

Record engine/version, source and template paths, build command, exit status,
log warnings/errors, PDF path and timestamp, page/render checks, anonymity
scan, package allowlist, and unresolved author checks. Ordinary verification
does not require SHA256 or MD5; record a hash only when the inspected
selected-year rule explicitly requires one.
