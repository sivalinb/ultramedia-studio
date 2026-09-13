import base from '@/week5/calibration/runs/base/summary.json';
import adapter from '@/week5/calibration/runs/adapter/summary.json';
import rules from '@/week5/calibration/runs/rules/summary.json';

export default function CalibrationEvidence() {
  const variants = [['Rules', rules], ['Base', base], ['Adapter', adapter]] as const;
  return (
    <section id="calibration-diagnosis" className="mt-12 rounded-3xl border border-amber-400/30 bg-amber-400/5 p-6 sm:p-8" aria-labelledby="calibration-title">
      <p className="text-xs uppercase tracking-widest text-amber-300">Week 4 feedback → Week 5 investigation</p>
      <h2 id="calibration-title" className="mt-3 text-2xl font-semibold">Check the judge. Explain the hold.</h2>
      <p className="mt-4 max-w-3xl leading-7 text-muted-foreground">
        A better benchmark score did not establish editorial readiness. We ran 48 new fictional cases per variant,
        changing evidence sufficiency and misleading hints in matched pairs. These are exploratory results with
        author-proposed labels. Independent label and judge calibration remain pending.
      </p>
      <div className="mt-6 overflow-x-auto">
        <table className="w-full min-w-[540px] text-left text-sm">
          <caption className="pb-3 text-left text-muted-foreground">Unnecessary holds on complete evidence: eight source groups per hint condition</caption>
          <thead><tr className="border-b border-white/15"><th className="py-3 pr-4">Variant</th><th className="pr-4">Neutral hint</th><th className="pr-4">Misleading hint</th><th>All-check passes, all 48</th></tr></thead>
          <tbody>{variants.map(([name, result]) => <tr key={name} className="border-b border-white/10">
            <th className="py-3 pr-4 font-medium">{name}</th>
            <td>{result.cells.complete_neutral.unnecessary_holds}/8</td>
            <td>{result.cells.complete_misleading.unnecessary_holds}/8</td>
            <td>{Object.values(result.cells).reduce((sum, cell) => sum + cell.all_checks_pass, 0)}/48</td>
          </tr>)}</tbody>
        </table>
      </div>
      <div className="mt-6 grid gap-5 md:grid-cols-3">
        <div><h3 className="font-semibold">A hint effect, with limits</h3><p className="mt-2 text-sm leading-6 text-muted-foreground">Changing only the hint adds eight holds for the base and six for the adapter. Both models hold all missing/conflicting cases. The adapter also holds two neutral record projections.</p></div>
        <div><h3 className="font-semibold">The judge has blind spots</h3><p className="mt-2 text-sm leading-6 text-muted-foreground">Two reversed-meaning challenges pass existing checks. A denial containing a sensitive word is rejected. These ten author-designed challenges still need independent review.</p></div>
        <div><h3 className="font-semibold">Release remains blocked</h3><p className="mt-2 text-sm leading-6 text-muted-foreground">The adapter invents a citation in all 16 missing-evidence cases. Its 22/48 score is below the base's 27/48 on this diagnostic. Earlier results remain available below.</p></div>
      </div>
      <p className="mt-6 text-sm leading-6">Next: independent labels → judge calibration → adjudication → repeat paired tests → one targeted change → fresh evaluation.</p>
      <p className="mt-3 text-sm text-muted-foreground">Eight authored source groups; one misleading-hint wording. No retrieval intervention, human-calibrated accuracy, speed comparison or production promotion is claimed.</p>
      <div className="mt-5 flex flex-wrap gap-5 text-sm text-primary">
        <a href="/week5/calibration/RESULTS.md">Read findings and limitations →</a>
        <a href="/week5/calibration-evidence.zip">Download protocol, packets and all 144 outputs →</a>
      </div>
    </section>
  );
}
