# Model validation

Select checks by model type:
- Descriptive: counting identities, batch keys, units, denominators and missingness.
- Predictive: target timing, leakage, baseline, temporal/group-aware validation,
  calibration and uncertainty.
- Optimization: domains, objective type, complete constraints, feasibility,
  solver status, gap and comparable inputs.
- Simulation: assumptions, initialization, stochastic seeds/repeats, sensitivity,
  and separation of observed and simulated effects.

Every probability needs an event, conditioning set, numerator, denominator,
sample size and missing-value rule. No observations means NA, not probability
zero. Sparse cells need qualification; do not infer individual prediction accuracy.

Define symbols and index sets. Distinguish original ordinal slots from compressed
nonempty rankings. Empty entries do not authorize reindexing. Quadratic objectives
need a compatible solver or an explicit reformulation.

Separate training fit, validation and extrapolation. High training R-squared,
small RMSE or alternating residual signs cannot prove absence of overfitting.
Report sample/parameter counts and limitations when external validation is absent.
Monotone nested-prefix counts may follow by construction, not a causal benefit.
Distinguish observed differences, statistical significance, prediction and causality.
New conclusions require evidence-ledger updates before publication.
