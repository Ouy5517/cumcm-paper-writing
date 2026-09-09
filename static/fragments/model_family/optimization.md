# Optimization-model validation

## Required inputs

Specify variables/domains, objective, complete constraints, and the solver/stopping rule.

## Primary diagnostics

Report feasibility, objective/bound checks, and solver termination status.

## Validation

Verify each returned solution against all complete constraints and independent bounds.
For schedules or curve-based constraints, check event timing and the final
exported trajectory under the problem's completion/threshold definitions; use
references/temporal-validation.md. Approximate search within a restricted horizon
or model does not establish an unrestricted optimum.

## Sensitivity

Perturb constraints, inputs, and objective coefficients within justified ranges.

## Failure boundary

Describe infeasible, unstable, or solver-limited instances.

## Do not claim

Do not make a global-optimum claim without a valid certificate.
