# CUMCM LaTeX Readiness and Windows Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install MiKTeX/XeLaTeX on Windows, make the PDF builder tolerate inaccessible `PATH` entries, and expose honest CUMCM rendering-readiness limits with automated and real-build verification.

**Architecture:** Keep `scripts/build_pdf.py` as the single trusted compiler entry point and isolate Windows path inspection in a small private helper. Add one on-demand `environment-readiness` reference and a focused contract test so the skill reports engine/template/authority/PDF limitations without silently changing renderers or claiming competition readiness. Verify the real engine through an integration test, then synchronize the validated source skill to both local installations.

**Tech Stack:** Python 3 standard library (`pathlib`, `shutil`, `subprocess`, `tempfile`, `unittest`), Markdown, YAML, PowerShell `winget`, MiKTeX XeLaTeX.

## Global Constraints

- The skill remains CUMCM-only; selected-year official authority and supplied template/package rules override all editorial guidance.
- The current calendar year must never select a CUMCM rule set, and a synthetic PDF fixture cannot establish scientific validity or submission compliance.
- For LaTeX/PDF delivery, missing XeLaTeX or template files, failed compiler exits, unresolved log errors, or absent PDFs are explicit `blocked` conditions; Word/DOCX and source-only delivery use their own artifact checks and do not require XeLaTeX; no silent renderer fallback is permitted.
- Preserve two XeLaTeX passes, `-no-shell-escape`, temporary build isolation, log gates, PDF signature validation, and atomic replacement of an older PDF only after a successful build.
- A `PATH` entry that raises `OSError` or `ValueError` during inspection is skipped while usable entries retain their original order; compiler lookup still fails clearly when no engine is found.
- Ordinary verification does not require SHA256, MD5, or source hashes; mention hashes only for an inspected selected-year submission rule.
- Do not add runtime dependencies or import Nature-specific word counts, display quotas, figure rules, or submission policies.
- Do not change global Git identity or push a new release unless the user explicitly requests publication after verification.

---

### Task 1: Harden Windows PATH filtering in the PDF builder

**Files:**
- Modify: `scripts/build_pdf.py`
- Test: `tests/test_build_pdf.py`

**Interfaces:**
- Consumes: the process `PATH` string and the existing `build(source, output, template=None, engine='xelatex')` contract.
- Produces: private `_path_entry_is_usable(entry: str) -> bool` and `_sanitize_path(path_value: str) -> str`; `build()` passes the sanitized value to `shutil.which` without changing its public signature.

- [ ] **Step 1: Write the failing regression test**

Append this method to `BuildTests` in `tests/test_build_pdf.py`:

```python
    def test_permission_denied_path_entry_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / 'paper.tex', root / 'paper.pdf'
            source.write_text('test source', encoding='utf-8')
            restricted = root / 'restricted-path-entry'
            permission_checks = []
            calls = []

            def compiler(command, **kwargs):
                calls.append(command)
                work = Path(next(x.split('=', 1)[1] for x in command
                                 if x.startswith('-output-directory=')))
                (work / 'paper.log').write_text('', encoding='utf-8')
                (work / 'paper.pdf').write_bytes(b'%PDF-new')
                return subprocess.CompletedProcess(command, 0, '', '')

            original_is_dir = builder.Path.is_dir

            def guarded_is_dir(path):
                if Path(path) == restricted:
                    permission_checks.append(path)
                    raise PermissionError('access denied')
                return original_is_dir(path)

            with patch.object(builder.Path, 'is_dir', guarded_is_dir), \
                 patch.object(builder.shutil, 'which', return_value='xelatex') as which, \
                 patch.object(builder.subprocess, 'run', side_effect=compiler), \
                 patch.dict(os.environ, {'PATH': os.pathsep.join([str(restricted), str(root)])}, clear=False):
                builder.build(source, output)

            self.assertEqual(output.read_bytes(), b'%PDF-new')
            self.assertEqual(len(calls), 2)
            self.assertTrue(permission_checks)
            self.assertNotIn(str(restricted), which.call_args.kwargs['path'])
```

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_build_pdf.BuildTests.test_permission_denied_path_entry_is_ignored -v`

Expected: `ERROR` with `PermissionError: access denied` from the existing `Path.is_dir()` comprehension.

- [ ] **Step 3: Implement the smallest safe helper**

In `scripts/build_pdf.py`, place these functions above `build()` and replace the direct comprehension with `_sanitize_path(env.get('PATH', ''))`:

```python
def _path_entry_is_usable(entry: str) -> bool:
    try:
        return Path(entry).is_dir()
    except (OSError, ValueError):
        return False


def _sanitize_path(path_value: str) -> str:
    return os.pathsep.join(
        entry for entry in path_value.split(os.pathsep)
        if _path_entry_is_usable(entry)
    )
```

The helper must not catch compiler errors, subprocess errors, or log errors;
only path-value inspection failures are downgraded to an unusable entry.

- [ ] **Step 4: Run the regression and existing builder tests**

Run: `python -m unittest tests.test_build_pdf -v`

Expected: all existing tests plus `test_permission_denied_path_entry_is_ignored` pass, with no `cumcm-build-*` directory left in each temporary fixture.

- [ ] **Step 5: Commit the isolated builder change**

Run:

```powershell
git add scripts/build_pdf.py tests/test_build_pdf.py
git -c user.name='Ouy5517' -c user.email='176414220+Ouy5517@users.noreply.github.com' commit -m "fix: tolerate inaccessible Windows PATH entries"
```

Expected: one commit containing only the builder and its regression test.

---

### Task 2: Add explicit CUMCM environment-readiness limits

**Files:**
- Create: `references/environment-readiness.md`
- Modify: `manifest.yaml`
- Modify: `SKILL.md`
- Modify: `references/preflight.md`
- Modify: `references/latex-production-workflow.md`
- Modify: `static/core/output-format.md`
- Create: `tests/test_environment_readiness_contract.py`

**Interfaces:**
- Consumes: the existing `task`, `delivery`, and on-demand reference routing.
- Produces: a routed readiness contract with statuses `ready`, `ready_with_author_checks`, and `blocked`.

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_environment_readiness_contract.py`:

```python
from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]


class EnvironmentReadinessContractTests(unittest.TestCase):
    def read(self, relative):
        return ' '.join((ROOT / relative).read_text(encoding='utf-8').lower().split())

    def test_reference_is_routed_for_engine_and_render_questions(self):
        manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        paths = {item['path'] for item in manifest['references']['on_demand']}
        self.assertIn('references/environment-readiness.md', paths)

    def test_statuses_and_boundaries_are_explicit(self):
        text = self.read('references/environment-readiness.md')
        for phrase in (
            'ready', 'ready_with_author_checks', 'blocked',
            'selected-year official authority', 'current calendar year',
            'must not select', 'synthetic fixture',
            'not scientific validity', 'absent pdf', 'unverified',
            'xelatex is missing', 'do not silently switch to reportlab',
        ):
            self.assertIn(phrase, text)

    def test_latex_workflow_points_to_readiness_gate(self):
        workflow = self.read('references/latex-production-workflow.md')
        preflight = self.read('references/preflight.md')
        output = self.read('static/core/output-format.md')
        self.assertIn('environment-readiness.md', workflow)
        self.assertIn('environment-readiness.md', preflight)
        self.assertIn('ready_with_author_checks', output)

    def test_no_claim_of_rendered_pass_without_a_fresh_pdf(self):
        text = self.read('references/environment-readiness.md')
        self.assertIn('source compilation alone', text)
        self.assertIn('cannot claim visual', text)
        self.assertIn('older pdf', text)

    def test_word_delivery_keeps_an_artifact_specific_path(self):
        rendered = self.read('static/fragments/delivery/rendered.md')
        electronic = self.read('static/fragments/delivery/electronic.md')
        preflight = self.read('references/preflight.md')
        self.assertIn('docx', rendered)
        self.assertIn('file formats', electronic)
        self.assertIn('word', rendered)
        self.assertIn('do not require xelatex', preflight)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the new contract test and verify RED**

Run: `python -m unittest tests.test_environment_readiness_contract -v`

Expected: `FAIL` because the new reference and route do not yet exist.

- [ ] **Step 3: Add the readiness reference and route it**

Create `references/environment-readiness.md` with this content:

```markdown
# CUMCM environment readiness

Use this reference for LaTeX engine, template, render, PDF, or submission
preflight questions. It describes toolchain readiness; it does not replace the
selected-year official CUMCM notice, supplied template/package, or scientific
validation. Readiness is specific to the requested final artifact; Word/DOCX
and source-only delivery use their own artifact and renderer checks.

## Status contract

- `ready`: a fresh requested artifact was produced, its applicable structure
  and visual checks passed, anonymity and package checks passed, and the
  selected-year authority was inspected. LaTeX/PDF requires fresh PDF review;
  Word/DOCX requires fresh DOCX and Word-render review.
- `ready_with_author_checks`: the build and technical checks are usable, but an
  author-owned item such as the selected-year notice, identity fields,
  disclosure wording, page rule, or support-file allowlist remains unresolved.
- `blocked`: the requested artifact's engine/template, source, required
  evidence, or build gate is unavailable or failed. XeLaTeX is required only
  for LaTeX/PDF delivery.

## Hard limitations

1. Resolve the selected-year official authority before enforcing page,
   anonymity, disclosure, file-size, date, or support-package rules. The
   current calendar year must not select a CUMCM rule set.
2. For LaTeX/PDF delivery, check the requested engine before rendering. If
   XeLaTeX is missing, report `blocked` with the platform-specific installation
   command and preserve the source; do not silently switch to ReportLab, Word,
   Markdown, or another renderer.
3. A missing template or year style is an author input gap, not permission to
   invent a class, page limit, declaration, or layout rule.
4. For LaTeX/PDF delivery, a failed build, an absent PDF, or an older PDF left
   in place is `blocked`. Source compilation alone cannot claim visual pass,
   table-flow pass, overflow pass, font pass, or submission readiness; those
   checks are `UNVERIFIED` until a fresh PDF is rendered and inspected. For
   Word/DOCX delivery, use its own DOCX build and render gate; a missing PDF is
   not by itself a block.
5. A synthetic fixture proves only that the local toolchain can compile a small
   document. It is not scientific validity, model validation, CUMCM compliance,
   or evidence that a real paper's tables, formulas, fonts, or page count pass.
6. The skill cannot certify plagiarism/AIGC-detector outcomes, promise an
   acceptance result, or recommend evasion. Preserve required disclosures and
   author review.

## Windows XeLaTeX preflight for LaTeX/PDF delivery

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
```

Add this on-demand manifest item:

```yaml
    - condition: the LaTeX engine, template availability, PDF render, or environment readiness is uncertain
      path: references/environment-readiness.md
```

Add to `SKILL.md` after the LaTeX routing paragraph:

```markdown
For engine, template, PDF, or platform-readiness questions, also load
`references/environment-readiness.md`. It distinguishes `ready`,
`ready_with_author_checks`, and `blocked`; when LaTeX/PDF delivery is
requested, a missing engine or fresh PDF is never hidden by a renderer
fallback or an older artifact.
```

Add to `references/preflight.md`:

```markdown
Load environment-readiness.md before assigning a readiness status. For
LaTeX/PDF delivery, a missing engine, missing template, failed build, or
absent fresh PDF is `blocked`; for Word/DOCX or source-only delivery, assess
the requested artifact with its own renderer and do not require XeLaTeX. An
uninspected selected-year rule or author-owned field is
`ready_with_author_checks`, not passed by assumption.
```

Add to `references/latex-production-workflow.md` immediately before `## 3. Build reproducibly`:

```markdown
Load environment-readiness.md before compiling. Verify the requested engine
and template first; if either is unavailable, stop with `blocked` and preserve
the source. Never use an older PDF or a different renderer as evidence of a
fresh LaTeX build.
```

Add to `static/core/output-format.md` under the preflight contract:

```markdown
Use `ready`, `ready_with_author_checks`, or `blocked` from
`references/environment-readiness.md`; technical compilation cannot override
an unresolved selected-year authority or author-owned submission check.
Word/DOCX delivery does not require XeLaTeX; readiness is specific to the
requested artifact.
```

- [ ] **Step 4: Run focused and regression contracts**

Run: `python -m unittest tests.test_environment_readiness_contract tests.test_latex_workflow_contract tests.test_editorial_style_contract -v`

Expected: all tests pass and the existing optional-hash and CUMCM-template boundaries remain intact.

- [ ] **Step 5: Commit the documented limitation contract**

Run:

```powershell
git add references/environment-readiness.md manifest.yaml SKILL.md references/preflight.md references/latex-production-workflow.md static/core/output-format.md tests/test_environment_readiness_contract.py
git -c user.name='Ouy5517' -c user.email='176414220+Ouy5517@users.noreply.github.com' commit -m "docs: define CUMCM environment readiness limits"
```

Expected: one commit containing the route, reference, core wording, and tests.

---

### Task 3: Install MiKTeX and verify a real XeLaTeX build

**Files:**
- Create: `tests/test_build_pdf_integration.py`
- Create: `tests/fixtures/minimal-xelatex.tex`

**Interfaces:**
- Consumes: the hardened `scripts/build_pdf.py` and a system `xelatex` executable.
- Produces: a valid fresh PDF when XeLaTeX is installed; an explicit skipped test reason otherwise.

- [ ] **Step 1: Add a minimal real-build fixture and integration test**

Create `tests/fixtures/minimal-xelatex.tex`:

```tex
\documentclass{article}
\begin{document}
CUMCM LaTeX readiness check.
\end{document}
```

Create `tests/test_build_pdf_integration.py`:

```python
from pathlib import Path
import importlib.util
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('builder', ROOT / 'scripts' / 'build_pdf.py')
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


@unittest.skipUnless(shutil.which('xelatex'), 'xelatex/MiKTeX is not installed')
class RealXeLaTeXBuildTests(unittest.TestCase):
    def test_real_xelatex_build_produces_fresh_pdf(self):
        with tempfile.TemporaryDirectory(prefix='cumcm-integration-') as directory:
            root = Path(directory)
            source = root / 'paper.tex'
            output = root / 'paper.pdf'
            source.write_text(
                (ROOT / 'tests' / 'fixtures' / 'minimal-xelatex.tex').read_text(encoding='utf-8'),
                encoding='utf-8',
            )
            with patch.object(builder.subprocess, 'run', wraps=builder.subprocess.run) as run:
                result = builder.build(source, output)
            self.assertEqual(result, output.resolve())
            self.assertEqual(run.call_count, 2)
            self.assertTrue(output.is_file())
            self.assertTrue(output.read_bytes().startswith(b'%PDF-'))
            self.assertEqual(list(root.glob('cumcm-build-*')), [])


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Check the package identity before installation**

Run: `winget search --id MiKTeX.MiKTeX --exact --source winget`

Expected: one result whose ID is `MiKTeX.MiKTeX`. If the package manager reports
no result, stop and use the official MiKTeX Windows installer, then continue
with the same version and build checks.

- [ ] **Step 3: Install MiKTeX with explicit noninteractive agreements**

Run:

```powershell
winget install --id MiKTeX.MiKTeX --exact --silent `
  --accept-source-agreements --accept-package-agreements
```

Expected: exit code 0 (or an explicit “already installed” result). Do not
change system-wide Git configuration or delete any existing TeX installation.

- [ ] **Step 4: Resolve the new executable in a fresh shell and run the version gate**

Run in a new PowerShell process:

```powershell
powershell -NoProfile -Command "xelatex --version"
```

Expected: output names MiKTeX and XeTeX, and `xelatex` resolves on `PATH`. If
the command is absent, report `blocked` with the installed location rather
than invoking another renderer.

- [ ] **Step 5: Run the real integration test and a direct builder command**

Run: `python -m unittest tests.test_build_pdf_integration -v`

Expected: one `ok` test and no skip after installation. Then run:

```powershell
$verifyDir = Join-Path $env:TEMP 'cumcm-latex-readiness'
New-Item -ItemType Directory -Force -Path $verifyDir | Out-Null
python scripts/build_pdf.py tests/fixtures/minimal-xelatex.tex --output (Join-Path $verifyDir 'paper.pdf')
pdfinfo (Join-Path $verifyDir 'paper.pdf')
```

Expected: the builder prints the resolved PDF path, `pdfinfo` reports a valid
PDF, and the source repository contains no `cumcm-build-*` directory.

- [ ] **Step 6: Commit the integration fixture and test**

Run:

```powershell
git add tests/test_build_pdf_integration.py tests/fixtures/minimal-xelatex.tex
git -c user.name='Ouy5517' -c user.email='176414220+Ouy5517@users.noreply.github.com' commit -m "test: verify real XeLaTeX integration"
```

Expected: one commit with no generated PDF or temporary build files.

---

### Task 4: Synchronize installed skill copies and complete verification

**Files:**
- Modify: `C:\Users\14564\.agents\skills\cumcm-paper-writing\` (copy of the validated source tree)
- Modify: `C:\Users\14564\.codex\skills\cumcm-paper-writing\` (copy of the validated source tree)

**Interfaces:**
- Consumes: the source tree after Tasks 1–3 and its passing test/validation output.
- Produces: two installed copies with identical content and manifest version.

- [ ] **Step 1: Verify target paths before copying**

Run:

```powershell
$source = (Resolve-Path 'cumcm-paper-writing').Path
$targets = @('C:\Users\14564\.agents\skills\cumcm-paper-writing', 'C:\Users\14564\.codex\skills\cumcm-paper-writing')
$targets | ForEach-Object { "$(Resolve-Path $_) <- $source" }
```

Expected: both resolved targets are the two named `cumcm-paper-writing` skill
directories, not a parent directory or workspace root.

- [ ] **Step 2: Copy validated source files into both installed locations**

Run:

```powershell
Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
    if ($_.Name -ne '.git') {
        Copy-Item -LiteralPath $_.FullName -Destination $targets[0] -Recurse -Force
        Copy-Item -LiteralPath $_.FullName -Destination $targets[1] -Recurse -Force
    }
}
```

Expected: both destinations contain the new reference, tests, builder, and
integration fixture; no source files are modified.

- [ ] **Step 3: Compare versions and representative files**

Run:

```powershell
foreach ($target in $targets) {
    $manifest = Get-Content -Raw (Join-Path $target 'manifest.yaml')
    $skill = Get-Content -Raw (Join-Path $target 'SKILL.md')
    [pscustomobject]@{ Target = $target; Version = ([regex]::Match($manifest, '(?m)^version:\s*(\S+)').Groups[1].Value); SkillBytes = ([Text.Encoding]::UTF8.GetByteCount($skill)) }
}
```

Expected: both rows report version `2.0.0` and equal `SkillBytes`; the new
reference and builder tests are present in both copies. This comparison is a
deployment check, not a user-facing requirement for ordinary paper work.

- [ ] **Step 4: Run the complete source verification suite**

Run:

```powershell
python scripts/validate_skill.py
python -m unittest discover -s tests -q
git diff --check
git status --short --branch
```

Expected: `Skill metadata and routes: PASS`, all tests pass (including the real
XeLaTeX integration test), `git diff --check` is clean, and the working tree is
clean after the commits. If `pdfinfo` is unavailable, retain the valid PDF
signature and report `pdfinfo` as an author environment check rather than
claiming full visual verification.

- [ ] **Step 5: Record the final readiness result**

Report the installed MiKTeX/XeLaTeX version, builder test result, integration
PDF result, source commit IDs, synchronized skill targets, and any remaining
`ready_with_author_checks` items. Do not claim CUMCM submission readiness
without a selected-year official notice, supplied template/package, real paper
content, every-page visual review, anonymity scan, and archive inspection.
