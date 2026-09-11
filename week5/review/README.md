# Complete the remaining evidence

## Blind editorial pilot

Status: packet prepared; **zero human reviews completed**. The PDF contains the existing five fictional probes and 15 saved outputs unchanged. It does not contain the assignment key or automatic scores. These authored probes are not representative race data.

1. Give each reviewer a separate copy of `UltraMedia-Blind-Editorial-Review.pdf`. Two independent race-media editors or experienced race volunteers are preferred. The founder may participate, with founder feedback reported separately. Do not send reports or assignment keys with the packet.
2. Reviewers fill every case and candidate, save, reopen to check fields, and return the file privately. Training consent defaults false. Review text is not automatically added to training data.
3. Keep identities, filled PDFs, and free-text responses outside the repository. Verify the responses came from the named humans. Record receipt time and SHA256 privately and lock responses before unblinding.
4. Run `python week5/review/collect_reviews.py /private/location/reviewer1.pdf /private/location/reviewer2.pdf --output /private/location/aggregate.json`. Dependencies: `pypdf`; builder also requires `reportlab`.
5. Inspect disagreements and every unsupported answer. The collector validates completeness, not identity or truth. It emits anonymous descriptive totals grouped by self-reported reviewer role. Inspect aggregates for privacy before publication. Do not claim a model winner from pooled A/B/C letters: assignments vary across cases. A separate operator may join the private assignment key after responses are locked.

Rebuild with `python week5/review/build_packet.py week5/review/UltraMedia-Blind-Editorial-Review.pdf`. Never edit saved outputs to improve the review results. See [original protocol](../project/HUMAN_REVIEW.md).

## Permissioned historical replay

Status: **no historical records ingested and no historical replay run**. `historical-case-template.json` is a blank intake record, not evidence. Obtain at least 30 fresh, rights-cleared cases from actual checkpoint timing exports and corresponding official race updates. A public URL alone is not permission to reuse or publish personal data. Keep raw records private until permissions and minimization are confirmed.

Suggested coverage: ordinary progress, position losses, projections, missing/stale records, contradictory timing, and misleading hints. Include multiple athletes and race editions; keep each race/athlete group out of training. Deduplicate before splitting and freeze the test set before inference. Have a race-domain reviewer specify supported facts, required holds and unacceptable claims independently of model outputs.

For each case record the exact source URL/export reference, retrieval time, observed time/timezone, permission basis, transformations, missing values, conflicts, expected behavior, and source checksum. Do not invent missing values. Evaluate rules, base and adapter with matched prompts, decoding and evidence; capture raw outputs, failures, latency, hardware and cost receipts. Use blind human review and report denominators and disagreements. Thirty cases remain a small pilot, not proof of safe autonomous publishing.

## GPU comparison recovery

The original QLoRA training is complete. The separate explicit-schema control has a saved base arm (36/120 automatic passes); its adapted arm was interrupted. Recovery should reuse the pinned adapter and unchanged base receipts, run only the missing arm, and verify hashes. Do not replace it with the local Q4 result, retrain, or select a new prompt after seeing test failures. Record the cross-runtime comparison limitation.

On September 11 a T4 was allocated, but automatic approval review blocked even the reduced upload pending explicit user approval of the adapter/code/synthetic-data/results transfer to Colab. The idle T4 was released to conserve quota. GPU results remain pending. No paid GPU purchase is authorized. Completed results, when available, must pass `week5/scripts/verify_gpu_run.py RUN --schema-control` before reports or public claims are updated.
