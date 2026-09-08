# Layout diagnosis

Load this reference only for layout/typesetting requests or observed table
walls, sparse pages, stranded headings, float, or overflow problems. Remedies
depend on the supplied CUMCM template and the observed failure; do not prescribe
universal spacing, float, or numeric layout limits. Do not use a fixed float
recipe. Do not prescribe universal numeric layout limits.

## Evidence-first workflow

1. **Compile** the current trusted source.
2. **Read log** messages before changing source.
3. **Render every page** of the resulting PDF.
4. **Create a contact sheet** to see document-level rhythm and float patterns.
5. **Inspect affected pages** at readable scale, alongside the relevant source.
6. **Diagnose** the observed cause, separating template behavior from content.
7. Make the **smallest source change** compatible with the supplied CUMCM template.
8. **Rebuild and iterate** from compilation until the observation is resolved.

## Diagnostic checklist

Check overfull/underfull content, undefined references, formula glyphs, table
walls, sparse pages, stranded headings, caption splits, float backlog,
unreadable tables, and appendix code wrapping. Also inspect headings, equations,
footers, references, and blank or overflow pages.

Use the evidence to choose a remedy: correct a source error, shorten or split a
semantically coherent table, move supporting detail to an appendix, revise a
caption, reorder nearby prose, or use only template-supported placement options.
Do not alter class/style behavior blindly, and do not treat a clean log as proof
of readable pages.
