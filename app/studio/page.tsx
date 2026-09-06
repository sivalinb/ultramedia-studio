'use client';

import { useState } from 'react';
import { Activity, ArrowLeft, CheckCircle2, Database, FlaskConical, Radio, RefreshCw, ShieldCheck, Sparkles, Workflow, XCircle, Zap } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button, buttonVariants } from '@/components/ui/button';

const API_BASE = process.env.NEXT_PUBLIC_ULTRAMEDIA_API_URL || '';

type Story = {
  id?: string;
  eyebrow: string;
  headline: string;
  body: string;
  social_caption: string;
  confidence: number;
  status: string;
  trace_id?: string;
  citations: Array<{ id: string; title: string; excerpt: string; score: number }>;
};

const initialStory: Story = {
  eyebrow: 'Turning point detected',
  headline: 'Mara Velez just changed the shape of the race.',
  body: 'Mara Velez gained 20 positions between Devil’s Thumb and Foresthill. UltraMedia matched the synthetic timing signal with official course context; an editor must approve this draft before publication.',
  social_caption: 'Turning point: a 20-place surge through the canyon sector. Verified race context attached. #UltraMedia',
  confidence: 0.94,
  status: 'pending_review',
  citations: [
    { id: 'timing-demo', title: 'Timing comparison · Foresthill', excerpt: 'Synthetic timing: position 31 at Devil’s Thumb to position 11 at Foresthill.', score: 1 },
    { id: 'wser-canyons', title: 'Official canyon sector context', excerpt: 'Official course context covering the California gold-country canyons.', score: 0.91 },
  ],
};

const trace = [
  ['moment_detector', 'Validated position-gain signal', '12 ms'],
  ['evidence_retriever', 'Retrieved timing + course evidence', '184 ms'],
  ['story_writer', 'Generated structured newsroom draft', '1.6 s'],
  ['fact_verifier', 'Validated claims and citation IDs', '310 ms'],
  ['safety_editor', 'Blocked unsupported health inferences', '82 ms'],
  ['human_review_queue', 'Paused publication for an editor', '26 ms'],
];

export default function StudioPage() {
  const [story, setStory] = useState(initialStory);
  const [loading, setLoading] = useState(false);
  const [evalStatus, setEvalStatus] = useState<'idle' | 'running' | 'PASS' | 'FAIL'>('idle');
  const [message, setMessage] = useState('Select a signal and generate a grounded story.');

  async function generateStory() {
    setLoading(true);
    setMessage('Running six agents against timing and course evidence…');
    try {
      if (API_BASE) {
        const response = await fetch(`${API_BASE}/api/v1/stories/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ race_id: 'wser-demo', moment: { athlete_bib: '214', signal_type: 'position_gain', headline_hint: 'large position gain through the canyon sector' } }),
        });
        if (!response.ok) throw new Error('The Python API rejected this signal.');
        setStory(await response.json());
        setMessage('Python workflow complete. Draft is waiting for human review.');
      } else {
        await new Promise((resolve) => setTimeout(resolve, 850));
        setStory({ ...initialStory, headline: 'The canyon surge is now the race’s defining move.', confidence: 0.96, status: 'pending_review' });
        setMessage('Portfolio simulation complete. Connect the Python API for live provider calls.');
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Generation failed safely.');
    } finally {
      setLoading(false);
    }
  }

  async function review(decision: 'approved' | 'revision_requested') {
    if (API_BASE && story.id) {
      const response = await fetch(`${API_BASE}/api/v1/stories/${story.id}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decision, reviewer: 'Portfolio Editor', rationale: decision === 'approved' ? 'Evidence checked' : 'Tighten the opening sentence' }),
      });
      if (response.ok) setStory(await response.json());
    } else {
      setStory((current) => ({ ...current, status: decision }));
    }
    setMessage(decision === 'approved' ? 'Approved by a human editor. Ready for channel publishing.' : 'Returned to the story agent with an editor note.');
  }

  async function runEvals() {
    setEvalStatus('running');
    if (API_BASE) {
      try {
        const response = await fetch(`${API_BASE}/api/v1/evals/run`, { method: 'POST' });
        const result = await response.json();
        setEvalStatus(result.release_decision);
        return;
      } catch {
        setEvalStatus('FAIL');
        return;
      }
    }
    await new Promise((resolve) => setTimeout(resolve, 700));
    setEvalStatus('PASS');
  }

  return (
    <main className="min-h-screen bg-background text-foreground">
      <header className="border-b border-white/10 bg-[#090d0b]/95">
        <div className="mx-auto flex h-16 max-w-[1500px] items-center justify-between px-4 sm:px-6">
          <div className="flex items-center gap-3"><a href="/" className={buttonVariants({ variant: 'ghost', size: 'icon-sm', className: 'rounded-full' })} aria-label="Back to UltraMedia home"><ArrowLeft className="size-4" /></a><span className="grid size-8 place-items-center rounded-full bg-primary text-primary-foreground"><Activity className="size-4" /></span><div><p className="text-xs font-black">ULTRAMEDIA STUDIO</p><p className="text-[9px] uppercase tracking-[.14em] text-white/35">Race control</p></div></div>
          <Badge variant="outline" className={API_BASE ? 'border-emerald-300/20 bg-emerald-300/5 text-emerald-300' : 'border-amber-300/20 bg-amber-300/5 text-amber-200'}>{API_BASE ? 'Python API connected' : 'Portfolio simulation'}</Badge>
        </div>
      </header>

      <div className="mx-auto max-w-[1500px] px-4 py-6 sm:px-6">
        <div className="mb-6 flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><p className="text-[10px] font-bold uppercase tracking-[.2em] text-primary">Western States simulation / Mile 62</p><h1 className="mt-2 text-3xl font-semibold tracking-tight">Live story control room</h1></div><div className="flex gap-2"><Button variant="outline" className="rounded-full border-white/15" onClick={runEvals} disabled={evalStatus === 'running'}><FlaskConical className={`size-4 ${evalStatus === 'running' ? 'animate-spin' : ''}`} /> {evalStatus === 'idle' ? 'Run release evals' : evalStatus}</Button><Button className="rounded-full font-bold" onClick={generateStory} disabled={loading}>{loading ? <RefreshCw className="size-4 animate-spin" /> : <Sparkles className="size-4" />} Generate story</Button></div></div>

        <div className="grid gap-4 xl:grid-cols-[290px_minmax(0,1fr)_360px]">
          <aside className="space-y-4">
            <Panel title="Live signal" icon={<Zap />}><div className="rounded-xl border border-primary/25 bg-primary/[.06] p-4"><div className="flex items-center justify-between"><Badge className="bg-primary text-primary-foreground">Selected</Badge><span className="font-mono text-[10px] text-primary">+20 places</span></div><p className="mt-4 text-sm font-semibold">Canyon position gain</p><p className="mt-2 text-xs leading-6 text-white/40">Bib 214 moved from 31st at Devil’s Thumb to 11th at Foresthill.</p></div><div className="mt-3 grid grid-cols-2 gap-2"><MiniMetric label="Signal confidence" value="98%" /><MiniMetric label="Source delay" value="12s" /></div></Panel>
            <Panel title="Grounded sources" icon={<Database />}><div className="space-y-2">{story.citations.map((citation) => <div key={citation.id} className="rounded-xl border border-white/8 bg-white/[.02] p-3"><div className="flex justify-between gap-3"><p className="text-xs font-semibold">{citation.title}</p><span className="font-mono text-[9px] text-primary">{Math.round(citation.score * 100)}%</span></div><p className="mt-2 text-[10px] leading-5 text-white/35">{citation.excerpt}</p></div>)}</div></Panel>
          </aside>

          <section className="overflow-hidden rounded-2xl border border-white/10 bg-card">
            <div className="flex items-center justify-between border-b border-white/10 px-5 py-4"><div className="flex items-center gap-2"><Radio className="size-4 text-primary" /><span className="text-xs font-bold">Story editor</span></div><Badge variant="outline" className={story.status === 'approved' ? 'border-emerald-300/20 text-emerald-300' : 'border-amber-300/20 text-amber-200'}>{story.status.replace('_', ' ')}</Badge></div>
            <div className="p-5 sm:p-8"><p className="text-[10px] font-bold uppercase tracking-[.18em] text-primary">{story.eyebrow}</p><h2 className="mt-4 text-4xl font-black uppercase leading-[.93] tracking-[-.055em] sm:text-6xl">{story.headline}</h2><p className="mt-7 max-w-3xl text-sm leading-7 text-white/55">{story.body}</p><div className="mt-8 rounded-2xl border border-white/8 bg-black/15 p-5"><p className="text-[9px] font-bold uppercase tracking-[.16em] text-white/30">Social caption</p><p className="mt-3 text-sm leading-6">{story.social_caption}</p></div><div className="mt-7 flex flex-wrap items-center gap-3"><Button className="rounded-full bg-emerald-300 text-emerald-950 hover:bg-emerald-200" onClick={() => review('approved')}><CheckCircle2 className="size-4" /> Approve story</Button><Button variant="outline" className="rounded-full border-white/15" onClick={() => review('revision_requested')}><XCircle className="size-4" /> Request revision</Button><span className="ml-auto font-mono text-[10px] text-white/35">Grounding {Math.round(story.confidence * 100)}%</span></div></div>
            <div aria-live="polite" className="border-t border-white/10 bg-primary/[.04] px-5 py-3 text-[10px] text-primary">{message}</div>
          </section>

          <aside><Panel title="Agent trace" icon={<Workflow />}><p className="mb-4 text-[10px] leading-5 text-white/35">Privacy-minimized execution. Raw prompts are not stored in trace metadata.</p><div>{trace.map(([stage, detail, duration], index) => <div key={stage} className="grid grid-cols-[18px_1fr_auto] gap-3 border-b border-white/6 py-3 last:border-0"><span className="mt-1.5 grid size-3 place-items-center rounded-full border border-primary/50"><span className="size-1 rounded-full bg-primary" /></span><div><p className="font-mono text-[10px] text-primary">{stage}</p><p className="mt-1 text-[10px] leading-5 text-white/40">{detail}</p></div><span className="font-mono text-[9px] text-white/25">{duration}</span></div>)}</div><div className="mt-5 rounded-xl border border-emerald-300/15 bg-emerald-300/[.04] p-4"><div className="flex items-center gap-2 text-emerald-300"><ShieldCheck className="size-4" /><span className="text-xs font-semibold">Human gate enforced</span></div><p className="mt-2 text-[10px] leading-5 text-white/35">The workflow can draft and verify. Only an authenticated editor can release.</p></div></Panel></aside>
        </div>
      </div>
    </main>
  );
}

function Panel({ title, icon, children }: { title: string; icon: React.ReactNode; children: React.ReactNode }) { return <section className="rounded-2xl border border-white/10 bg-card p-4"><div className="mb-4 flex items-center gap-2 text-primary [&>svg]:size-4">{icon}<h2 className="text-xs font-bold text-white">{title}</h2></div>{children}</section>; }
function MiniMetric({ label, value }: { label: string; value: string }) { return <div className="rounded-xl border border-white/8 bg-white/[.02] p-3"><p className="font-mono text-sm text-primary">{value}</p><p className="mt-1 text-[9px] text-white/30">{label}</p></div>; }
