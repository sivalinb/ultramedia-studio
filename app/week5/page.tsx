'use client';

import { useState } from 'react';
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
import evidence from '@/public/data/week5-evidence.json';

export default function WeekFivePage() {
  const [selected, setSelected] = useState(0);
  const example = evidence.examples[selected];
  const audit = evidence.manifest.audit;
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
              is missing. Explore the data and run the notebook to produce the
              model comparison.
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
            </ul>
            <div className="mt-5 border-t border-white/10 pt-5 text-sm leading-6">
              <strong>GPU training and model comparison: not run.</strong>
              <p className="mt-2 text-muted-foreground">
                No adapter score or human approval is claimed. Run the notebook,
                review its outputs, and retain the evidence before making a
                quality claim.
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
              benchmark. Base-model quality, adapted quality, and editor
              preference remain unmeasured.
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
