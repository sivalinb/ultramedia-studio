# UltraMedia visual brochure

[Open the eleven-page brochure](UltraMedia-Brochure.pdf).

This landscape US Letter digital brochure introduces the product before inviting readers into its research evidence. It uses eleven custom illustrations with the creator's likeness and distinct section colors, plus selectable captions, an exact measured-results chart, internal navigation, external evidence links and two QR codes. It can also be printed as eleven pages; it is not imposed as a folded leaflet.

## Reader journey

1. **Story:** illustrated product overview with the creator's likeness throughout.
2. **Problem and solution:** scattered facts and uncertain claims become a reviewable draft.
3. **People:** four intended editorial roles, illustrated in teal.
4. **Workflow:** choose, retrieve, draft, validate and review, in blue.
5. **Data provenance:** authored research, static demo context and actual execution receipts.
6. **Factors considered:** fields, units, programmed ranges and evidence conditions.
7. **Learning:** QLoRA, merge, local serving and controlled comparison, in green.
8. **Results:** a chart generated from saved counts with preserved negative evidence.
9. **Roadmap:** current work, reliability, editor pilot and conditional expansion.
10. **Explore:** clickable resources and two vector QR codes.
11. **Sources:** twelve linked source entries, dataset identity and usage boundaries.

The [detailed source appendix](DATA_SOURCES.md) records creator, origin, purpose, licensing, exact fields, ranges, generator seed, split integrity, demo-source attribution, retrieval behavior and current coverage limits. It separates official race context from simulated athlete timing and synthetic training records.

## Evidence boundaries

The brochure pins GitHub source links to `cc8f42cbc73f6efe92c49d21437f4e4b16fd1089`, the reviewed source snapshot before brochure creation. The public demo links are live destinations and may evolve separately. This brochure does not deploy a website or host model inference.

The headline result is automatic contract success on 120 synthetic cases: 76/120 base versus 109/120 adapted, +27.5 percentage points, paired race-group bootstrap 95% interval +20 to +35 points. Both local arms use the same schema constraints. The brochure retains the 11 adapted failures, the five-probe 3/5 versus 3/5 result, the rules benchmark, the application-quality failure and incomplete human review/GPU control. It does not imply that every Week 5 agenda topic was executed.

Audience benefits are intended use cases, not measured customer outcomes. The example on page 4 and race figures in the sales artwork are illustrative, not observed race results or actual model outputs. The original personal reference photographs are excluded from this repository; only the user-requested illustrated likeness is included.

The roadmap is a proposed product sequence derived from documented gaps, not a claim of approved funding or scheduled delivery. Reliability work precedes a bounded editor pilot; integrations, hosting, RFT and distillation are conditional future options. No new model training, user research or hosting is performed by this brochure revision.

## Rebuild

Install Python packages `reportlab`, `matplotlib` and `pillow`; provide Arial regular/bold on macOS or DejaVu Sans regular/bold on Linux. Then run from the repository root:

```sh
python week5/brochure/build_illustrated_brochure.py --output week5/brochure/UltraMedia-Brochure.pdf
```

The builder uses the final PNGs in [art/](art/) without raster editing. [Final generation/edit prompts](art/final-prompts.json) and the [initial illustration briefs](art/prompts.json) record the built-in image tool workflow. The source portrait and original personal photos are not included. The earlier typeset builder supplies shared PDF helpers; the illustrated builder above is the current deliverable entry point.

Scientific plot values come from saved comparison JSON, not AI-drawn bars. PDF streams use lossless compression; original artwork is preserved. All eleven pages were rendered and visually inspected. Validation checks 88 internal navigation links, 35 external links, nonoverlapping clickable regions, source paths at the pinned commit, dataset hashes and the actual fixture counts. See [validation.json](validation.json).
