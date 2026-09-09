'use client';

import { useState } from 'react';

type Prediction = { raw_output: string | null; metrics: Record<string, boolean>; error_type?: string };
export type RecordedComparison = {
  id: string;
  title: string;
  description: string;
  download: string;
  results: {
    base: { cases: number; metrics: Record<string, number>; latency_ms: { p50: number; p95: number } };
    adapter: { cases: number; metrics: Record<string, number>; latency_ms: { p50: number; p95: number } };
    automatic_success_delta: number;
    paired_group_bootstrap_95_interval: number[];
  };
  examples: { id: string; signal: string; condition: string; inputs: unknown; base: Prediction; adapter: Prediction }[];
};

const labels: Record<string, string> = {
  schema_valid: 'Valid output format', citation_ids_valid: 'Valid citation IDs',
  structured_claims_supported: 'Supported structured claims', required_metric_covered: 'Required metric covered',
  disposition_correct: 'Correct draft or abstention decision', numeric_tokens_supported: 'Supported numeric tokens',
  sensitive_language_absent: 'Selected sensitive-language checks', projection_not_achievement: 'Projection kept distinct from achievement',
  automatic_success: 'All automatic checks passed',
};

export default function ComparisonEvidence({ comparison }: { comparison: RecordedComparison }) {
  const [selected, setSelected] = useState(0);
  const example = comparison.examples[selected];
  const result = comparison.results;
  return <section className="mt-10 min-w-0 rounded-2xl border border-primary/25 bg-card p-6" id={comparison.id}>
    <h2 className="text-2xl font-semibold">{comparison.title}</h2>
    <p className="mt-3 text-base leading-7 text-muted-foreground">{comparison.description}</p>
    <div className="mt-5 overflow-x-auto">
      <table className="w-full min-w-[470px] text-left text-sm">
        <thead><tr className="border-b border-white/15"><th className="py-3 pr-4">Automatic check</th><th className="p-3">Base model</th><th className="p-3">With adapter</th></tr></thead>
        <tbody>{Object.entries(labels).map(([key, label]) => <tr key={key} className="border-b border-white/10">
          <th className="py-3 pr-4 font-normal">{label}</th>
          <td className="p-3">{(result.base.metrics[key] * 100).toFixed(1)}% <span className="text-muted-foreground">({Math.round(result.base.metrics[key] * result.base.cases)}/{result.base.cases})</span></td>
          <td className="p-3">{(result.adapter.metrics[key] * 100).toFixed(1)}% <span className="text-muted-foreground">({Math.round(result.adapter.metrics[key] * result.adapter.cases)}/{result.adapter.cases})</span></td>
        </tr>)}</tbody>
      </table>
    </div>
    <p className="mt-5 leading-7">Change in all-check success: <strong>{(result.automatic_success_delta * 100).toFixed(1)} percentage points</strong>.
      {' '}Paired group-bootstrap 95% interval: {result.paired_group_bootstrap_95_interval.map(n => (n * 100).toFixed(1)).join(' to ')} points.</p>
    <p className="mt-2 text-sm leading-6 text-muted-foreground">Measured request latency, p50 / p95: base {(result.base.latency_ms.p50 / 1000).toFixed(2)} / {(result.base.latency_ms.p95 / 1000).toFixed(2)} seconds;
      {' '}adapter {(result.adapter.latency_ms.p50 / 1000).toFixed(2)} / {(result.adapter.latency_ms.p95 / 1000).toFixed(2)} seconds. Timing is specific to this runtime and workload.</p>
    <p className="mt-3 text-sm leading-6 text-muted-foreground">All failures remain in the denominator. These checks measure a synthetic contract, not human editorial preference. The lexical safety check can flag sensitive words even in a denial; its failure rate is not a count of harmful assertions.</p>
    {example && <div className="mt-7 border-t border-white/10 pt-6">
      <h3 className="text-xl font-semibold">Inspect recorded outputs</h3>
      <p className="mt-2 text-sm leading-6 text-muted-foreground">One example per signal and evidence condition: the first matching case in dataset order, selected independently of outcomes. All 120 cases are in the download.</p>
      <label className="mt-4 block text-sm" htmlFor={comparison.id + '-case'}>Choose an evidence scenario</label>
      <select id={comparison.id + '-case'} value={selected} onChange={e => setSelected(Number(e.target.value))}
        className="mt-2 w-full max-w-xl rounded-lg border border-white/20 bg-background p-3 text-sm">
        {comparison.examples.map((item, index) => <option key={item.id} value={index}>{item.signal.replaceAll('_', ' ')} · {item.condition.replaceAll('_', ' ')}</option>)}
      </select>
      <p className="mt-3 break-all text-xs text-muted-foreground">Recorded case: {example.id}</p>
      <details className="mt-4 rounded-xl border border-white/10 p-4"><summary className="cursor-pointer text-sm text-primary">Supplied evidence and timing</summary>
        <pre className="mt-3 max-h-80 overflow-auto whitespace-pre-wrap break-words text-xs leading-5">{JSON.stringify(example.inputs, null, 2)}</pre>
      </details>
      <div className="mt-4 grid gap-4 lg:grid-cols-2">{(['base', 'adapter'] as const).map(variant => {
        const prediction = example[variant];
        const failures = Object.entries(prediction.metrics).filter(([key, value]) => key !== 'automatic_success' && !value).map(([key]) => labels[key]);
        return <article key={variant} className="min-w-0 rounded-xl border border-white/10 p-4">
          <h4 className="font-semibold">{variant === 'base' ? 'Base model' : 'With adapter'}</h4>
          <p className={`mt-2 text-sm ${prediction.metrics.automatic_success ? 'text-primary' : 'text-amber-200'}`}>
            {prediction.metrics.automatic_success ? 'All automatic checks passed' : 'Failed checks: ' + failures.join(', ')}
          </p>
          <pre className="mt-3 max-h-96 overflow-auto whitespace-pre-wrap break-words text-xs leading-5">{prediction.raw_output ?? `No output retained. Error: ${prediction.error_type ?? 'unknown'}`}</pre>
        </article>;
      })}</div>
    </div>}
    <a className="mt-6 inline-block text-sm text-primary" href={comparison.download} download>Download complete predictions, reports and verification evidence →</a>
    <p className="mt-4 text-sm text-amber-200">Human editorial review and production model promotion remain pending.</p>
  </section>;
}
