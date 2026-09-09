'use client';

import { useState } from 'react';
import classification from '@/week5/reports/data/handout/UltraMedia-Week5-Disposition-Analysis.json';
import smoke from '@/week5/evidence/handout-smoke/summary.json';

const journey = [
  ['Prepare the data', '600 fictional examples: 400 train, 80 validation, 120 frozen test. Race groups stay separate.'],
  ['Train a small adapter', 'QLoRA changes rank-16 adapters over a frozen 4-bit Qwen base. Only completion tokens contribute to loss.'],
  ['Select and merge', 'Validation selects checkpoint 100. Verify adapter hashes, merge, and convert for local inference.'],
  ['Compare fairly', 'Use the same inputs and local JSON constraints for base and adapter. Keep every failed output.'],
  ['Put evidence before publication', 'The model drafts or asks for evidence. The app checks the output; a human editor reviews the wording.'],
];

export default function ProjectEvidence() {
  const [variant, setVariant] = useState<'base' | 'adapter'>('adapter');
  const result = classification.variants[variant];
  const [training, setTraining] = useState('0');
  const [serving, setServing] = useState('10');
  const [labor, setLabor] = useState('100');
  const [accepted, setAccepted] = useState('100');
  const entries = [training, serving, labor, accepted];
  const valid = entries.every(v => v.trim() !== '' && Number.isFinite(Number(v)) && Number(v) >= 0) && Number.isInteger(Number(accepted)) && Number(accepted) >= 1;
  const cost = valid ? (Number(training) + Number(serving) + Number(labor)) / Number(accepted) : null;
  return <section id="handout-project" className="mt-10 space-y-8" aria-label="Week 5 project guide">
    <div className="rounded-2xl border border-primary/30 bg-card p-6 sm:p-8">
      <p className="text-sm font-semibold uppercase tracking-widest text-primary">The Week 5 project</p>
      <h2 className="mt-3 text-3xl font-semibold">From race evidence to an editor’s decision</h2>
      <p className="mt-4 max-w-4xl text-base leading-7 text-muted-foreground">An editor receives scattered timing updates. UltraMedia prepares a cited draft when the facts support it and flags insufficient evidence for review. Fine-tuning teaches response behavior; current race facts stay in the request.</p>
      <div className="mt-5 flex flex-wrap gap-5 text-base text-primary">
        <a href="#adapter-application-evidence">Watch actual model execution →</a>
        <a href="#local-deployment-comparison">Inspect paired examples →</a>
        <a href="/week5/handout-project.zip" download>Download the project kit →</a>
      </div>
      <img src="/week5/week5-flow.svg" className="mt-7 hidden h-auto w-full rounded-xl md:block" alt="Week 5 flow: data preparation, QLoRA, validation, merge, comparison, and human editorial review" />
      <ol className="mt-6 space-y-4 md:hidden">{journey.map(([title, detail], i) => <li key={title} className="border-l-2 border-primary/50 pl-4"><p className="text-base font-semibold">{i + 1}. {title}</p><p className="mt-1 text-base leading-7 text-muted-foreground">{detail}</p></li>)}</ol>
      <a href="/week5/week5-flow.svg" target="_blank" rel="noreferrer" className="mt-4 inline-block text-base text-primary">Open or save the full flow diagram →</a>
    </div>

    <details className="rounded-2xl border border-white/10 bg-card p-6">
      <summary className="cursor-pointer text-xl font-semibold">Watch the recorded project walkthrough</summary>
      <p className="mt-4 text-base leading-7 text-muted-foreground">A silent recording of the actual page: inspect the flow, switch base and adapted results, see all five probe outcomes, and explore cost assumptions. This is a recorded UI walkthrough. The separate Loom submission is still pending.</p>
      <video className="mt-5 w-full rounded-xl" controls preload="metadata" poster="/week5/project-walkthrough-poster.png" aria-label="Silent recorded Week 5 project walkthrough">
        <source src="/week5/project-walkthrough.webm" type="video/webm" />
        <a href="/week5/project-walkthrough.webm">Download the recorded walkthrough</a>
      </video>
    </details>
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="rounded-2xl border border-white/10 bg-card p-6">
        <h3 className="text-2xl font-semibold">When should the model draft?</h3>
        <p className="mt-3 text-base leading-7 text-muted-foreground">A direct match to the handout’s classification exercise: two output classes, measured on 120 saved local cases. The race signal is supplied as input.</p>
        <div className="my-5 grid grid-cols-2 gap-3">
          {(['base', 'adapter'] as const).map(v => <button key={v} type="button" aria-pressed={variant === v} onClick={() => setVariant(v)} className={`rounded-lg border px-4 py-3 text-base ${variant === v ? 'border-primary bg-primary/15 text-primary' : 'border-white/20'}`}>{v === 'base' ? 'Base model' : 'Fine-tuned model'}</button>)}
        </div>
        <p className="text-3xl font-semibold" aria-live="polite">{(result.accuracy * 100).toFixed(1)}% decision accuracy</p>
        <p className="mt-2 text-base text-muted-foreground">Macro F1: {result.macro_f1.toFixed(4)} · all 120 cases included</p>
        <div className="mt-5 overflow-x-auto">
          <table className="w-full text-left text-base"><caption className="mb-3 text-left text-sm text-muted-foreground">Confusion matrix: rows = reference, columns = prediction</caption><thead><tr><th className="p-2">Reference</th><th className="p-2">Draft</th><th className="p-2">Hold</th></tr></thead><tbody>{['Draft', 'Insufficient evidence'].map((label, i) => <tr key={label}><th scope="row" className="p-2 font-normal">{label}</th>{result.confusion_matrix[i].slice(0, 2).map((n, j) => <td key={j} className={`border border-background p-4 text-center text-2xl ${i === j ? 'bg-primary/15 text-primary' : 'bg-amber-300/10 text-amber-200'}`}>{n}</td>)}</tr>)}</tbody></table>
        </div>
        <p className="mt-4 text-base leading-7 text-muted-foreground">The adapter makes 11 unnecessary holds and no unsupported draft decisions on the 48 cases requiring abstention. This small synthetic sample does not establish zero risk.</p>
        <p className="mt-3 text-base leading-7"><strong>+7.5 points</strong> in decision accuracy; <strong>+27.5 points</strong> in passing all nine checks. These are different measures.</p>
        <a className="mt-4 inline-block text-base text-primary" href="/week5/DISPOSITION_RESULTS.md">Read precision, recall, F1 and limitations →</a>
      </div>
      <div className="rounded-2xl border border-white/10 bg-card p-6">
        <h3 className="text-2xl font-semibold">Five new task-level probes</h3>
        <p className="mt-3 text-base leading-7 text-muted-foreground">Position loss, projected record, missing evidence, contradictory pace, and a misleading hint. These first attempts use the existing models and unchanged prompts.</p>
        <div className="mt-5 grid grid-cols-3 gap-3">{(['rules', 'base', 'adapter'] as const).map(v => <div key={v} className="rounded-xl bg-white/5 p-4"><p className="text-sm capitalize text-muted-foreground">{v}</p><p className="mt-2 text-3xl font-semibold">{smoke.reports[v].passed}/5</p></div>)}</div>
        <p className="mt-5 text-base leading-7 text-amber-200">No adapter advantage in these five probes. The adapter invents a citation on empty evidence and unnecessarily holds a supported update under a misleading hint. Both failures remain in the results.</p>
        <p className="mt-3 text-base leading-7 text-muted-foreground">Some passing outputs still have awkward wording or ambiguous direction. Software checks do not replace an editor’s assessment of meaning.</p>
        <a className="mt-5 inline-block text-base text-primary" href="/week5/HANDOUT_SMOKE_RESULTS.md">Inspect every outcome and raw evidence →</a>
        <div className="mt-6 border-t border-white/10 pt-5"><h4 className="text-lg font-semibold">Why use fine-tuning?</h4><p className="mt-3 text-base leading-7 text-muted-foreground">Rules already pass 120/120 engineered benchmark cases. Keep rules for the structured decision. Use the adapted model as a research candidate until editors demonstrate better wording or less correction effort.</p></div>
      </div>
    </div>

    <details className="rounded-2xl border border-white/10 bg-card p-6">
      <summary className="cursor-pointer text-xl font-semibold">Explore a cost scenario</summary>
      <p className="mt-4 text-base leading-7 text-muted-foreground">Hypothetical amounts in your chosen currency, for one consistent workload. These defaults are examples, not measured spending or provider prices. Include retries in serving and labor. Human acceptance and correction effort have not been measured.</p>
      <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{[['Amortized training cost', training, setTraining], ['Serving cost, all attempts', serving, setServing], ['Editor labor cost', labor, setLabor], ['Accepted briefs', accepted, setAccepted]].map(([label, value, setter]) => <label key={label as string} className="text-base">{label as string}<input className="mt-2 w-full rounded-lg border border-white/25 bg-background p-3" type="number" min="0" step="any" value={value as string} onChange={event => (setter as (v: string) => void)(event.target.value)} /></label>)}</div>
      <p className="mt-5 text-xl font-semibold" aria-live="polite">{cost === null ? 'Enter nonnegative costs and a whole number of accepted briefs, at least one.' : `${cost.toFixed(2)} per accepted brief — hypothetical`}</p>
      <a className="mt-3 inline-block text-base text-primary" href="/week5/BUSINESS_CASE.md">Read the business decision and accounting limits →</a>
    </details>
    <div className="rounded-2xl border border-amber-300/25 bg-amber-300/5 p-6"><h3 className="text-xl font-semibold">Submission status</h3><p className="mt-3 text-base leading-7">The custom route uses GitHub assets plus a Loom video. The project kit includes a timed walkthrough script and a blank blind-review packet. Loom recording, actual human review and form submission are pending. The final explicit-schema GPU control awaits recovery after interruption.</p><p className="mt-3 text-base text-muted-foreground">Handout deadline: September 13, 2026, 11:59 p.m. PT. Human review is our production gate; it is separate from the handout’s submission instructions.</p><a className="mt-4 inline-block text-base text-primary" href="/week5/DEMO_AND_SUBMISSION.md">Open the demo script and submission checklist →</a></div>
  </section>;
}
