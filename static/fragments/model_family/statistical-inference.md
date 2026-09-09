# Statistical-inference validation

## Required inputs

Define the estimand, independent unit, sampling/design structure, measurement
process, groups or repeated observations, missingness and model assumptions.

## Primary diagnostics

Check sample size at the independent-unit level, dependence, distributions or
residuals relevant to the method, effect estimates and uncertainty. Separate
entity state from measurement-site state in nested records.

## Validation

Use appropriate analytic checks or resampling that preserves the sampling
structure. Where multiple comparisons support a joint claim, state the family
and treatment of multiplicity. Check preprocessing against original records.

## Sensitivity

Vary justified missingness assumptions, inclusion rules, transformations and
model specifications. For composition data inspect closure and zero meanings
before considering log ratios; no universal transformation is prescribed.

## Failure boundary

Identify selection bias, non-identifiability, small independent sample counts,
unmeasured confounding or unsupported distribution assumptions.

## Do not claim

Do not treat repeated measurements as independent samples or infer causality
from association. A stable prediction under perturbation is not test accuracy.
