'use client';

import { useState } from 'react';
import ComparisonEvidence, { type RecordedComparison } from './ComparisonEvidence';
import Link from 'next/link';
import {
  ArrowLeft,
  ArrowDownToLine,
  Database,
  FlaskConical,
  ShieldCheck,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import evidence from '@/week5/evidence/site-snapshot.json';

type ModelComparison = {
  status: string;
  base_model_score: number | null;
  adapter_score: number | null;
  training?: {
    base_model: string;
    training_seconds: number;
    trainable_parameters: number;
    peak_allocated_vram_bytes: number;
    environment: { gpu: string };
  };
  results?: {
    base: { cases: number; metrics: Record<string, number> };
    adapter: { cases: number; metrics: Record<string, number> };
    automatic_success_delta: number;
    paired_group_bootstrap_95_interval: number[];
  };
};

type LocalServing = {
  status: string;
  model: string;
  runtime: string;
  hardware: string;
  browser_checks_passed: number;
  generation_seconds: number;
  model_workflow_decision: string;
  failed_model_cases: number;
};

const learningMap = [
  ['Behavior vs. knowledge', 'Learn drafting and abstention; keep race facts in supplied evidence.', 'Dataset examples and saved evidence packs'],
  ['SFT and tokenization', 'Train only assistant completions and verify sequence lengths.', 'Notebook, tokenizer audit and loss-mask receipt'],
  ['LoRA / QLoRA', 'Train rank-16 adapters over a frozen NF4 base model.', 'Training configuration, adapter hashes and GPU memory'],
  ['Data quality and overfitting', 'Separate race groups and select checkpoints by validation loss.', '400 / 80 / 120 split, overlap checks and loss curves'],
  ['Prompting before training', 'Test an explicit-schema prompt on both base and adapted models.', 'Predeclared stronger prompt control'],
  ['Evaluation', 'Keep failed generations in the denominator and inspect regressions.', 'Raw predictions, nine checks and paired uncertainty interval'],
  ['Local models and serving', 'Run an open-source GGUF model through the actual Race Desk.', 'Browser test report, source citations, traces and demo recording'],
  ['Model cards and release decisions', 'Record lineage and limits; keep human review separate.', 'Data card, serving guide and pending human review'],
];

export default function WeekFivePage() {
  const [selected, setSelected] = useState(0);
  const example = evidence.examples[selected];
  const audit = evidence.manifest.audit;
  const model = evidence.model_comparison as ModelComparison;
  const completed = model.status === 'completed' && model.results && model.training;
  const comparisons = (evidence as typeof evidence & { comparisons?: RecordedComparison[] }).comparisons ?? [];
  const trainingCompleted = (evidence as typeof evidence & { training_completed?: boolean }).training_completed;
  const strongerControlPending = completed && !comparisons.some(item => item.id === 'stronger-prompt-control');
  const local = (evidence as typeof evidence & { local_serving?: LocalServing }).local_serving;
  const adapterDemo = (evidence as typeof evidence & { adapter_serving?: { browser_checks_passed: number; failed_model_cases: number } }).adapter_serving;
  return (
    <main className="min-h-screen bg-background text-foreground">
      <header className="border-b border-white/10">
        <nav className="mx-auto flex max-w-7xl flex-wrap items-center gap-6 px-6 py-5 text-sm">
          <Link href="/" className="flex items-center gap-2">
            <ArrowLeft size={18} /> UltraMedia
          </Link>
          <Link href="/studio">Race desk</Link>
          <Link href="/observability">Observability</Link>
          <Badge variant="outline" className="ml-auto">
            Week 5 · research submission
          </Badge>
        </nav>
      </header>
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_340px]">
          <div>
            <p className="mb-3 text-sm uppercase tracking-widest text-primary">
              Evidence-grounded editorial specialization
            </p>
            <h1 className="max-w-3xl text-4xl font-semibold leading-tight sm:text-5xl">
              Teach the writing.
              <br />
              Keep the facts in evidence.
            </h1>
            <p className="mt-6 max-w-3xl text-base leading-7 text-muted-foreground">
              A reproducible QLoRA experiment for race reporting: consistent
              drafts, cited numeric claims, and a clear response when evidence
              is missing. Explore the data, the experiment, and its recorded evidence.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <a
                className="inline-flex items-center gap-2 rounded-full bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground"
                href="/week5/UltraMedia_Week5_QLoRA.ipynb"
                download
              >
                <ArrowDownToLine size={18} /> Colab / Kaggle notebook
              </a>
              <a
                className="rounded-full border border-white/20 px-5 py-3 text-sm"
                href="/week5/synthetic-dataset.zip"
                download
              >
                Download dataset
              </a>
              <a
                className="rounded-full border border-white/20 px-5 py-3 text-sm"
                href="/week5/SUBMISSION.md"
                download
              >
                Submission guide
              </a>
            </div>
          </div>
          <aside className="rounded-2xl border border-amber-300/25 bg-amber-300/5 p-6">
            <h2 className="text-lg font-semibold text-amber-200">
              What has run
            </h2>
            <ul className="mt-4 space-y-3 text-sm leading-6">
              <li>Dataset generation and automatic validation</li>
              <li>Deterministic held-out contract evaluation</li>
              <li>Tokenizer length audit and software tests</li>
              {local?.status === 'verified' && <li>Local open-source model and browser-to-API workflow</li>}
              {trainingCompleted && <li>QLoRA training: 100 steps, both validation epochs recorded</li>}
              {comparisons.map(item => <li key={item.id}><a className="text-primary" href={'#' + item.id}>{item.title}: 120 cases per model</a></li>)}
            </ul>
            <div className="mt-5 border-t border-white/10 pt-5 text-sm leading-6">
              <strong>{strongerControlPending ? 'Original GPU comparison complete. Stronger prompt control pending.' : completed ? 'GPU comparisons complete. Human review pending.' : 'Completed GPU comparison: pending.'}</strong>
              <p className="mt-2 text-muted-foreground">
                {completed
                  ? 'The scores below measure automatic structured checks. Interpret the original result alongside the stronger shared-schema prompt control. Editorial quality and real-race generalization still require human review.'
                  : 'The verified local comparison is reported separately below. GPU prompt controls and human editorial review remain pending.'}
              </p>
            </div>
          </aside>
        </div>
        <section className="my-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            ['Synthetic examples', audit.rows],
            [
              'Independent race groups',
              Object.values(audit.group_counts).reduce((a, b) => a + b, 0),
            ],
            ['Shared groups across splits', 0],
            ['Human-approved examples', audit.human_approved],
          ].map(([label, value]) => (
            <div
              key={String(label)}
              className="rounded-2xl border border-white/10 bg-card p-6"
            >
              <p className="text-3xl font-semibold text-primary">{value}</p>
              <p className="mt-2 text-sm text-muted-foreground">{label}</p>
            </div>
          ))}
        </section>
        <section className="grid gap-6 lg:grid-cols-2">
          <article className="rounded-2xl border border-white/10 bg-card p-6">
            <h2 className="mb-4 flex items-center gap-2 text-xl font-semibold">
              <Database size={20} /> Dataset contract
            </h2>
            <div
              className="flex gap-1 overflow-hidden rounded-xl"
              aria-label="Training 400; validation 80; test 120"
            >
              <div
                className="bg-primary p-3 text-center text-sm font-semibold text-primary-foreground"
                style={{ width: '66.67%' }}
              >
                Train · 400
              </div>
              <div
                className="bg-sky-300 p-3 text-center text-sm text-sky-950"
                style={{ width: '13.33%' }}
              >
                80
              </div>
              <div
                className="bg-violet-300 p-3 text-center text-sm text-violet-950"
                style={{ width: '20%' }}
              >
                120
              </div>
            </div>
            <p className="mt-4 text-sm leading-6 text-muted-foreground">
              400 train, 80 validation, 120 test. Four signal types and five
              evidence conditions. Every race episode stays in one split. Shared
              templates remain a limitation; this corpus does not prove
              real-race generalization.
            </p>
            <a
              href="/week5/DATA_CARD.md"
              className="mt-4 inline-block text-sm text-primary"
              download
            >
              Read provenance and limitations →
            </a>
          </article>
          <article className="rounded-2xl border border-white/10 bg-card p-6">
            <h2 className="mb-4 flex items-center gap-2 text-xl font-semibold">
              <FlaskConical size={20} /> Measured baseline
            </h2>
            <p className="text-3xl font-semibold">
              {evidence.deterministic?.cases ?? 0} contract cases
            </p>
            <p className="mt-4 text-sm leading-6 text-muted-foreground">
              The deterministic rule baseline passes the stored structured
              checks. This checks code and fixture behavior; it is not an LLM
              benchmark. {completed ? 'The measured model comparison appears below; editor preference remains unmeasured.' : 'Model performance and editor preference remain unmeasured.'}
            </p>
            <a
              href="/data/week5-evidence.json"
              className="mt-4 inline-block text-sm text-primary"
              download
            >
              Download the evidence snapshot →
            </a>
          </article>
        </section>
        <section className="mt-10 rounded-2xl border border-white/10 bg-card p-6" id="week5-learning-map">
          <h2 className="text-2xl font-semibold">Week 5 learning → implementation → evidence</h2>
          <p className="mt-3 text-base leading-7 text-muted-foreground">
            The course&apos;s SFT workflow is applied to evidence-grounded race reporting.
            The execution status above distinguishes completed checks from pending experiments.
          </p>
          <div className="mt-5 overflow-x-auto">
            <table className="w-full min-w-[620px] text-left text-sm">
              <thead><tr className="border-b border-white/15">
                <th className="py-3 pr-4">Learning</th><th className="px-4 py-3">Implementation</th><th className="px-4 py-3">Where to inspect it</th>
              </tr></thead>
              <tbody>{learningMap.map(([concept, implementation, artifact]) => (
                <tr key={concept} className="border-b border-white/10 align-top">
                  <th className="py-4 pr-4 font-medium">{concept}</th>
                  <td className="px-4 py-4 leading-6 text-muted-foreground">{implementation}</td>
                  <td className="px-4 py-4 leading-6">{artifact}</td>
                </tr>
              ))}</tbody>
            </table>
          </div>
          <div className="mt-5 flex flex-wrap gap-5 text-sm text-primary">
            <a href="/week5/SCHEMA_CONTROL.md" download>Read the prompt-control plan →</a>
            <a href="/week5/END_TO_END.md" download>Reproduce the end-to-end demo →</a>
          </div>
        </section>
        {local?.status === 'verified' && (
          <section className="mt-10 rounded-2xl border border-primary/25 bg-card p-6" id="local-model-demo">
            <h2 className="text-2xl font-semibold">A real local-model workflow</h2>
            <p className="mt-3 text-base leading-7 text-muted-foreground">
              {local.model} on {local.hardware}. The browser generated a draft through
              the Python API, retrieved source evidence, checked the output, and saved a versioned review.
            </p>
            <dl className="mt-5 grid gap-4 sm:grid-cols-3">
              <div><dt className="text-sm text-muted-foreground">End-to-end software checks</dt><dd className="mt-1 text-xl font-semibold">{local.browser_checks_passed} passed</dd></div>
              <div><dt className="text-sm text-muted-foreground">Recorded generation request</dt><dd className="mt-1 text-xl font-semibold">{local.generation_seconds.toFixed(1)} seconds</dd></div>
              <div><dt className="text-sm text-muted-foreground">Additional model workflow check</dt><dd className="mt-1 text-xl font-semibold">{local.model_workflow_decision} · {local.failed_model_cases} failed model cases</dd></div>
            </dl>
            <p className="mt-5 text-sm leading-6 text-muted-foreground">
              The software checks include rejecting unsupported edits and reporting model failures.
              Passing those checks does not mean every model response was correct. This local base-model
              demonstration is separate from the QLoRA comparison; the public page presents recorded execution.
            </p>
            <video className="mt-6 aspect-[1280/900] w-full rounded-xl border border-white/10 object-cover object-top" controls preload="none"
              poster="/week5/local-demo-poster.png" aria-label="Recorded local Race Desk end-to-end test">
              <source src="/week5/local-demo.webm" type="video/webm" />
              <a href="/week5/local-demo.webm">Download the demo recording</a>
            </video>
            <p className="mt-3 text-sm text-amber-200">Review actions in this recording are automated synthetic test fixtures. Human editorial review remains pending.</p>
            <div className="mt-5 flex flex-wrap gap-5 text-sm text-primary">
              <a href="/week5/local-serving-evidence.zip" download>Download test reports, outputs, traces and screenshots →</a>
              <a href="/week5/END_TO_END.md" download>Run the demo yourself →</a>
            </div>
          </section>
        )}
        <section className="mt-10 rounded-2xl border border-white/10 p-6">
          <h2 className="text-2xl font-semibold">Detailed fine-tuning reports</h2>
          <p className="mt-3 text-base leading-7 text-muted-foreground">Read the data inventory, training configuration and loss curves, experiment flow diagrams, full predictions, failure analysis and reproducibility receipts. Completed measurements and pending work are labeled in each report.</p>
          <div className="mt-4 flex flex-wrap gap-6 text-sm text-primary">
            <a href="https://github.com/sivalinb/ultramedia-studio/tree/codex/week5-submission/week5/reports">Read reports on GitHub →</a>
            <a href="/week5/fine-tuning-reports.zip" download>Download reports and data →</a>
          </div>
        </section>
        {comparisons.filter(item => item.id === 'stronger-prompt-control').map(item => <ComparisonEvidence key={item.id} comparison={item} />)}
        {completed && model.results && model.training && (
          <section className="mt-10 rounded-2xl border border-primary/25 bg-card p-6">
            <h2 className="text-2xl font-semibold">Completed training and original comparison</h2>
            <p className="mt-3 text-base leading-7 text-muted-foreground">
              {model.training.base_model} · {model.training.environment.gpu} ·{' '}
              {model.results.base.cases} held-out cases per model. Both variants use
              the same model revision, evidence, prompt, quantization, and decoding limits.
            </p>
            <dl className="mt-6 grid gap-4 text-sm sm:grid-cols-3">
              <div><dt className="text-muted-foreground">Trainable adapter parameters</dt>
                <dd className="mt-1 text-lg font-semibold">{model.training.trainable_parameters.toLocaleString('en-US')}</dd></div>
              <div><dt className="text-muted-foreground">Recorded training invocation</dt>
                <dd className="mt-1 text-lg font-semibold">{(model.training.training_seconds / 60).toFixed(1)} minutes</dd></div>
              <div><dt className="text-muted-foreground">Peak allocated GPU memory</dt>
                <dd className="mt-1 text-lg font-semibold">{(model.training.peak_allocated_vram_bytes / 1024 ** 3).toFixed(2)} GiB</dd></div>
            </dl>
            <img className="mt-6 h-auto w-full rounded-xl" src="/week5/measured-results.png"
              width={1920} height={640} alt="Recorded training and validation loss, and the base-versus-adapter automatic checks" />
            <div className="mt-5 flex flex-wrap gap-6 text-sm text-primary">
              <a href="/week5/gpu-evidence.zip" download>Download run logs, predictions, reports, and review forms →</a>
              <a href="/week5/measured-results.png" download>Download measured results plot →</a>
            </div>
            <p className="mt-4 text-sm leading-6 text-amber-200">
              Human editorial review is pending. This research run does not promote a model to production.
            </p>
          </section>
        )}
        {comparisons.filter(item => item.id !== 'stronger-prompt-control').map(item => <ComparisonEvidence key={item.id} comparison={item} />)}
        {adapterDemo && <section className="mt-10 rounded-2xl border border-primary/25 bg-card p-6" id="adapter-application-evidence">
          <h2 className="text-2xl font-semibold">The fine-tuned model in the Race Desk</h2>
          <p className="mt-3 text-base leading-7 text-muted-foreground">The actual trained adapter was merged, converted and served locally. All {adapterDemo.browser_checks_passed} browser software checks passed, including generation, citations, protected review, saved revisions and mobile behavior.</p>
          <p className="mt-3 text-base leading-7 text-amber-200">The separate model-quality suite still reports FAIL: {adapterDemo.failed_model_cases} generation case failed. Its record-watch response omitted the requested metric and made the wrong draft decision. The application rejected the output.</p>
          <video className="mt-5 w-full rounded-xl border border-white/10" controls preload="metadata" poster="/week5/adapter-demo-poster.png" aria-label="Actual fine-tuned model browser workflow recording">
            <source src="/week5/adapter-demo.webm" type="video/webm" />
          </video>
          <a href="/week5/adapter-serving-evidence.zip" download className="mt-5 inline-block text-sm text-primary">Download adapted-model test reports, traces and raw outputs →</a>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">Review actions in this recording are automated synthetic QA with training consent disabled. Human editorial review and production model promotion remain pending.</p>
        </section>}
        <section className="mt-10 rounded-2xl border border-white/10 bg-card p-6">
          <h2 className="text-2xl font-semibold">Inspect a training example</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            These examples come only from the training split. Source
            measurements and reference responses are visible together;
            targets have not been human-approved.
          </p>
          <div className="my-5 flex flex-wrap gap-2">
            {evidence.examples.map((row, index) => (
              <Button
                variant={selected === index ? 'default' : 'outline'}
                size="sm"
                key={row.id}
                aria-pressed={selected === index}
                onClick={() => setSelected(index)}
              >
                {row.inputs.moment.signal_type.replaceAll('_', ' ')} ·{' '}
                {row.provenance.condition.replaceAll('_', ' ')}
              </Button>
            ))}
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            <article>
              <h3 className="mb-3 text-lg font-semibold">
                Evidence supplied to the model
              </h3>
              {example.inputs.evidence.map((item) => (
                <div
                  key={item.id}
                  className="mb-3 rounded-xl border border-white/10 p-4"
                >
                  <p className="text-sm leading-6">{item.excerpt}</p>
                  <code className="mt-2 block break-all text-xs text-muted-foreground">
                    {item.id}
                  </code>
                </div>
              ))}
              <p className="mt-4 text-sm leading-6 text-muted-foreground">
                Headline hint: {example.inputs.moment.headline_hint}
              </p>
            </article>
            <article className="rounded-xl bg-black/20 p-5">
              <Badge variant="outline">
                {example.output.disposition.replaceAll('_', ' ')}
              </Badge>
              <h3 className="mt-4 text-xl font-semibold">
                {example.output.headline}
              </h3>
              <p className="mt-4 text-base leading-7 text-muted-foreground">
                {example.output.body}
              </p>
              {example.output.reason && (
                <p className="mt-4 text-sm text-amber-200">
                  {example.output.reason}
                </p>
              )}
              <details className="mt-5 text-sm">
                <summary className="cursor-pointer text-primary">
                  Full target contract
                </summary>
                <pre className="mt-3 overflow-auto whitespace-pre-wrap break-words text-xs">
                  {JSON.stringify(example.output, null, 2)}
                </pre>
              </details>
            </article>
          </div>
        </section>
        <section className="mt-10 rounded-2xl border border-primary/20 bg-primary/5 p-6">
          <h2 className="flex items-center gap-2 text-xl font-semibold">
            <ShieldCheck size={20} /> From research to the newsroom
          </h2>
          <p className="mt-3 max-w-4xl text-base leading-7 text-muted-foreground">
            Run the frozen base-versus-adapter comparison, inspect failures, and
            complete blind editorial review. Synthetic training alone cannot
            promote a model. Corrected, consenting editor examples have their
            own export path and preserve the original evidence and every
            revision.
          </p>
          <div className="mt-5 flex flex-wrap gap-6 text-sm text-primary">
            <Link href="/studio">Open the editorial workflow →</Link>
            <a href="/week5/EVALUATION.md" download>
              Evaluation protocol →
            </a>
            <a href="/week5/SERVING.md" download>
              Serving and rollback →
            </a>
          </div>
        </section>
      </div>
    </main>
  );
}
