# Natural Table Flow and Emphasis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add enforceable guidance for natural table placement and restrained bold emphasis while removing mandatory artifact hash checks.

**Architecture:** Keep concise routing rules in `SKILL.md`, detailed editorial rules in the paper-structure and CUMCMThesis references, and artifact verification policy in the existing production references. Extend the lightweight unittest contract so future edits cannot silently remove the new behavior.

**Tech Stack:** Markdown skill documentation, Python standard-library `unittest`.

## Global Constraints

- Do not create a 2-by-2 montage from four independent tables.
- Normally place no more than two tables consecutively and connect table groups with interpretation.
- Bold only short, decision-relevant conclusions, indicators, model definitions, risks, or boundaries.
- Do not require SHA256 or source hashes for normal paper production and packaging.
- Preserve compilation, visual, anonymity, archive, and cross-file consistency checks.

---

### Task 1: Lock the editorial and verification contracts

**Files:**
- Create: `tests/test_editorial_style_contract.py`
- Modify: `tests/test_latex_workflow_contract.py`
- Test: `tests/test_editorial_style_contract.py`
- Test: `tests/test_latex_workflow_contract.py`

**Interfaces:**
- Consumes: UTF-8 Markdown files at repository-relative paths.
- Produces: unittest assertions for table-flow, emphasis, and no-mandatory-hash policy.

- [ ] **Step 1: Write failing tests**

Create tests that assert the skill and layout references explicitly prohibit a
four-table montage/table wall, limit ordinary consecutive tables to two, require
interpretive prose, define restrained bolding, and contain no mandatory
`SHA256`/`source hash` artifact checks.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests.test_editorial_style_contract tests.test_latex_workflow_contract -v`

Expected: FAIL because the new editorial rules are absent and the LaTeX workflow still requires SHA256.

- [ ] **Step 3: Commit the failing contract tests**

Run: `git add tests/test_editorial_style_contract.py tests/test_latex_workflow_contract.py && git commit -m "test: define natural paper layout contract"`

### Task 2: Implement natural layout and emphasis guidance

**Files:**
- Modify: `SKILL.md`
- Modify: `references/paper-structure.md`
- Modify: `references/cumcmthesis-template.md`

**Interfaces:**
- Consumes: the contract tests from Task 1.
- Produces: concise routing guidance plus detailed table-flow and bold-emphasis rules.

- [ ] **Step 1: Add the minimal rules**

Add explicit prose implementing every layout and emphasis constraint from the
design without adding a formatter or subjective style-scoring machinery.

- [ ] **Step 2: Run the editorial contract test**

Run: `python -m unittest tests.test_editorial_style_contract -v`

Expected: PASS.

- [ ] **Step 3: Commit the editorial guidance**

Run: `git add SKILL.md references/paper-structure.md references/cumcmthesis-template.md && git commit -m "feat: guide natural table flow and emphasis"`

### Task 3: Remove mandatory artifact hash checks

**Files:**
- Modify: `references/artifact-consistency.md`
- Modify: `references/code-appendix.md`
- Modify: `references/latex-production-workflow.md`
- Modify: `tests/test_latex_workflow_contract.py`

**Interfaces:**
- Consumes: existing build and package verification workflow.
- Produces: verification based on reproducible commands and substantive checks, without mandatory artifact hashes.

- [ ] **Step 1: Remove hash requirements**

Delete mandatory input, source, PDF, support-archive, and code-excerpt hash
recording. Keep code revision, dependencies, commands, compilation, visual,
anonymity, archive-member, and cross-file checks.

- [ ] **Step 2: Run focused tests**

Run: `python -m unittest tests.test_latex_workflow_contract tests.test_editorial_style_contract -v`

Expected: PASS.

- [ ] **Step 3: Run full validation**

Run: `python scripts/validate_skill.py`

Expected: `Skill metadata and routes: PASS`.

Run: `python -m unittest discover -s tests -v`

Expected: all tests pass.

- [ ] **Step 4: Commit the verification simplification**

Run: `git add references/artifact-consistency.md references/code-appendix.md references/latex-production-workflow.md tests/test_latex_workflow_contract.py && git commit -m "refactor: drop mandatory artifact hash checks"`
