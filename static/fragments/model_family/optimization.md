# Optimization-model validation

## Required inputs

Specify variables/domains, objective, complete constraints, and the solver/stopping rule.

## Primary diagnostics

Report feasibility, objective/bound checks, and solver termination status.

## Validation

Verify each returned solution against all complete constraints and independent bounds.

## Sensitivity

Perturb constraints, inputs, and objective coefficients within justified ranges.

## Failure boundary

Describe infeasible, unstable, or solver-limited instances.

## Do not claim

Do not make a global-optimum claim without a valid certificate.
