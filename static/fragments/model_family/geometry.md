# Geometry-model validation

## Required inputs

Define coordinate frame and handedness, angle convention, units, objects and
dimensions, transformations, tolerances and geometric constraints.

## Primary diagnostics

Check known directions, symmetric cases, vector norms, rotation/translation
invariants and distance residuals. Verify quadrant handling explicitly.

## Validation

Compare a small construction with an independent formula or hand calculation.
Apply identical filters to object coordinates and their IDs/attributes. Recheck
clearances, boundaries and dimensions on the exported rounded solution.

## Sensitivity

Vary meaningful placement, scale, geometry or discretization parameters within
justified ranges. Check numerical tolerance separately from physical clearance.

## Failure boundary

Name degeneracies, grazing angles, overlap, boundary clipping and approximation
errors. Quantify any residual violation instead of rounding it away silently.

## Do not claim

Do not use a plausible diagram as proof of feasible geometry, or a coordinate
check as validation of an entire energy/physical model coupled to it.
