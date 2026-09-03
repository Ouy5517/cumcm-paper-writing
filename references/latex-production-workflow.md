# LaTeX production workflow

Load this reference when the requested deliverable is a PDF, when mathematical
notation must remain typeset, or when a `CUMCMThesis`/`cumcmthesis` template is
available. This workflow turns verified paper content into a reproducible,
anonymous submission artifact; it is not a substitute for evidence validation.

## Inputs and outputs

Required inputs:

- verified prose, equations, tables, figures, citations, and appendix material;
- the current-year notice and any supplied template files;
- runnable analysis/figure code and an evidence ledger.

Required outputs:

- `paper.tex`, the authoritative typesetting source;
- `paper.pdf`, compiled from that source;
- complete source code, generated figures, reproduction commands, and any
  required AI-use detail PDF in an anonymous support archive;
- a verification record with build, page, visual, anonymity, and hash results.

## 1. Inspect and stage the template

Inspect the supplied README, example `.tex`, `cumcmthesis.cls`, year `.sty`, and
font/package assumptions. Copy reusable class/style files into the project or
set `TEXINPUTS` to their directory. Never copy sample prose, author data, QR
codes, advertisements, or demonstration figures.

Start an anonymous electronic paper with the template's supported equivalent of:

```tex
\documentclass[withoutpreface,bwprint]{cumcmthesis}
\usepackage{cumcm2026} % replace only when the selected year supplies another style
```

The official notice overrides template comments. Keep the template and build
inputs inside the project or record their exact external prerequisite.

## 2. Create real LaTeX, not formula-shaped text

Write inline mathematics as `$...$` and displayed mathematics in equation,
align, or `\[...\]` environments. Preserve commands, braces, subscripts,
superscripts, limits, fractions, and indicator notation. For example:

```tex
\[
n_{bk}=\sum_i \mathbf{1}\{r_i=k\},\qquad
p_{bk}=\frac{n_{bk}}{N_b^+}.
\]
```

The source must contain `n_{bk}=\sum_i` and `\frac{n_{bk}}{N_b^+}`, not
plain-text approximations. A converter that emits parenthesized underscore or
caret forms, or Unicode sigma in place of structured mathematics, has failed
the contract.

Convert prose programmatically only when the conversion preserves math blocks.
If Markdown is the editorial source, keep a deterministic conversion/build
script beside it and test representative formulas before converting the full
paper. Do not use ReportLab, Word text runs, or a Markdown renderer as a silent
fallback for mathematical typesetting when the requested output is LaTeX.

## 3. Build reproducibly

Compile in an isolated build directory so auxiliary files do not pollute the
submission tree. Run xelatex 两次 (two passes) so references, numbering, and
bookmarks settle; `latexmk -xelatex` is an acceptable equivalent.

Example PowerShell sequence:

```powershell
$build = Join-Path $PWD 'paper/tmp/latex'
New-Item -ItemType Directory -Force -Path $build | Out-Null
xelatex -interaction=nonstopmode -halt-on-error -output-directory=$build paper/paper.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=$build paper/paper.tex
Copy-Item -LiteralPath (Join-Path $build 'paper.pdf') -Destination 'paper/paper.pdf' -Force
```

On Windows, sanitize `PATH` before invoking MiKTeX if it contains entries that
are files rather than directories. Stop on a nonzero compiler exit, missing
font/glyph, undefined control sequence/reference, or absent output PDF. Do not
declare success from the existence of an older PDF.

## 4. Verify source and PDF

Run source checks before visual review:

```powershell
rg -n 'n_\(|\^\(|Missing character|Undefined control sequence|LaTeX Error' paper
pdfinfo paper/paper.pdf
pdftoppm -png -r 140 paper/paper.pdf paper/tmp/render/page
```

Interpret the first command contextually: code listings may contain literal
source syntax, but mathematical prose and generated LaTeX must not contain
flattened formula artifacts. Confirm A4 size, expected page count, blank author
metadata, and current-year size limits with `pdfinfo` or equivalent tools.

Inspect every rendered page, including the appendix. Check title/abstract page,
heading hierarchy, equation glyphs and numbering, table rules, figure labels,
page breaks, footer numbers, references, code wrapping, and blank/overflow pages.
Source compilation is not visual verification.

## 5. Verify anonymity and package consistency

Scan visible text, PDF metadata, TeX comments, code comments, filenames, and
archive paths for contestant names, schools, division details, account names,
home directories, and absolute local paths. Use an `anonymity` scan over the
exact files entering the archive, not the entire development workspace.

Build the support archive from an explicit allowlist. Include runnable code,
figures, `paper.tex`, the deterministic build script, reproduction instructions,
and required disclosure files. Exclude temporary render directories, caches,
private/unused data, editor files, and obsolete non-LaTeX PDF builders.

List archive members, rerun code/tests/verifiers, and compare paper values with
generated reports and figures. Record SHA256 for the final PDF and support
archive so the reviewed artifacts are identifiable.

## Completion contract

Return `ready` only when the exact final artifacts pass fresh compilation,
automated checks, every-page visual review, anonymity inspection, archive
inspection, and cross-file consistency checks. Otherwise return
`ready_with_author_checks` or `blocked` with the remaining checks named.
