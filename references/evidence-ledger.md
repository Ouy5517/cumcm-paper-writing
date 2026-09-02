# Claim-evidence and reproducibility ledger

Use one row for every material result or conclusion:

| ID | Claim | Evidence/source | Derivation/code location | Scope/boundary | Status | Paper location |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | [bounded claim] | [data/figure/equation/citation] | [file/function/cell] | [population/assumption] | VERIFIED / UNVERIFIED / AUTHOR_INPUT_NEEDED | [section] |

Rules:

- Contest-provided raw data is not a citation; state its provenance in the
  data description and cite external/public data separately.
- A derived number is VERIFIED only when its inputs, transformation, and
  calculation can be reproduced or manually checked.
- A model assumption is not evidence. Label it and explain its consequence.
- Code, figures, tables, abstract, and conclusion must agree on names, units,
  rounding, sample scope, and result values.
- Cite the source where the definition, method, dataset, or external fact is
  used, then include the same item in the reference list.
- If evidence is missing, write [AUTHOR_INPUT_NEEDED: evidence for ...] or
  [待补：...] and do not escalate the claim.
