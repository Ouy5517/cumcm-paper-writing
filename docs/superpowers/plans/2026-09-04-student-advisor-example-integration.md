# Student–Advisor Example Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete, portable student–advisor matching example to the `cumcm-paper-writing` repository and publish the verified result to GitHub.

**Architecture:** Keep the installable skill at the repository root and place the independent reference implementation under `examples/student-advisor-matching/`. The example owns its public data, analysis, tests, paper, and support artifacts; CUMCMThesis remains an external dependency selected by argument, environment variable, or an untracked `third_party` directory.

**Tech Stack:** Python 3.12, pandas, NumPy, SciPy, Matplotlib, openpyxl, pytest, XeLaTeX/MiKTeX, CUMCMThesis, Poppler, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-03-student-advisor-example-integration-design.md`

## Global Constraints

- Publish `data1.xlsx`, `data2.xlsx`, and `data3.xlsx` only under `examples/student-advisor-matching/data/public/`.
- Do not publish caches, LaTeX auxiliary files, rendered QA pages, internal plans from the case workspace, the obsolete ReportLab builder, or local absolute paths.
- Do not vendor CUMCMThesis files because the supplied snapshot states no license; document the upstream URL and accept a template directory.
- Preserve the verified paper's structured LaTeX formulas, generated figures, anonymous PDF, and AI-use detail PDF.
- Add no repository-wide software license without separate user authorization.
- Use test-first migration and verify the exact staged allowlist before pushing `main`.

---

### Task 1: Define the repository example contract

**Files:**
- Create: `tests/test_example_repository_contract.py`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: the target layout in the design specification.
- Produces: `EXAMPLE_ROOT`, required-file assertions, path/privacy assertions, and ignore rules used to gate all later tasks.

- [ ] **Step 1: Write the failing structure test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = ROOT / "examples" / "student-advisor-matching"


def test_example_has_public_problem_data_and_reproducible_outputs():
    required = [
        "README.md", "requirements.txt", "preflight.md",
        "problem/problem.md", "problem/problem.pdf",
        "data/public/data1.xlsx", "data/public/data2.xlsx",
        "data/public/data3.xlsx", "src/analyze_public_data.py",
        "src/plot_public_data.py", "paper/paper.tex", "paper/paper.pdf",
    ]
    assert all((EXAMPLE_ROOT / path).is_file() for path in required)
```

- [ ] **Step 2: Run the test and confirm RED**

Run: `pytest tests/test_example_repository_contract.py -v`

Expected: FAIL because `examples/student-advisor-matching/` does not exist.

- [ ] **Step 3: Extend `.gitignore` for generated case artifacts**

Add rules for `.pytest_cache/`, `**/__pycache__/`, `**/tmp/`, LaTeX auxiliary
extensions, and `examples/student-advisor-matching/third_party/`, while leaving
the reviewed `paper.pdf` and support PDF trackable.

- [ ] **Step 4: Keep the test red until the case is staged**

Run: `pytest tests/test_example_repository_contract.py -v`

Expected: FAIL for the same missing-layout reason, not a test syntax error.

- [ ] **Step 5: Commit the contract**

```powershell
git add .gitignore tests/test_example_repository_contract.py
git commit -m "test: define example repository contract"
```

### Task 2: Stage authorized problem and public data

**Files:**
- Create: `examples/student-advisor-matching/problem/problem.md`
- Create: `examples/student-advisor-matching/problem/problem.pdf`
- Create: `examples/student-advisor-matching/data/public/data1.xlsx`
- Create: `examples/student-advisor-matching/data/public/data2.xlsx`
- Create: `examples/student-advisor-matching/data/public/data3.xlsx`
- Modify: `tests/test_example_repository_contract.py`

**Interfaces:**
- Consumes: user-authorized files from the local `题目与公开数据` directory.
- Produces: immutable example inputs at `problem/` and `data/public/`.

- [ ] **Step 1: Add workbook and PDF metadata assertions**

Use `openpyxl.load_workbook()` and `pypdf.PdfReader()` to assert that staged
inputs contain the expected sheet/header structure and do not expose a creator,
last-modified-by value, local account, or absolute path.

- [ ] **Step 2: Run the test and confirm RED**

Run: `pytest tests/test_example_repository_contract.py -v`

Expected: FAIL because the public files have not been staged or metadata has not
yet been normalized.

- [ ] **Step 3: Copy the five authorized inputs and normalize metadata if needed**

Use explicit file paths. For workbooks, preserve cell values and styles while
clearing `creator`, `lastModifiedBy`, `company`, and external links if present.
For the problem PDF, preserve visible content and clear identity metadata only
if inspection finds it.

- [ ] **Step 4: Run the metadata test and inspect workbook values**

Run: `pytest tests/test_example_repository_contract.py -v`

Expected: metadata assertions PASS; the overall structure test may remain red
until later case files exist.

- [ ] **Step 5: Commit public inputs**

```powershell
git add examples/student-advisor-matching/problem examples/student-advisor-matching/data tests/test_example_repository_contract.py
git commit -m "data: add public student-advisor example inputs"
```

### Task 3: Migrate portable analysis and visualization code

**Files:**
- Create: `examples/student-advisor-matching/src/analyze_public_data.py`
- Create: `examples/student-advisor-matching/src/plot_public_data.py`
- Create: `examples/student-advisor-matching/tests/test_public_analysis.py`
- Create: `examples/student-advisor-matching/tests/test_visualizations.py`
- Create: `examples/student-advisor-matching/requirements.txt`
- Create: `examples/student-advisor-matching/reports/public-baseline.md`
- Create: `examples/student-advisor-matching/paper/figures/*.png`
- Modify: `tests/test_example_repository_contract.py`

**Interfaces:**
- Consumes: `EXAMPLE_ROOT/data/public/data1.xlsx` through `data3.xlsx`.
- Produces: `analyze_batch`, `fit_saturating_curve`, generated report text,
  `generate_figures`, three PNGs, and passing case regression tests.

- [ ] **Step 1: Add a failing portability assertion**

Assert that both scripts resolve `project_root / "data" / "public"`, accept
`--data-dir`, and contain neither the former sibling data-directory name nor a
Windows home path.

- [ ] **Step 2: Run the root contract test and confirm RED**

Run: `pytest tests/test_example_repository_contract.py -v`

Expected: FAIL because portable scripts are absent.

- [ ] **Step 3: Copy and minimally adapt the verified scripts and tests**

Change only root/path calculation and imports required by the new layout. Keep
the verified definitions, evidence boundaries, chart values, and grayscale-safe
visual distinctions unchanged.

- [ ] **Step 4: Regenerate report and figures from in-repository data**

```powershell
cd examples/student-advisor-matching
python src/analyze_public_data.py
python src/plot_public_data.py
pytest -q
```

Expected: the report and three figures are regenerated; all migrated tests pass.

- [ ] **Step 5: Run root and case tests**

Run from repository root:

```powershell
pytest tests -q
pytest examples/student-advisor-matching/tests -q
```

Expected: analysis/visualization tests PASS; only paper-layout requirements may
remain incomplete.

- [ ] **Step 6: Commit analysis assets**

```powershell
git add examples/student-advisor-matching/src examples/student-advisor-matching/tests examples/student-advisor-matching/requirements.txt examples/student-advisor-matching/reports examples/student-advisor-matching/paper/figures tests/test_example_repository_contract.py
git commit -m "feat: add reproducible student-advisor analysis"
```

### Task 4: Migrate the LaTeX paper and support artifacts

**Files:**
- Create: `examples/student-advisor-matching/paper/paper.md`
- Create: `examples/student-advisor-matching/paper/paper.tex`
- Create: `examples/student-advisor-matching/paper/paper.pdf`
- Create: `examples/student-advisor-matching/paper/README.md`
- Create: `examples/student-advisor-matching/paper/scripts/build_latex_pdf.py`
- Create: `examples/student-advisor-matching/paper/scripts/verify_pdf.py`
- Create: `examples/student-advisor-matching/tests/test_latex_pdf.py`
- Create: `examples/student-advisor-matching/support/AI工具使用详情.pdf`
- Create: `examples/student-advisor-matching/support/scripts/build_ai_usage_pdf.py`
- Create: `examples/student-advisor-matching/support/scripts/verify_ai_usage.py`
- Modify: `tests/test_example_repository_contract.py`

**Interfaces:**
- Consumes: paper Markdown, case figures, CUMCMThesis class/style selected by
  `--template-dir`, `CUMCM_TEMPLATE_DIR`, or local `third_party/CUMCMThesis`.
- Produces: `resolve_template_dir(explicit: Path | None) -> Path`,
  `build_source(markdown: str) -> str`, `paper.tex`, verified `paper.pdf`, and
  verified AI-use detail PDF.

- [ ] **Step 1: Add failing tests for template discovery and paper structure**

Test all three discovery modes and a clear `FileNotFoundError` when no template
exists. Assert generated TeX uses
`\\documentclass[withoutpreface,bwprint]{cumcmthesis}`, contains structured
`\\sum`/`\\frac` formulas, and contains no local absolute path.

- [ ] **Step 2: Run the new paper tests and confirm RED**

Run: `pytest examples/student-advisor-matching/tests/test_latex_pdf.py -v`

Expected: FAIL because the migrated builder and sources are absent.

- [ ] **Step 3: Migrate source and refactor template resolution**

Move build and verification programs under `paper/scripts/`. Update path math
for the deeper directory, expose the interfaces above, add `--template-dir`,
and remove the old hard-coded CUMCMThesis location. Do not copy `build_pdf.py`.

- [ ] **Step 4: Migrate and normalize support scripts**

Update paths for `support/scripts/`, preserve anonymous PDF generation, and
ensure the verifier reads the sibling support PDF without a local path.

- [ ] **Step 5: Rebuild the exact tracked PDFs**

```powershell
cd examples/student-advisor-matching
python paper/scripts/build_latex_pdf.py --template-dir $env:CUMCM_TEMPLATE_DIR
python paper/scripts/verify_pdf.py
python support/scripts/build_ai_usage_pdf.py
python support/scripts/verify_ai_usage.py
```

Expected: 27-page A4 anonymous paper with three figures; one-page anonymous
AI-use detail PDF; all verifiers PASS.

- [ ] **Step 6: Run formula and path scans**

Search the exact case allowlist for flattened formulas, local home paths,
identity fields, missing glyphs, LaTeX errors, and obsolete ReportLab references.
Expected: no actionable match.

- [ ] **Step 7: Commit paper and support artifacts**

```powershell
git add examples/student-advisor-matching/paper examples/student-advisor-matching/support examples/student-advisor-matching/tests/test_latex_pdf.py tests/test_example_repository_contract.py
git commit -m "docs: add verified CUMCM LaTeX example paper"
```

### Task 5: Add example and repository documentation

**Files:**
- Create: `examples/student-advisor-matching/README.md`
- Create: `examples/student-advisor-matching/preflight.md`
- Create: `examples/student-advisor-matching/docs/chart-map.md`
- Create: `examples/student-advisor-matching/docs/claim-evidence-ledger.md`
- Create: `examples/student-advisor-matching/docs/data-quality.md`
- Create: `examples/student-advisor-matching/docs/modeling-plan.md`
- Create: `examples/student-advisor-matching/third_party/README.md`
- Modify: `README.md`
- Modify: `manifest.yaml`
- Modify: `tests/test_example_repository_contract.py`

**Interfaces:**
- Consumes: final case layout and commands from Tasks 2–4.
- Produces: discoverable root/example documentation, external-template setup,
  version `0.5.0`, and documentation-link checks.

- [ ] **Step 1: Add failing documentation-link tests**

Extract repository-relative Markdown links from the two README files and assert
that every non-URL target exists. Assert the root README links directly to the
example and the example README names the public-data and evidence boundaries.

- [ ] **Step 2: Run the contract test and confirm RED**

Run: `pytest tests/test_example_repository_contract.py -v`

Expected: FAIL because the documentation and links are absent.

- [ ] **Step 3: Migrate case documents without internal plans**

Copy only the four public-facing analytical documents and preflight checklist.
Rewrite commands and paths for the integrated layout. Do not copy the case
workspace's `docs/superpowers/plans/` directory.

- [ ] **Step 4: Write root and example README navigation**

Document authored/generated files, reproducible commands, CUMCMThesis setup,
data authorization, claim boundaries, and expected artifacts. Add a direct
example link to the root README and increment `manifest.yaml` to `0.5.0`.

- [ ] **Step 5: Run link and content tests**

Run: `pytest tests/test_example_repository_contract.py -v`

Expected: all repository contract tests PASS.

- [ ] **Step 6: Commit documentation**

```powershell
git add README.md manifest.yaml examples/student-advisor-matching/README.md examples/student-advisor-matching/preflight.md examples/student-advisor-matching/docs examples/student-advisor-matching/third_party tests/test_example_repository_contract.py
git commit -m "docs: organize complete student-advisor example"
```

### Task 6: Add continuous integration and final release verification

**Files:**
- Create: `.github/workflows/ci.yml`
- Modify: `tests/test_example_repository_contract.py`

**Interfaces:**
- Consumes: Python requirements and both test suites.
- Produces: GitHub Actions checks for skill contracts, case analysis, figures,
  source-generation tests, repository layout, and path/privacy invariants.

- [ ] **Step 1: Add a failing CI contract assertion**

Assert `.github/workflows/ci.yml` exists, uses `actions/checkout`, installs both
root/case requirements as applicable, and runs both root and case tests.

- [ ] **Step 2: Run the contract test and confirm RED**

Run: `pytest tests/test_example_repository_contract.py -v`

Expected: FAIL because CI is absent.

- [ ] **Step 3: Add the minimal GitHub Actions workflow**

Use Ubuntu and Python 3.12. Install
`examples/student-advisor-matching/requirements.txt`, run both pytest targets,
and regenerate the report/figures. Do not install or redistribute CUMCMThesis;
source-only LaTeX tests must remain independent of the template compiler.

- [ ] **Step 4: Run complete local verification**

```powershell
python -m unittest discover -s tests -v
pytest tests -q
pytest examples/student-advisor-matching/tests -q
python examples/student-advisor-matching/src/analyze_public_data.py
python examples/student-advisor-matching/src/plot_public_data.py
python examples/student-advisor-matching/paper/scripts/verify_pdf.py
python examples/student-advisor-matching/support/scripts/verify_ai_usage.py
python "$env:USERPROFILE/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .
git diff --check
```

Expected: every command exits 0.

- [ ] **Step 5: Inspect release contents**

Review `git status --short`, staged files, file sizes, workbook/PDF metadata,
case text scans, and `git diff --stat`. Confirm no caches, temp files, local
plans, template code, or obsolete builder is tracked. Record SHA256 for both
tracked PDFs and the three public workbooks.

- [ ] **Step 6: Commit and push**

```powershell
git add .github/workflows/ci.yml tests/test_example_repository_contract.py
git commit -m "ci: validate skill and reference example"
git push origin main
```

- [ ] **Step 7: Verify the remote**

Compare `git rev-parse HEAD` with `git ls-remote origin refs/heads/main`, confirm
the worktree is clean, and report the GitHub URL, commit hash, test counts, and
key example paths.
