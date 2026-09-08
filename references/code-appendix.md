# Concise code appendices

Keep the complete runnable engineering project. The policy values
`full`/`core`/`none`/`unresolved` are subordinate to verified CUMCM rules for
the selected year:
- full: include all required complete source; simplify unused or duplicated code
  in the implementation first and rerun tests. Do not omit required dependencies.
- core: include key model/solver/metric functions or permitted pseudocode. Keep
  I/O, plot styling, logging, environment setup and duplicate experiments in support.
- none: omit code listings and provide permitted algorithm/provenance descriptions.
- unresolved: prepare a concise provisional draft, preserve complete code and mark
  appendix compliance unchecked until the actual rule is verified.

No universal line/page quota. An author-requested length target is subordinate
to verified submission rules. Do not shrink fonts to unreadable sizes.
Map paper algorithms/equations to source file, function/region and run command.
Extract core listings from actual tested source and record the selection.
Label excerpts as partial and state dependencies. Never pretend an excerpt runs
standalone. Prefer one representative implementation over repeated variants.
After shortening, verify numerical equivalence with justified tolerances,
source/excerpt agreement, wrapping and final-page readability.
Use cumcm-practical-faq.md to preserve the appendix versus support package
distinction; verify the selected-year contents of each separately.
