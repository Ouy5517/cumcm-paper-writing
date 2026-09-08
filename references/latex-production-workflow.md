# LaTeX production workflow

Load this reference when the requested deliverable is a PDF, when mathematical
notation must remain typeset, or when a `CUMCMThesis`/`cumcmthesis` template is
available. This workflow turns verified paper content into a reproducible,
anonymous submission artifact; it is not a substitute for evidence validation.

Resolve the selected year and inspect its official notice first. The CUMCM
class/style example below applies only to a matching supplied template. Other
templates may use article, ctexart, or supplied classes. Identity policy, front
matter, and supporting-file requirements come from that inspected authority.
Code selection follows code-appendix.md; complete code stays in the
engineering project even when omitted from the paper.

## Inputs and outputs

Required inputs:

- verified prose, equations, tables, figures, citations, and appendix material;
- the selected-year official notice and any supplied template files;
- runnable analysis/figure code and an evidence ledger.

Required outputs:

- `paper.tex`, the authoritative typesetting source;
- `paper.pdf`, compiled from that source;
- complete source code, generated figures, reproduction commands, and any
  required disclosure files in the form permitted by the selected-year verified
  CUMCM official notice and submission package;
- a verification record with build, page, visual, anonymity, and package results.

## 1. Inspect and stage the template

Inspect the supplied README, example `.tex`, `cumcmthesis.cls`, year `.sty`, and
font/package assumptions. Copy reusable class/style files into the project or
set `TEXINPUTS` to their directory. Never copy sample prose, author data, QR
codes, advertisements, or demonstration figures.

Start an anonymous electronic paper with the template's supported equivalent of:

```tex
\documentclass[withoutpreface,bwprint]{cumcmthesis}
\usepackage{cumcm2026} % only when the inspected supplied template uses this style
```

Include `cumcm2026` only when the inspected supplied template actually uses
`cumcm2026`; otherwise select the template's supplied year style or omit the
year style. The official notice overrides template comments. Keep the template and build
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

The equation above is an example, not required paper content. Preserve each
input equation's meaning and mathematical structure. A converter that emits parenthesized underscore or
caret forms, or Unicode sigma in place of structured mathematics, has failed
the contract.

Convert prose programmatically only when the conversion preserves math blocks.
If Markdown is the editorial source, keep a deterministic conversion/build
script beside it and test representative formulas before converting the full
paper. Do not use ReportLab, Word text runs, or a Markdown renderer as a silent
fallback for mathematical typesetting when the requested output is LaTeX.

Load environment-readiness.md before compiling. Verify the requested engine
and template first; if either is unavailable, stop with `blocked` and preserve
the source. Never use an older PDF or a different renderer as evidence of a
fresh LaTeX build.

## 3. Build reproducibly

Compile in an isolated build directory so auxiliary files do not pollute the
submission tree. Run xelatex 两次 (two passes) so references, numbering, and
bookmarks settle; `latexmk -xelatex` is an acceptable equivalent.

Use the bundled compiler from the skill directory (source assets resolve from
the TeX source's parent directory):

```powershell
python scripts/build_pdf.py paper/paper.tex --output paper/paper.pdf --template-dir "$env:CUMCM_TEMPLATE_DIR"
```

On Windows, sanitize `PATH` before invoking MiKTeX if it contains entries that
are files rather than directories. Stop on a nonzero compiler exit, missing
font/glyph, undefined control sequence/reference, or absent output PDF. Do not
declare success from the existence of an older PDF.

The compiler uses a fresh temporary directory, checks both exit codes and the
final log, and atomically replaces the destination only after success. Failed
builds preserve an existing PDF but never report it as current. This is a build
gate only; PDF structure, mathematical meaning and visual QA are separate.
Compile only inspected/trusted TeX; disabling shell escape is not a sandbox.

## 4. Verify source and PDF

Run source checks before visual review:

```powershell
rg -n 'n_\(|\^\(|Missing character|Undefined control sequence|LaTeX Error' paper
pdfinfo paper/paper.pdf
New-Item -ItemType Directory -Force paper/tmp/render | Out-Null
pdftoppm -png -r 140 paper/paper.pdf paper/tmp/render/page
```

Interpret the first command contextually: code listings may contain literal
source syntax, but mathematical prose and generated LaTeX must not contain
flattened formula artifacts. Confirm A4 size, expected page count, blank author
metadata, and selected-year verified size limits with `pdfinfo` or equivalent tools.

Inspect every rendered page, including the appendix. Check title/abstract page,
heading hierarchy, equation glyphs and numbering, table rules, figure labels,
page breaks, footer numbers, references, code wrapping, and blank/overflow pages.
Source compilation is not visual verification.

When an observed layout/typesetting issue involves table walls, sparse pages,
stranded headings, floats, or overflow, load layout-diagnosis.md. Follow its
compile-to-render diagnostic order and choose only a template-supported remedy
for the observed failure.

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
generated reports and figures. Record the final filenames and build revision so
the reviewed artifacts are identifiable without a separate hash-validation step.

## Completion contract

Return `ready` only when the exact final artifacts pass fresh compilation,
automated checks, every-page visual review, anonymity inspection, archive
inspection, and cross-file consistency checks. Otherwise return
`ready_with_author_checks` or `blocked` with the remaining checks named.
