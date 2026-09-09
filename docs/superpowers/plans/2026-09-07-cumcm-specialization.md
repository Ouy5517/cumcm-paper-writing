# CUMCM-Specialized Skill Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `cumcm-paper-writing` into a Chinese, CUMCM-only skill with section- and model-family-aware routing, compact core guidance, targeted academic-writing normalization, and complete contract tests.

**Architecture:** Keep `SKILL.md` as a concise router backed by `manifest.yaml`. Put universal CUMCM behavior in a five-file always-loaded core, section/model-specific behavior in focused fragments, and heavier result-allocation, consistency, layout, and submission procedures in on-demand references. Preserve the existing PDF builder and substantive verification gates while removing generic contest routes and mandatory artifact hashes.

**Tech Stack:** Markdown, YAML, Python 3 standard-library `unittest`, existing PyYAML development dependency.

## Global Constraints

- The skill supports CUMCM only; no active route or public description may claim MCM/ICM, course-paper, or generic-contest support.
- Chinese is the default manuscript language; canonical English method names, mathematics, variables, units, and citations remain intact.
- The current calendar year never selects a rule set; exact rules require an inspected year-specific authority.
- Rule precedence is official CUMCM source, supplied template/package, verified dated baseline, CUMCM guidance, then non-binding high-impact-journal editorial practice.
- Nature-derived practices may shape argument, evidence placement, captions, consistency, and readability, but may not impose Nature word/display/reference limits, submission policy, data policy, English house style, landscape-page rules, or journal-specific multi-panel constraints.
- Do not assemble four independent tables into a 2-by-2 composite; normally place no more than two tables consecutively and insert interpretation before more tabular evidence.
- Bold only short key conclusions, decisive indicators, objective functions, critical constraints, risks, or applicability boundaries.
- Ordinary verification must not require SHA256 or source hashes.
- Do not add runtime dependencies or change `scripts/build_pdf.py` without a failing CUMCM-specific test.
- Existing staged natural-layout changes are part of the implementation baseline and must be preserved.
- Git commits require the user's real configured identity. If it remains unavailable, stage each completed task and report the commit blocker without inventing identity values.

---

### Task 1: Define the CUMCM-only public and routing contract

**Files:**
- Create: `tests/test_cumcm_specialization_contract.py`
- Modify: `tests/test_metadata.py`
- Modify: `SKILL.md`
- Modify: `manifest.yaml`
- Modify: `README.md`
- Modify: `agents/openai.yaml`
- Create: `static/fragments/task/polish.md`
- Delete: `static/fragments/language/en.md`
- Delete: `static/fragments/language/zh.md`

**Interfaces:**
- Consumes: existing `validator.validate(root) -> list[str]` and manifest schema.
- Produces: a CUMCM-only router with task values `plan`, `draft-section`, `draft-paper`, `polish`, `restructure`, `audit`, `preflight`, and `submission-package`.

- [ ] **Step 1: Write failing public-scope tests**

Create `tests/test_cumcm_specialization_contract.py` with this test surface:

```python
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class CumcmSpecializationContractTests(unittest.TestCase):
    def text(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8").lower()

    def manifest(self) -> dict:
        return yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))

    def test_public_surfaces_are_cumcm_only(self) -> None:
        for relative in ("SKILL.md", "README.md", "agents/openai.yaml"):
            with self.subTest(relative=relative):
                text = self.text(relative)
                self.assertIn("cumcm", text)
                self.assertNotIn("mcm/icm", text)
                self.assertNotIn("course exercises", text)
                self.assertNotIn("generic contest", text)

    def test_manifest_has_no_contest_or_language_axis(self) -> None:
        axes = self.manifest()["axes"]
        self.assertNotIn("contest", axes)
        self.assertNotIn("language", axes)

    def test_task_axis_includes_polish(self) -> None:
        tasks = self.manifest()["axes"]["task"]["values"]
        self.assertEqual(
            set(tasks),
            {"plan", "draft-section", "draft-paper", "polish", "restructure", "audit", "preflight", "submission-package"},
        )
        self.assertEqual(tasks["polish"], "static/fragments/task/polish.md")

    def test_calendar_year_is_not_a_rule_selector(self) -> None:
        combined = self.text("SKILL.md") + self.text("references/year-selection.md")
        self.assertIn("current calendar year", combined)
        self.assertIn("must not", combined)


if __name__ == "__main__":
    unittest.main()
```

Extend `tests/test_metadata.py` with a test that collects every manifest target
and asserts both deleted language fragments are absent from those targets.

- [ ] **Step 2: Run the new tests and verify RED**

Run: `python -m unittest tests.test_cumcm_specialization_contract tests.test_metadata -v`

Expected: FAIL because public surfaces are contest-neutral, the manifest still
has `contest`/`language`, and `polish` is absent.

- [ ] **Step 3: Rewrite the router and public metadata minimally**

Rewrite `SKILL.md` so it states CUMCM-only scope, loads the manifest and all
`always_load` files, detects the currently available `task` and `delivery` axes,
applies the authority hierarchy, and routes full-paper, LaTeX, and preflight
work to the existing references. Preserve the evidence gate, table-flow rule,
selective-emphasis rule, and submission gate. Add `section` and `model_family`
detection to this router in Tasks 3 and 4 when those axes and fragments exist.

Change `manifest.yaml` to version `1.0.0`, remove `contest` and `language`, add
`polish: static/fragments/task/polish.md`, and retain the existing delivery axis.
Update the top-level description to say the manifest is CUMCM-only.

Set public metadata to:

```yaml
interface:
  display_name: "CUMCM Paper Writing"
  short_description: "Write, revise, validate, and package Chinese CUMCM papers"
  default_prompt: "Use $cumcm-paper-writing for this Chinese CUMCM paper task."
```

Rewrite `README.md` as a concise CUMCM-only user guide covering inputs, supported
tasks, authority hierarchy, validation commands, and repository layout. Create
`static/fragments/task/polish.md` with a diagnosis-first order:

```markdown
# Polish mode

Diagnose task coverage, section purpose, evidence placement, terminology and
notation, and claim boundaries before sentence-level editing. Preserve correct
content and revise only the affected passage unless the correction changes the
argument structure. Return polished Chinese text plus compact revision notes.
```

Delete both language fragments because Chinese behavior is fixed in the core.

- [ ] **Step 4: Run the focused tests and verify GREEN**

Run: `python -m unittest tests.test_cumcm_specialization_contract tests.test_metadata -v`

Expected: PASS.

- [ ] **Step 5: Stage and commit the public contract**

Run: `git add SKILL.md manifest.yaml README.md agents/openai.yaml static/fragments/task/polish.md static/fragments/language tests/test_cumcm_specialization_contract.py tests/test_metadata.py`

Run: `git commit -m "feat: specialize skill for CUMCM"`

Expected: commit succeeds when Git identity is configured; otherwise leave the
task staged and record the existing identity blocker.

---

### Task 2: Add the compact CUMCM core workflow

**Files:**
- Create: `static/core/reader-contract.md`
- Create: `static/core/terminology-notation-ledger.md`
- Modify: `static/core/stance.md`
- Modify: `static/core/workflow.md`
- Modify: `static/core/output-format.md`
- Modify: `manifest.yaml`
- Modify: `tests/test_cumcm_specialization_contract.py`

**Interfaces:**
- Consumes: every request routed by `SKILL.md`.
- Produces: five always-loaded files and three internal artifacts: one-sentence argument, problem-coverage matrix, and terminology/notation ledger.

- [ ] **Step 1: Add failing core-contract tests**

Add tests that assert `manifest.yaml["always_load"]` equals:

```python
[
    "static/core/stance.md",
    "static/core/workflow.md",
    "static/core/output-format.md",
    "static/core/reader-contract.md",
    "static/core/terminology-notation-ledger.md",
]
```

Also assert the core contains these semantic anchors after whitespace
normalization:

```python
required = {
    "static/core/reader-contract.md": [
        "what is answered", "why this model", "what result", "why it is credible", "where it applies"
    ],
    "static/core/terminology-notation-ledger.md": [
        "canonical form", "first-use definition", "unit", "numeric precision", "collision"
    ],
    "static/core/workflow.md": [
        "one-sentence argument", "problem coverage matrix", "terminology and notation ledger",
        "one primary job", "targeted revision"
    ],
}
```

- [ ] **Step 2: Run the core tests and verify RED**

Run: `python -m unittest tests.test_cumcm_specialization_contract -v`

Expected: FAIL because the two core files and workflow anchors do not exist.

- [ ] **Step 3: Implement the five-file core**

Create `reader-contract.md` with the five CUMCM reader questions. Create
`terminology-notation-ledger.md` with a compact ledger schema:

```markdown
| Canonical form | Definition/first use | Symbol or abbreviation | Unit | Precision | Variants/collisions | Decision |
| --- | --- | --- | --- | --- | --- | --- |
```

Require one concept per canonical name, one symbol per quantity within a model,
definition before use, stable units, and one precision per repeated metric.

Revise `stance.md` to fix the language to clear Chinese academic prose and to
separate binding CUMCM rules from non-binding editorial guidance. Revise
`workflow.md` to build the three artifacts, give each paragraph one primary job,
draft from evidence outward, draft the abstract last, run targeted revision, and
trigger a whole-paper consistency sweep after multi-round editing. Revise
`output-format.md` so draft/restructure/polish modes return content, section map,
assumptions, claim-evidence map, terminology decisions, and compact structural
notes; audit/preflight contracts remain separate.

Update `manifest.yaml` to list exactly the five always-loaded files.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run: `python -m unittest tests.test_cumcm_specialization_contract tests.test_metadata -v`

Expected: PASS.

- [ ] **Step 5: Stage and commit the core**

Run: `git add manifest.yaml static/core tests/test_cumcm_specialization_contract.py`

Run: `git commit -m "feat: add CUMCM writing core"`

Expected: commit succeeds with configured identity; otherwise changes remain staged.

---

### Task 3: Add section-aware routing and writing contracts

**Files:**
- Create: `static/fragments/section/abstract.md`
- Create: `static/fragments/section/problem-analysis.md`
- Create: `static/fragments/section/assumptions-notation.md`
- Create: `static/fragments/section/model-formulation.md`
- Create: `static/fragments/section/solution-results.md`
- Create: `static/fragments/section/validation-sensitivity.md`
- Create: `static/fragments/section/model-evaluation.md`
- Create: `static/fragments/section/conclusion.md`
- Create: `static/fragments/section/references.md`
- Create: `static/fragments/section/appendix.md`
- Modify: `manifest.yaml`
- Modify: `static/fragments/task/draft-paper.md`
- Modify: `tests/test_cumcm_specialization_contract.py`

**Interfaces:**
- Consumes: `section` values detected by `SKILL.md`; multiple values are allowed.
- Produces: one focused fragment per CUMCM paper section and a full-paper loading contract.

- [ ] **Step 1: Write failing section-route tests**

Assert the `section` axis is multi-valued and has exactly this mapping:

```python
{
    "abstract": "static/fragments/section/abstract.md",
    "problem-analysis": "static/fragments/section/problem-analysis.md",
    "assumptions-notation": "static/fragments/section/assumptions-notation.md",
    "model-formulation": "static/fragments/section/model-formulation.md",
    "solution-results": "static/fragments/section/solution-results.md",
    "validation-sensitivity": "static/fragments/section/validation-sensitivity.md",
    "model-evaluation": "static/fragments/section/model-evaluation.md",
    "conclusion": "static/fragments/section/conclusion.md",
    "references": "static/fragments/section/references.md",
    "appendix": "static/fragments/section/appendix.md",
}
```

For each fragment, assert it contains `Purpose`, `Required inputs`, `Structure`,
`Evidence boundary`, and `Common failures`. Assert `draft-paper.md` names every
required section value and states that the abstract is drafted last.

- [ ] **Step 2: Run section tests and verify RED**

Run: `python -m unittest tests.test_cumcm_specialization_contract -v`

Expected: FAIL because the axis and fragments are absent.

- [ ] **Step 3: Implement section fragments**

Give every fragment the same five headings but section-specific content:

- `abstract`: problem, method per subproblem, reproducible key result, validation, boundary; no citations or invented numbers.
- `problem-analysis`: convert each prompt demand into an output, evidence need, and model choice criterion.
- `assumptions-notation`: state consequence and testability of assumptions; define symbols, domains, units, and indices once.
- `model-formulation`: objective/state equations, constraints, domains, parameters, and model-selection rationale.
- `solution-results`: keep each subproblem's method/result adjacent; distinguish observed, fitted, predicted, and scenario values.
- `validation-sensitivity`: match validation to model family, vary material assumptions/parameters, and report instability.
- `model-evaluation`: evidence-based strengths, weaknesses, computational cost where measured, and applicability boundary.
- `conclusion`: answer each subproblem without introducing new data; align with abstract and validation.
- `references`: cite sources actually inspected, preserve in-text mapping, and flag unverifiable metadata.
- `appendix`: apply verified code policy, list support files, keep listings readable, and retain complete runnable code outside excerpts.

Update `draft-paper.md` to route through all ten sections in argument order while
drafting the abstract after results and validation stabilize.

- [ ] **Step 4: Run section tests and verify GREEN**

Run: `python -m unittest tests.test_cumcm_specialization_contract tests.test_metadata -v`

Expected: PASS.

- [ ] **Step 5: Stage and commit section routing**

Run: `git add manifest.yaml static/fragments/section static/fragments/task/draft-paper.md tests/test_cumcm_specialization_contract.py`

Run: `git commit -m "feat: route CUMCM paper sections"`

---

### Task 4: Add model-family validation contracts

**Files:**
- Create: `static/fragments/model_family/evaluation.md`
- Create: `static/fragments/model_family/prediction.md`
- Create: `static/fragments/model_family/optimization.md`
- Create: `static/fragments/model_family/mechanistic.md`
- Create: `static/fragments/model_family/simulation.md`
- Create: `static/fragments/model_family/hybrid.md`
- Modify: `manifest.yaml`
- Modify: `references/model-validation.md`
- Modify: `tests/test_cumcm_specialization_contract.py`

**Interfaces:**
- Consumes: one or more model families detected from the solution.
- Produces: model-specific inputs, assumptions, diagnostics, validation, sensitivity, failure boundaries, and prohibited claims.

- [ ] **Step 1: Write failing model-family tests**

Assert `model_family` is multi-valued and maps exactly to the six files above.
For every fragment, require headings `Required inputs`, `Primary diagnostics`,
`Validation`, `Sensitivity`, `Failure boundary`, and `Do not claim`.

Add semantic checks:

```python
anchors = {
    "evaluation.md": ["weight stability", "ranking stability"],
    "prediction.md": ["train", "validation", "extrapolation"],
    "optimization.md": ["feasibility", "objective", "constraint"],
    "mechanistic.md": ["initial", "boundary", "parameter identifiability"],
    "simulation.md": ["random seed", "replication", "convergence"],
    "hybrid.md": ["component", "interface", "propagated uncertainty"],
}
```

- [ ] **Step 2: Run model-family tests and verify RED**

Run: `python -m unittest tests.test_cumcm_specialization_contract -v`

Expected: FAIL because the model-family axis and fragments are absent.

- [ ] **Step 3: Implement model-family fragments and shared validation**

Create the six files with the required headings and anchors. Keep detailed
checks in each family file and reduce `references/model-validation.md` to shared
cross-family principles: define the estimand/output, separate calibration from
validation, compare against a justified baseline, quantify uncertainty where
possible, test material assumptions, report failure cases, and prevent hybrid
components from hiding propagated uncertainty.

- [ ] **Step 4: Run model-family tests and verify GREEN**

Run: `python -m unittest tests.test_cumcm_specialization_contract tests.test_metadata -v`

Expected: PASS.

- [ ] **Step 5: Stage and commit model routing**

Run: `git add manifest.yaml static/fragments/model_family references/model-validation.md tests/test_cumcm_specialization_contract.py`

Run: `git commit -m "feat: add CUMCM model-family validation"`

---

### Task 5: Add result allocation, consistency, and rendered-layout references

**Files:**
- Create: `references/main-text-discipline.md`
- Create: `references/consistency-sweep.md`
- Create: `references/layout-diagnosis.md`
- Modify: `manifest.yaml`
- Modify: `references/paper-structure.md`
- Modify: `references/latex-production-workflow.md`
- Modify: `static/fragments/task/restructure.md`
- Modify: `static/fragments/task/audit.md`
- Modify: `tests/test_editorial_style_contract.py`
- Modify: `tests/test_cumcm_specialization_contract.py`

**Interfaces:**
- Consumes: full papers, Results-heavy sections, multi-round revisions, and rendered PDFs.
- Produces: result-allocation records, targeted revision maps, whole-paper consistency findings, and a compile-render-inspect layout loop.

- [ ] **Step 1: Write failing discipline and layout tests**

Assert `manifest.yaml` routes:

```python
{
    "references/main-text-discipline.md",
    "references/consistency-sweep.md",
    "references/layout-diagnosis.md",
}
```

Assert `main-text-discipline.md` contains the result classes `core answer`,
`necessary support`, `qualification`, `robustness`, `intermediate table`, and
`implementation detail`, plus destinations `main text`, `appendix`, and
`support material`. Assert it forbids burying contradictory evidence.

Assert `consistency-sweep.md` checks abstract/body/conclusion numbers,
terminology, notation, units, precision, cross-references, and claims against
tables. Assert `layout-diagnosis.md` orders `compile`, `log`, `render`, `contact
sheet`, `inspect`, and `iterate`, while containing no fixed Nature float recipe.

- [ ] **Step 2: Run discipline tests and verify RED**

Run: `python -m unittest tests.test_editorial_style_contract tests.test_cumcm_specialization_contract -v`

Expected: FAIL because the three references are absent.

- [ ] **Step 3: Implement the on-demand references**

Adapt the concepts, not the wording, from the inspected `nature-skills` files:

- `main-text-discipline.md`: classify results, build the shortest sufficient
  subproblem evidence chain, separate main text/captions/appendix/support files,
  run a deletion-or-replacement check on additions, and keep contradictory or
  conclusion-changing evidence visible.
- `consistency-sweep.md`: mechanically find variants, inspect context before
  correction, reconcile repeated numbers and precision, compare claims with
  tables/figures, remove display restatement, and repeat until no new material
  inconsistency is found.
- `layout-diagnosis.md`: compile, inspect relevant log warnings, render all pages,
  build a contact sheet, inspect affected pages at readable resolution, diagnose
  float/table/heading/caption/code issues, make the smallest source change, and
  repeat. CUMCM template behavior determines remedies.

Update `paper-structure.md`, `latex-production-workflow.md`, `restructure.md`,
and `audit.md` to link these references only under their observable triggers.
Preserve the existing table-wall and restrained-bold rules.

- [ ] **Step 4: Run discipline tests and verify GREEN**

Run: `python -m unittest tests.test_editorial_style_contract tests.test_cumcm_specialization_contract tests.test_latex_workflow_contract -v`

Expected: PASS.

- [ ] **Step 5: Stage and commit the discipline layer**

Run: `git add manifest.yaml references/main-text-discipline.md references/consistency-sweep.md references/layout-diagnosis.md references/paper-structure.md references/latex-production-workflow.md static/fragments/task/restructure.md static/fragments/task/audit.md tests/test_editorial_style_contract.py tests/test_cumcm_specialization_contract.py`

Run: `git commit -m "feat: add CUMCM manuscript discipline checks"`

---

### Task 6: Remove obsolete generic routing and align CUMCM authority references

**Files:**
- Delete: `references/contest-profile.md`
- Modify: `references/year-selection.md`
- Modify: `references/requirements.md`
- Modify: `references/chinese-quick-reference.md`
- Modify: `references/problem-coverage.md`
- Modify: `references/preflight.md`
- Modify: `references/cumcmthesis-template.md`
- Modify: `references/artifact-consistency.md`
- Modify: `references/code-appendix.md`
- Modify: `static/core/contest-baseline.md`
- Modify: `static/fragments/delivery/source.md`
- Modify: `static/fragments/delivery/rendered.md`
- Modify: `static/fragments/delivery/electronic.md`
- Modify: `static/fragments/delivery/physical.md`
- Modify: `static/fragments/delivery/both.md`
- Modify: `tests/test_cumcm_specialization_contract.py`
- Modify: `tests/test_latex_workflow_contract.py`

**Interfaces:**
- Consumes: verified CUMCM year/package authority and the selected delivery form.
- Produces: no active generic-contest reference and a clear separation between binding CUMCM rules and non-binding editorial guidance.

- [ ] **Step 1: Write failing cleanup tests**

Add a recursive active-content scan over `SKILL.md`, `manifest.yaml`, `README.md`,
`agents/openai.yaml`, `static/`, and `references/`, excluding historical design
documents. Reject `MCM/ICM`, `course exercises`, `unknown contests`, and
`generic contest`. Assert `references/contest-profile.md` does not exist and no
manifest value points to it.

Assert authority references contain `binding CUMCM rule`, `non-binding editorial
guidance`, `selected year`, `official notice`, and `supplied template`. Preserve
the optional-hash assertions from `test_editorial_style_contract.py`.

- [ ] **Step 2: Run cleanup tests and verify RED**

Run: `python -m unittest tests.test_cumcm_specialization_contract tests.test_latex_workflow_contract tests.test_editorial_style_contract -v`

Expected: FAIL because generic content and `contest-profile.md` remain.

- [ ] **Step 3: Complete the CUMCM-only migration**

Delete `references/contest-profile.md`. Rewrite references and delivery
fragments so every exact requirement is conditioned on the selected CUMCM year
and inspected authority. Retain useful historical 2019/2025/2026 pointers as
unverified research aids, never automatic defaults. Keep three-line tables and
CUMCMThesis rules conditional on the supplied template. Keep code policy
`full/core/none/unresolved` subordinate to verified CUMCM rules. Preserve
optional source hashes and no mandatory artifact hashes.

- [ ] **Step 4: Run cleanup tests and verify GREEN**

Run: `python -m unittest tests.test_cumcm_specialization_contract tests.test_latex_workflow_contract tests.test_editorial_style_contract tests.test_metadata -v`

Expected: PASS.

- [ ] **Step 5: Stage and commit cleanup**

Run: `git add -A references static tests`

Run: `git commit -m "refactor: remove generic contest compatibility"`

---

### Task 6A: Normalize the user-supplied practical FAQ

**Files:**
- Create: `references/cumcm-practical-faq.md`
- Modify: `manifest.yaml`
- Modify: `SKILL.md`
- Modify: `references/preflight.md`
- Modify: `references/model-validation.md`
- Modify: `references/code-appendix.md`
- Create: `tests/test_practical_faq_contract.py`

**Interfaces:**
- Consumes: user-supplied `output.md` as non-authoritative source material.
- Produces: a routed, normalized practical FAQ that remains subordinate to selected-year verified CUMCM authority.

- [ ] **Step 1: Write failing normalization tests**

Assert the new reference and route exist; label the source as non-authoritative;
require selected-year verification for page counts, similarity thresholds,
file-size limits, dates, delivery forms, AI-use declarations, and MD5/hash steps;
retain appendix/support-package distinction, model-family-specific validation,
in-text citation discipline, and conditional three-line-table guidance.

Reject active recommendations to evade similarity/AIGC checks, disguise copied
text, modify code for evasion, omit required AI-use disclosure, exploit weak
enforcement, or recommend named commercial writing/rewriting tools. Tests must
check semantics with representative forbidden patterns, not only one exact phrase.

- [ ] **Step 2: Run focused tests and verify RED**

Run: `python -m unittest tests.test_practical_faq_contract -v`

Expected: FAIL because the normalized reference and route do not exist.

- [ ] **Step 3: Implement the smallest normalized reference**

Summarize usable principles rather than copying the twenty Q&A entries. Separate
`verified rule`, `non-binding guidance`, and `unverified claim`. Route the
reference only for relevant preflight, validation, appendix/support-package, or
submission questions; do not add it to the compact always-loaded core.

No volatile number from `output.md` becomes a default. No new ordinary hash
validation is introduced. The official selected-year notice/package/template
remains authoritative.

- [ ] **Step 4: Run focused and regression verification**

Run: `python -m unittest tests.test_practical_faq_contract tests.test_cumcm_specialization_contract tests.test_editorial_style_contract tests.test_latex_workflow_contract -v`

Run: `python scripts/validate_skill.py`

Expected: all pass.

- [ ] **Step 5: Stage the FAQ normalization**

Stage only Task 6A files. Do not copy `output.md` into the repository and do not
commit while Git identity remains unavailable.

---

### Task 7: Validate the complete skill and documentation

**Files:**
- Modify: `scripts/validate_skill.py`
- Modify: `tests/test_metadata.py`
- Modify: `docs/superpowers/specs/2026-09-07-cumcm-specialization-design.md` only if validation exposes an actual specification contradiction
- Test: all files under `tests/`

**Interfaces:**
- Consumes: completed CUMCM-only repository.
- Produces: structural validation for every axis and route, including multi-valued axes and duplicate-path detection.

- [ ] **Step 1: Write failing validator tests**

Extend `tests/test_metadata.py` with temporary-manifest cases asserting that
`validator.validate()` reports:

- a missing section fragment;
- a missing model-family fragment;
- an absolute or escaping route;
- a duplicated `always_load` path;
- a `default` value not present in an axis.

The tests must assert the relevant path or axis name appears in each error.

- [ ] **Step 2: Run validator tests and verify RED**

Run: `python -m unittest tests.test_metadata -v`

Expected: at least the duplicate `always_load` case FAILS because the current
validator does not detect duplicates.

- [ ] **Step 3: Extend the validator minimally**

In `scripts/validate_skill.py`, retain the existing YAML/frontmatter/UI checks
and add one duplicate-route pass:

```python
seen = set()
for path in paths:
    if path in seen:
        errors.append(f"Duplicate route: {path}")
    seen.add(path)
```

Do not add content-style regex enforcement to the validator; policy behavior
belongs in contract tests.

- [ ] **Step 4: Run complete verification**

Run: `python scripts/validate_skill.py`

Expected: `Skill metadata and routes: PASS`.

Run: `python -m unittest discover -s tests -v`

Expected: all tests pass with zero failures and zero errors.

Run: `git diff --check` and `git diff --cached --check`.

Expected: both exit 0; line-ending conversion notices are informational, not
whitespace errors.

Run: `rg -n -i "mcm/icm|course exercises|unknown contests|generic contest|sha256|source hash|final pdf hash" SKILL.md manifest.yaml README.md agents static references tests`.

Expected: no active generic-competition claims or mandatory artifact-hash rules;
test fixtures may contain rejected phrases only inside explicit negative assertions.

- [ ] **Step 5: Review the staged diff against the specification**

Check each acceptance criterion in
`docs/superpowers/specs/2026-09-07-cumcm-specialization-design.md` against the
staged files. Confirm the router, manifest, README, UI metadata, fragments,
references, and tests agree on names and paths.

- [ ] **Step 6: Stage and commit final validation changes**

Run: `git add -A`

Run: `git commit -m "test: verify CUMCM specialized workflow"`

Expected: commit succeeds with configured identity; otherwise all verified
changes remain staged on `feature/natural-paper-layout` and the identity blocker
is reported without changing Git configuration.
