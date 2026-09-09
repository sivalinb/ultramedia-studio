# UltraMedia visual brochure

[Open the six-page brochure](UltraMedia-Brochure.pdf).

This landscape US Letter digital brochure introduces the product before inviting readers into its research evidence. It combines the approved personalized sales illustration with selectable text, vector workflow diagrams, a measured-results chart, internal navigation, external evidence links and two QR codes. It can also be printed as six pages; it is not imposed as a folded leaflet.

## Reader journey

1. **Story:** race evidence in, reviewed stories out; illustrated product overview.
2. **People:** intended users and the editorial tasks the workspace supports.
3. **Workflow:** choose, retrieve, draft, validate and review; a clearly labeled fictional example.
4. **Learning:** prompting, retrieval and fine-tuning; the synthetic dataset and completed local lifecycle.
5. **Results:** matched base/adapted comparison with uncertainty, failed cases and pending review.
6. **Explore:** demo, public evidence hub, walkthrough, full report, data provenance, training receipts, paired comparison, CSV, agenda mapping and technical visual.

## Evidence boundaries

The brochure pins GitHub source links to `cc8f42cbc73f6efe92c49d21437f4e4b16fd1089`, the reviewed source snapshot before brochure creation. The public demo links are live destinations and may evolve separately. This brochure does not deploy a website or host model inference.

The headline result is automatic contract success on 120 synthetic cases: 76/120 base versus 109/120 adapted, +27.5 percentage points, paired race-group bootstrap 95% interval +20 to +35 points. Both local arms use the same schema constraints. The brochure retains the 11 adapted failures, the five-probe 3/5 versus 3/5 result, the rules benchmark, the application-quality failure and incomplete human review/GPU control. It does not imply that every Week 5 agenda topic was executed.

Audience benefits are intended use cases, not measured customer outcomes. The example on page 3 and race figures in the sales artwork are illustrative, not observed race results or actual model outputs. The original personal reference photographs are excluded from this repository; only the user-requested illustrated likeness is included.

## Rebuild

Install Python packages `reportlab`, `matplotlib` and `pillow`; provide Arial regular/bold on macOS or DejaVu Sans regular/bold on Linux. Then run from the repository root:

```sh
python week5/brochure/build_brochure.py --output week5/brochure/UltraMedia-Brochure.pdf
```

The builder reads the approved [personalized illustration](../diagrams/ultramedia-product-pitch-siva.png). The [image-edit prompt](../diagrams/ultramedia-product-pitch-siva-prompt.txt) records how the likeness was requested. No new AI image generation is needed to rebuild the brochure.

Validation includes six-page rendering and visual review, PDF metadata/text extraction, internal/external link inspection, source-path existence at the pinned commit and numerical checks against saved reports. See [validation.json](validation.json).
