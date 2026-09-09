# Solve and retain evidence

Implement or derive the smallest complete answer first. Use explicit inputs and
units; centralize shared scenario parameters so downstream questions consume the
same updated values. Inspect downloaded code before using any part of it.

Run cheap hand checks or small enumerations before a large search. Record the
actual command, input version, dependencies used, solver status and outputs;
record seeds only for stochastic calculations. A script existing is not a run.
For derivations preserve assumptions and intermediate steps needed to check it.

For optimization report the best feasible value and any valid bound/certificate,
plus stopping condition, elapsed compute if measured and constraint residuals.
Check the exported/rounded solution again, not just solver memory. Keep the
baseline and diagnosed failures when they affect the interpretation.

If a solver or runtime is unavailable, complete independent derivations and
small checks, then mark the larger computation unexecuted. Do not install an
entire historical environment when a scoped dependency is sufficient. Move to
`validate` before promoting computed outputs to manuscript claims.
