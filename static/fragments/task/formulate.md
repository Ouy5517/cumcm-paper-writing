# Formulate a model

Load `references/model-selection.md` and the applicable model-family fragments.
For each required output define variables and domains, known parameters and units,
equations or relations, assumptions, objective and complete constraints when
optimizing. Explain why the representation matches the question and data.

Choose a tractable baseline and only useful alternatives. For an analytical
problem this may be a derivation with a limiting-case check. For a coupled model
define each interface's meaning, shape, unit, uncertainty and dependency order.
Avoid selecting a complex algorithm merely because a case paper used it.

Before solving specify a falsification or acceptance check: feasibility tolerance,
mass/energy balance, held-out metric, independent enumeration or other justified
criterion. Separate supplied tolerances from analyst-selected ones. Link each
material assumption to the output it might change and a feasible check.
