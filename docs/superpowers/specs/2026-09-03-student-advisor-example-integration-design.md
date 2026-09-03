# Student–Advisor Example Integration Design

## Goal

Extend `cumcm-paper-writing` from a standalone Codex skill into a documented,
testable skill repository with one complete reference implementation. The
reference implementation is the supplied student–advisor matching exercise and
must demonstrate the full path from public problem data to analysis, figures,
LaTeX source, verified PDF, and supporting materials.

The user explicitly authorized publishing `data1.xlsx`, `data2.xlsx`, and
`data3.xlsx` as public example data.

## Chosen approach

Use a single repository with two independent top-level concerns:

1. the installable skill remains at the repository root;
2. runnable demonstrations live below `examples/`.

This keeps installation compatible with the existing GitHub repository while
making the example discoverable and versioned with the workflow it exercises.
The case is a reference implementation, not part of the skill's always-loaded
context.

## Target layout

```text
cumcm-paper-writing/
├── SKILL.md
├── manifest.yaml
├── agents/
├── references/
├── static/
├── tests/                         # skill contract tests
├── examples/
│   └── student-advisor-matching/
│       ├── README.md
│       ├── requirements.txt
│       ├── preflight.md
│       ├── problem/
│       │   ├── problem.md
│       │   └── problem.pdf
│       ├── data/
│       │   └── public/
│       │       ├── data1.xlsx
│       │       ├── data2.xlsx
│       │       └── data3.xlsx
│       ├── src/
│       ├── tests/
│       ├── reports/
│       ├── docs/
│       ├── paper/
│       │   ├── paper.md
│       │   ├── paper.tex
│       │   ├── paper.pdf
│       │   ├── figures/
│       │   └── scripts/
│       └── support/
│           ├── AI工具使用详情.pdf
│           └── scripts/
└── .github/workflows/ci.yml
```

## Content mapping

Move or copy only reviewed artifacts from the existing case workspace:

- `题目.md` and `题目.pdf` become `problem/problem.md` and
  `problem/problem.pdf`;
- the three authorized workbooks go to `data/public/`;
- analysis and plotting programs go to `src/`;
- data, visualization, and LaTeX contract tests go to the case `tests/`;
- evidence, data-quality, chart-map, and modeling documents go to `docs/`;
- generated baseline results go to `reports/`;
- editable paper source, generated TeX/PDF, and figures go to `paper/`;
- paper build/verification programs go to `paper/scripts/`;
- AI-use PDF and its build/verification programs go to `support/` and
  `support/scripts/`.

Do not publish caches, rendered page PNGs, LaTeX auxiliary files, local planning
documents, the obsolete ReportLab builder, temporary archives, or local
absolute paths.

## Data and privacy boundary

The example may contain the supplied problem statement and three user-approved
public workbooks. Before staging, inspect workbook properties and values for
author names, organizations, comments, external links, hidden sheets, and
unexpected personal identifiers. Preserve the analytical values but clear
document metadata if it contains local identity.

Scan every staged text file, PDF metadata, archive member, and workbook property
for local account names, home paths, contestant identity, school identity,
tokens, and credentials. Run the scan against an explicit staged-file allowlist
rather than the full development workspace.

No repository-wide software license will be added without separate user
authorization. Third-party template code will not be copied into this repository
because the supplied local snapshot does not state a license. The example will
document the upstream CUMCMThesis URL and accept a user-provided template path.

## Reproducible path contract

The case must run from its own directory. Programs must resolve inputs relative
to the case root and default to `data/public/`; no source file may rely on the
former sibling folder `题目与公开数据` or any absolute path.

The LaTeX builder will discover the template in this order:

1. an explicit `--template-dir` argument;
2. `CUMCM_TEMPLATE_DIR`;
3. `third_party/CUMCMThesis` below the case directory, if the user placed it
   there.

Failure to find `cumcmthesis.cls` and the selected year style must produce a
clear actionable error. The builder must never silently fall back to the old
plain-text/ReportLab PDF path. Tests may generate `paper.tex` without compiling;
the published PDF must still be rebuilt and verified using the supplied local
template before upload.

## Documentation

The root README will explain:

- what the skill does and how to install/invoke it;
- the repository split between skill and examples;
- a direct link to the student–advisor example;
- the example's evidence boundary and the fact that it is an exercise, not an
  official contest solution;
- prerequisites for Python, XeLaTeX/CUMCMThesis, and Poppler.

The example README will provide one clean setup sequence for PowerShell and a
platform-neutral command summary. It will identify generated versus authored
files, explain the public-data authorization, state unsupported claims, and show
how to regenerate reports, figures, TeX, PDF, and verification output.

## Testing and CI

Add repository structure tests before migrating the case. They must fail while
the example layout is missing, then pass after integration. Tests will verify:

- required case directories and public files exist;
- source defaults point to `data/public/` and contain no local absolute path;
- the obsolete ReportLab builder and transient output are absent;
- LaTeX source preserves structured formulas and uses CUMCMThesis;
- the analysis and visualization regression suites pass;
- the final PDF verifier and AI-use verifier pass when their dependencies are
  available;
- documentation links resolve.

GitHub Actions will install Python dependencies and run the skill and case test
suites. It will not download or redistribute the third-party LaTeX template.
Compilation remains a documented local/release verification step unless a
licensed template dependency is later added.

## Release and upload

Implementation will use test-first migration, update the skill manifest version,
run the full local analysis/figure/LaTeX/PDF verification pipeline, inspect the
staged file list and repository size, and check `git diff --check`. Commit only
the reviewed allowlist, push `main`, then confirm the local and remote commit
hashes match.

## Acceptance criteria

- GitHub contains the installable skill and the complete, logically organized
  student–advisor example.
- The three public workbooks and problem statement are present in their declared
  locations.
- A fresh checkout can run analysis, figures, and tests without depending on a
  sibling data directory.
- LaTeX compilation works when the documented CUMCMThesis path is supplied.
- The tracked PDF matches the verified LaTeX source and contains no identity or
  formula-flattening defects.
- CI passes, the worktree is clean, and `origin/main` matches the local commit.
