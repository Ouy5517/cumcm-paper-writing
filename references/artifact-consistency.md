# Artifact consistency

Declare one authoritative_source: Markdown OR TeX OR another editable source.
Record generation commands and dependencies. Do not independently edit generated
TeX while a Markdown builder overwrites it. Authority changes require updating
the builder, README and downstream artifacts together.

Maintain input/source hashes, code revision, result files, figure dependencies,
build commands and final PDF hash in a case-local build record.
After revision recompute affected results, update the ledger, regenerate figures,
paper and code excerpts. Every included graphic must have a producing script;
captions, counts and appendix inventory must match actual files.
Run documented commands from a clean checkout with explicit dependencies.

Do not use a fixed title, figure count or total page count to validate all papers.
Count components separately according to contest-profile.yaml. Separate build,
scientific, coverage, visual and package verdicts.

Reviewed example: https://github.com/Ouy5517/student_advisor_case at commit
109929382eb53083b4dbd6f2796d0e31abbc2f97. Its Markdown/TeX divergence and outdated
figure inventory are failure examples, not patterns to reproduce.
