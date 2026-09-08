# CUMCMThesis template contract

Load this reference when the author supplies `cumcmthesis.cls`, a year style
such as `cumcm2026.sty`, or an example project based on CUMCMThesis.

## Authority and safe reuse

Inspect the supplied README, class, year style, and example source. Reuse the
layout contract and reusable class/style files; do not reuse sample narrative,
advertising, QR codes, identity fields, example figures, or decorative boxes.
The selected year's inspected official notice defines binding CUMCM rules and
overrides conflicting template comments. The supplied template defines only
the layout behavior it actually contains; other advice is non-binding editorial
guidance.

For an anonymous electronic paper, the canonical class option is equivalent to:

    \documentclass[withoutpreface,bwprint]{cumcmthesis}

If LaTeX is requested, compile with the supplied template and XeLaTeX; when
dependencies are missing, preserve source and report the exact missing input.
For other delivery requests, a compatible math-capable renderer may be used,
with its identity and layout limitations recorded.

## Conditional template observations

Apply the following only when the supplied template contains the corresponding
behavior. They are not automatic CUMCM requirements.

| Element | Contract |
| --- | --- |
| Page | White A4; 2.5 cm on all four sides |
| Electronic first page | Centered paper title, centered bold `摘 要`, abstract, then `关键字` |
| Page numbering | Arabic numbers from abstract page 1; centered footer |
| Contents | No table of contents |
| Body | Chinese body approximately 12 pt with two-character paragraph indent and about 1.35-1.38 line spacing |
| Major heading | Centered, bold Heiti, approximately size 3 |
| Subheading | Left aligned, bold Heiti, approximately size 4 |
| Table | When the supplied template uses a three-line table, keep its caption above and avoid full cell grids unless the data structure requires them |
| Figure | Centered; caption below; automatic numbering and in-text reference |
| Formula | Use real mathematical typesetting when available; number and reference formulas used later |
| Color | `bwprint`-safe; distinctions must remain understandable in grayscale |
| Metadata | Empty author and no contestant/school/division identifiers |

## Figure and table evidence

- A figure caption states the metric, denominator/sample scope, and source or
  derivation. Observations use filled marks or solid lines; fitted/scenario
  values use open marks or dashed lines plus an explicit caption note.
- When required by the supplied template, a three-line table keeps only top,
  header-separator, and bottom rules. Align decimals and units; avoid shrinking
  text to fit an oversized table.
- Do not combine four independent tables into a 2-by-2 panel merely to save
  space. Normally keep no more than two tables together, then resume the
  explanation before presenting further tabular evidence.
- Use a figure when the intended reading task is a trend or comparison; use a
  table when readers need exact values. Do not duplicate the same evidence in
  both forms without a specific analytical reason.
- Refer to every retained figure and table in the body and state the takeaway
  without repeating all values shown.

## 2026 AI-use placement

When the supplied entry package contains the 2026 AI-use rule, put one truthful
statement immediately before references. If AI was used, include the anonymous
`AI工具使用详情.pdf` in supporting materials and list it in the appendix.

## Fallback disclosure

For a permitted alternative renderer, record its identity and verify geometry,
abstract page, headings, tables, captions, page numbering and math visually.
An alternative renderer does not satisfy an explicit LaTeX delivery request.
