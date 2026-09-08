# CUMCM Paper Writing

A source-grounded workflow for planning, drafting, revising, validating,
rendering, and packaging Chinese CUMCM papers.

Current release: `2.0.0`. See [CHANGELOG.md](CHANGELOG.md) for the upgrade and
migration notes.

## Inputs

Invoke `$cumcm-paper-writing` with the problem, competition year, data, code,
results, requested task and delivery format, plus any official notice or supplied
template. Chinese is the manuscript default; canonical English method names,
mathematics, variables, units, and citations remain intact.

## Supported tasks

`plan`, `draft-section`, `draft-paper`, `polish`, `restructure`, `audit`,
`preflight`, and `submission-package` are available. Delivery routes cover
source, rendered output, electronic or physical packages, and both packages.

## Authority

Apply official CUMCM sources first, then the supplied template or package, a
verified dated baseline, CUMCM guidance, and finally non-binding high-impact-
journal editorial practice. The current calendar year never selects rules;
inspect a year-specific authority before enforcing exact requirements.

## Validation

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_skill.py
```

## Repository layout

`SKILL.md` defines routing behavior; `manifest.yaml` maps task, delivery,
section, and model-family fragments; `static/` contains shared and routed
instructions; `references/` contains focused CUMCM guidance; `scripts/` and
`tests/` provide validation.
