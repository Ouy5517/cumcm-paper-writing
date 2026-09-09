# Validate the solution

Load `references/model-validation.md` and the applicable family checks. Test
whether the requested output is supported, not merely whether code terminates.
Use independent formulas, observations, limiting cases, brute-force small cases
or conserved quantities as appropriate. Reusing the same implementation's
answer as its test oracle is not independent validation.

Check feasibility and accounting, units and bounds, input uncertainty, material
assumptions and result-to-artifact agreement. For data-derived models separate
fitting from evaluation and define the independent sampling unit. A missing
held-out target limits performance claims; it does not authorize invented scores.

If a check fails, identify the input, model, implementation or export stage
responsible and revise affected outputs. Increase model complexity only when
the evidence indicates it will repair the problem. Report tested range and
remaining failure boundary; never make sensitivity tests a fixed ritual.

Return actual checks and outcomes, the claims now supported, unresolved issues
and the coverage matrix update. Keep human review and competition compliance
separate from numerical validation.
