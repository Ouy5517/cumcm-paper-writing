# Simulation-model validation

## Required inputs

Specify state transitions/events, initial conditions, parameters and time/space
discretization. For stochastic simulation also specify distributions, random
seed and replications. Identify calibration data when calibration is used.

## Primary diagnostics

Report convergence/Monte Carlo error as applicable: step-size or mesh convergence
for deterministic simulations; Monte Carlo uncertainty and replication summaries
for stochastic simulations. Report calibration fit only if calibration occurred.
An exact discrete recurrence needs an independent recurrence/closed-form or
boundary check, not an invented time-step or mesh-refinement study.

## Validation

Compare simulated outputs with held-out observations or independently known behavior.
For discrete-event models, replay a small event ledger and check resource
occupancy, precedence, conservation and the exact completion rule at the horizon.
Use references/temporal-validation.md for applicable event or curve checks.

## Sensitivity

Vary material calibration inputs, event rules or discretization. Vary
distributions and assess random seeds only for stochastic simulations.

## Failure boundary

Identify applicable limits: discretization error when approximating continuous
dynamics, rare events or insufficient replication for stochastic simulations,
and uncalibrated regimes when calibrated parameters are used.

## Do not claim

Do not draw a stochastic single-run conclusion about a distribution or a
real-world causal claim from simulation alone. Deterministic runs need no
invented random seeds or replications.
