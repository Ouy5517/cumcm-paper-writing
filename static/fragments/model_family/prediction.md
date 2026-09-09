# Prediction-model validation

## Required inputs

Specify the target, split protocol, leakage controls, baseline, and metric.
For dated observations define information availability at prediction time, not
only the timestamp of the measured event. Use references/temporal-validation.md
when a forecast enters a decision. Sales alone may not identify uncensored demand.

## Primary diagnostics

Report separate train and validation/test performance only where targets exist
and the split supports the claim. Report extrapolation performance only with
independent target observations in that range; otherwise label extrapolation
as assumption-dependent and unvalidated.

## Validation

Use calibration, residual, or forecast diagnostics as applicable to the prediction setting.

## Sensitivity

Test split choices, feature availability, horizon, and plausible deployment shifts.

## Failure boundary

State where the target population, time range, or covariates exceed observed support.

## Do not claim

Do not infer causality from prediction.
