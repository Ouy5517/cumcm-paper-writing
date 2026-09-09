# Hybrid-model validation

## Required inputs

Name each component, define interface variables/units, and state calibration order.

## Primary diagnostics

Report component and end-to-end checks, propagated uncertainty, and cross-model consistency.

## Validation

Validate each component and the full pipeline against relevant independent evidence.

## Sensitivity

Vary meaningful interface values and uncertainty passed between components.
Check interface variables/units for conversion invariance; do not perturb units
as if they were physical parameters. Test calibration order only if scientifically
meaningful; preserve actual computational dependencies.

## Failure boundary

Describe interface mismatch, incompatible assumptions, and uncertainty amplification.

## Do not claim

Do not let one component's fit validate the full pipeline.
