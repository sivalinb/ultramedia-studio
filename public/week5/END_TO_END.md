# End-to-end demonstration and independent verification

The public Week 5 page presents recorded evidence. A connected local Race Desk can also run an actual open-source model, retrieve source context, validate its numeric claims, and persist versioned editorial decisions. These are distinct demonstrations; a static website does not host a GPU model.

## Local inference option

The verified setup uses an Apple M1 Max with 64 GiB memory, the llama.cpp server bundled with official Ollama 0.33.3, and the public `qwen3:4b-instruct` Q4_K_M model. The downloaded model SHA-256 is `85e4a5b7b8ef0e48af0e8658f5aaab9c2324c76c1641493f4d1e25fce54b18b9`. This proves local serving of an unadapted model; it is not the NF4 QLoRA comparison or proof that an arbitrary GGUF has the exact training-base lineage.

Start a compatible llama.cpp server with that model, keeping it bound to loopback:

```bash
llama-server --model /path/to/qwen3-4b-instruct-q4_k_m.gguf \
  --alias qwen3:4b-instruct --host 127.0.0.1 --port 8080 \
  --ctx-size 8192 --n-gpu-layers 99
```

Install the Python API and use a separate synthetic QA database. Set `PROVIDER_MODE=llamacpp`, `LLAMACPP_BASE_URL=http://127.0.0.1:8080`, `LLAMACPP_MODEL=qwen3:4b-instruct`, and `APPROVAL_API_KEY` to a private test credential. Run the API on 127.0.0.1:8000, then start the frontend with `NEXT_PUBLIC_ULTRAMEDIA_API_URL=http://127.0.0.1:8000 npm run dev`. Keep that local URL out of the public production build.

The local provider uses the exact JSON schema for constrained decoding and a separately versioned serving prompt. The prompt says to repeat supplied numeric values rather than compute new quantities. Generation records retain that prompt version. Invalid outputs remain errors; there is no silent substitution of rule-generated text.

## Reproduce the browser checks

Use only an isolated synthetic API database: this test intentionally creates drafts and simulated review decisions.

```bash
npm ci --registry=https://registry.npmjs.org
npx playwright install chromium
E2E_REVIEWER_KEY_FILE=/path/to/private-test-key.txt npm run test:e2e
```

Optional configuration: `E2E_SITE_URL`, `E2E_API_URL`, `E2E_EXPECTED_PROVIDER`, and `E2E_OUTPUT_DIR`. The defaults target the local setup above. Artifacts are saved under `week5/runs/e2e-<timestamp>`; this folder is excluded from source packages. The test records JSON receipts, desktop/mobile screenshots and browser video. Reviewer credentials are excluded from reports and masked in the UI.

Coverage includes browser-to-API generation using the real provider, all six workflow stages, pending-review persistence, credential rejection, unsupported numeric-edit rejection, training-consent rights requirements, revision history, stale-revision conflicts, missing-athlete rejection, the workflow-check action, mobile layout, and notebook/dataset/submission downloads. Simulated test approvals **do not count as human editorial review** and have training consent disabled.

## What the real tests uncovered

1. Plain JSON mode did not guarantee the contract: the model emitted `numeric_value` instead of `value`. Local serving now uses schema-constrained decoding.
2. A schema-valid draft mentioned an unsupported 6.3-mile segment. Validation correctly rejected it. The local serving prompt now explicitly prohibits new numeric derivations; the validator was not weakened.
3. Wrapped textarea content polluted the field's accessible label. Explicit label references now give assistive technology and browser tests stable field names.

4. The workflow-check endpoint previously returned an HTTP 500 when a model output violated the contract. It now returns the complete FAIL report, retains both failed cases, and includes failures in every applicable denominator. A regression test verifies this behavior.

The recorded browser run passed **13 software checks** and the Python suite passed **33 tests**. The independent local-model workflow check passed its four retrieval cases but failed both generation cases. This is a model-quality failure, not a passing release: the model still sometimes derives unsupported numbers despite the serving prompt. A separate successful browser draft and its revisions survived an actual API restart. All approvals in these tests are automated fixtures, with training consent disabled.

The original failed probes are retained alongside the software evidence. These findings also motivated the separately predeclared [stronger GPU prompt control](SCHEMA_CONTROL.md), which must be reported independently of local constrained decoding.

## Three-minute demonstration

1. Open `/week5` and explain the behavior-versus-knowledge split. Inspect one supported and one missing-evidence training example.
2. Show the recorded experiment status, actual base/adapted results when available, and the stronger prompt-only control. Open a failure as well as a successful case.
3. Show the local Race Desk recording or run it locally: generate a draft, inspect citations and the six-stage trace, try an unsupported numeric edit, then save a clearly labeled synthetic test revision.
4. Open the downloadable evidence and reproduction instructions. Explain the limits of synthetic data and why human review still blocks model promotion.

Award selection is not a software test. This package is designed to make the implementation, tradeoffs, failures, and measured evidence easy to assess.
