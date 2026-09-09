# Prepare inputs

Load `references/input-audit.md`. Inventory the actual files and parameter
tables, retaining immutable originals. Establish sample/entity IDs, units,
coordinate frames, timestamps, missingness meanings and provenance before
transforming anything. A problem with constants but no dataset still needs a
parameter audit; a proved symbolic statement needs no fabricated observations.

Produce only the cleaned inputs, transformations and audit findings required for
the next calculation. Preserve exclusion IDs and reasons and counts before/after.
Define evaluation splits before fitting transformations when prediction is the
target. Validate joins and derived values against the original source.

If information is insufficient, distinguish recoverable missing input from a
non-identifiable target. Give explicit assumptions, bounds or scenarios when
they answer part of the question; do not invent data to complete a pipeline.
