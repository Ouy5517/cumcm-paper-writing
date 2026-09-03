# Submission preflight

Run these checks on the selected year and record PASS, FAIL, or AUTHOR CHECK.

## Content and structure

- One abstract-only page with title, abstract, and keywords.
- Problem restatement, assumptions, notation, model, solution, results,
  validation/sensitivity, conclusions/limitations, references, and appendix
  are present as needed.
- The body page limit comes from the selected year's official rule; do not
  import a 2019/2025 limit into 2026.
- No table of contents and no unsupported claim in the abstract or conclusion.
- Figures and tables are numbered, referenced in prose, legible at final scale,
  and label observations, fits, extrapolations, units, denominators, and scope.
- If a supplied template controls presentation, major headings, subheadings,
  abstract label, keywords, three-line tables, and captions match its contract.
- LaTeX source retains structured mathematics (`\sum`, `\frac`, subscripts,
  superscripts, braces); generated prose contains no `_()`/`^()` artifacts.

## Physical package

- White A4; all margins >=2.5 cm; left binding.
- Physical page 1 is the official consent letter and page 2 the official
  numbering page; body starts on physical page 4.
- Arabic footer numbering starts at 1 on the abstract page and is centered.
- Appendix is printed and bound with the body.

## Electronic package

- One uncompressed anonymous PDF/Word paper, preferably PDF, within the
  selected size limit; it starts with the abstract and excludes the physical
  consent and numbering pages.
- Appendix is included in the paper. The file list names every support item.
- One anonymous ZIP/RAR support archive, when applicable, contains runnable
  code, permitted author-consulted data, and substantial intermediate outputs.
- No identity in visible text, metadata, filenames, archive paths, comments, or
  code comments where practical.

## Reproducibility and references

- Every used program is complete and runnable, including Excel/SPSS commands
  when applicable; otherwise insert the exact no-program statement.
- Paper values match code, tables, figures, appendix, and archive.
- Every external/public source is cited in text and in the reference list.
- Current-year entry and AI-use notices are checked separately.
- The AI-use statement precedes references and agrees with the anonymous detail
  PDF in supporting materials when the selected rule requires it.
- The exact final TeX compiles twice without missing glyphs, undefined controls,
  unresolved references, or stale-output substitution; every PDF page is rendered
  to an image and visually inspected.
- Final PDF and support archive are produced from explicit inputs, their members
  are inspected, and SHA256 hashes identify the reviewed artifacts.

## Status rule

- ready: all checks pass and no author verification remains.
- ready_with_author_checks: structure is sound, but author must verify a team
  field, official notice, citation, code run, rendered layout, or size.
- blocked: a missing problem statement, result, or essential input prevents a
  meaningful draft or audit.
