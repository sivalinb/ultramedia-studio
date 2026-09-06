'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Activity, ArrowUpRight, Bot, CheckCircle2, Clock3, Database, Eye, Film, FlaskConical, Gauge, Layers3, MapPin, Play, Radio, Share2, ShieldCheck, SlidersHorizontal, Sparkles, TrendingUp, Workflow, Zap } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button, buttonVariants } from '@/components/ui/button';

const stories = [
  { time: '19:42', eyebrow: 'Turning point detected', title: 'The race just changed in the canyons.', copy: 'Mara Velez gained 11 positions from Devil’s Thumb to Michigan Bluff—her strongest sustained climb of the day.', signal: '+11 places' },
  { time: '19:36', eyebrow: 'Course record watch', title: 'A historic pace survives Foresthill.', copy: 'Eli Mercer is eight minutes inside record pace, even after a measured slowdown through the hottest sector.', signal: '68% chance' },
  { time: '19:28', eyebrow: 'Last finisher watch', title: 'The final cutoff is tightening.', copy: 'Three runners are separated by six minutes. One timing read is still missing, so the projection remains provisional.', signal: '±29 min' },
];

const runners = [
  ['01', 'Eli Mercer', '13:58 proj.', '+02'],
  ['02', 'Tom Harker', '14:16 proj.', '—'],
  ['03', 'Noah Chen', '14:27 proj.', '+04'],
  ['01F', 'Mara Velez', '16:11 proj.', '+11'],
];

export default function Home() {
  const [activeStory, setActiveStory] = useState(0);
  const [activeLab, setActiveLab] = useState<'models' | 'evals' | 'trace'>('evals');
  const [highlightBuilt, setHighlightBuilt] = useState(false);
  const story = stories[activeStory];
  return (
    <main className="min-h-screen overflow-hidden bg-background text-foreground">
      <header className="sticky top-0 z-50 border-b border-white/10 bg-[#090d0b]/92 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-[1600px] items-center justify-between px-4 sm:px-6">
          <a href="#top" className="flex items-center gap-3" aria-label="UltraMedia Studio home">
            <span className="grid size-8 place-items-center rounded-full bg-primary text-primary-foreground"><Activity className="size-4" strokeWidth={2.7} /></span>
            <span className="text-sm font-black tracking-[-0.02em]">ULTRAMEDIA <span className="text-white/45">STUDIO</span></span>
          </a>
          <div className="hidden items-center gap-2 rounded-full border border-primary/25 bg-primary/8 px-3 py-1.5 text-xs sm:flex">
            <span className="relative flex size-2"><span className="absolute inline-flex size-full animate-ping rounded-full bg-primary opacity-70" /><span className="relative inline-flex size-2 rounded-full bg-primary" /></span>
            <span className="font-semibold">LIVE · WESTERN STATES 100</span><span className="text-white/40">19:42 PDT</span>
          </div>
          <div className="flex items-center gap-2"><Link href="/races" className={buttonVariants({ size: 'sm', variant: 'ghost', className: 'hidden rounded-full font-bold sm:inline-flex' })}>Race atlas</Link><Link href="/studio" className={buttonVariants({ size: 'sm', className: 'rounded-full font-bold' })}>Open newsroom <ArrowUpRight className="size-4" /></Link></div>
        </div>
      </header>

      <div id="top" className="mx-auto max-w-[1600px] px-4 py-5 sm:px-6">
        <section className="relative mb-20 min-h-[700px] overflow-hidden rounded-[2rem] border border-white/10 bg-cover bg-[position:62%_center] shadow-[0_40px_140px_rgba(0,0,0,.48)]" style={{ backgroundImage: "url('/river-crossing-hero.png')" }} aria-label="Ultra runners crossing a mountain river at dawn">
          <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(6,10,8,.96)_0%,rgba(6,10,8,.78)_35%,rgba(6,10,8,.20)_70%,rgba(6,10,8,.08)_100%)]" />
          <div className="absolute inset-0 bg-gradient-to-t from-[#07100a]/75 via-transparent to-black/10" />
          <div className="relative z-10 flex min-h-[700px] max-w-3xl flex-col justify-between p-6 sm:p-10 lg:p-14">
            <div className="flex items-center gap-2"><Badge className="rounded-full bg-primary text-primary-foreground"><Radio className="mr-1 size-3" /> Live endurance intelligence</Badge><span className="text-[10px] font-semibold uppercase tracking-[.15em] text-white/45">Built for race day</span></div>
            <div className="py-16">
              <p className="mb-5 text-[10px] font-bold uppercase tracking-[.24em] text-primary">UltraMedia Studio</p>
              <h1 className="max-w-3xl text-[clamp(3.5rem,7.2vw,7.8rem)] font-black uppercase leading-[.82] tracking-[-.075em]">The AI newsroom for every mile.</h1>
              <p className="mt-7 max-w-2xl text-base leading-7 text-white/65 sm:text-lg sm:leading-8">UltraMedia helps race organizers, broadcasters, sponsors, and media teams turn live timing, GPS, weather, course, and historical data into verified stories, commentary, social highlights, and personalized finisher recaps.</p>
              <div className="mt-8 flex flex-wrap gap-3"><Link href="/races" className={buttonVariants({ size: 'lg', className: 'rounded-full px-6 font-bold' })}>Explore 10 years of races <ArrowUpRight className="size-4" /></Link><a href="#model-lab" className={buttonVariants({ size: 'lg', variant: 'outline', className: 'rounded-full border-white/20 bg-black/20 px-6 backdrop-blur hover:bg-white/10' })}>See how the AI works</a></div>
            </div>
            <div className="flex flex-wrap gap-x-8 gap-y-3 border-t border-white/15 pt-5 text-[10px] font-bold uppercase tracking-[.15em] text-white/45"><span>Race organizers</span><span>Broadcast teams</span><span>Sponsors</span><span>Athletes & fans</span></div>
          </div>
        </section>

        <div className="mb-5 flex items-end justify-between gap-6">
          <div><p className="mb-1 text-[10px] font-bold uppercase tracking-[0.22em] text-primary">Race intelligence / Live studio</p><h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Every mile becomes a story.</h1></div>
          <p className="hidden max-w-md text-right text-xs leading-relaxed text-white/45 md:block">AI-assisted race coverage grounded in timing, course, weather, and historical data. Human-approved before publish.</p>
        </div>

        <section className="grid overflow-hidden rounded-[1.5rem] border border-white/10 bg-card shadow-[0_30px_120px_rgba(0,0,0,.38)] lg:grid-cols-[250px_minmax(0,1fr)_340px]">
          <aside className="border-b border-white/10 bg-[#0b100d] p-5 lg:border-b-0 lg:border-r">
            <div className="flex items-start justify-between"><div><p className="text-[10px] font-bold uppercase tracking-[0.18em] text-white/35">Race desk</p><h2 className="mt-2 text-xl font-bold">Western States</h2><p className="mt-1 flex items-center gap-1.5 text-xs text-white/45"><MapPin className="size-3" /> Olympic Valley → Auburn</p></div><Badge variant="outline" className="border-primary/30 bg-primary/10 text-primary">100 MI</Badge></div>
            <div className="mt-6 grid grid-cols-2 gap-2"><Metric value="287" label="On course" /><Metric value="21" label="Finished" /></div>
            <div className="mt-7 flex items-center justify-between border-b border-white/8 pb-3"><p className="text-[10px] font-bold uppercase tracking-[0.18em] text-white/35">Projected leaders</p><TrendingUp className="size-3.5 text-primary" /></div>
            <div>{runners.map(([rank, name, time, movement]) => <div key={rank + name} className="grid grid-cols-[34px_1fr_auto] items-center border-b border-white/6 py-3"><span className="font-mono text-[11px] text-white/35">{rank}</span><div><p className="text-xs font-semibold">{name}</p><p className="mt-0.5 text-[10px] text-white/35">{time}</p></div><span className="font-mono text-[10px] text-primary">{movement}</span></div>)}</div>
            <div className="mt-5 rounded-xl border border-emerald-300/15 bg-emerald-300/5 p-3"><div className="flex items-center gap-2 text-emerald-300"><ShieldCheck className="size-4" /><span className="text-xs font-semibold">Data confidence · High</span></div><p className="mt-1.5 text-[10px] leading-relaxed text-white/35">6 verified sources · Updated 12s ago</p></div>
          </aside>

          <article className="relative min-h-[630px] overflow-hidden p-5 sm:p-8 lg:p-10">
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_75%_15%,rgba(196,255,74,.08),transparent_30%)]" />
            <div className="relative z-10 flex h-full flex-col">
              <div className="flex flex-wrap items-center justify-between gap-3"><Badge className="rounded-full bg-primary text-primary-foreground hover:bg-primary"><Sparkles className="mr-1 size-3" /> {story.eyebrow}</Badge><span className="flex items-center gap-1.5 font-mono text-[10px] text-white/40"><Clock3 className="size-3" /> Detected {story.time}</span></div>
              <div className="my-auto py-10"><h2 className="max-w-4xl text-[clamp(2.8rem,6vw,6.8rem)] font-black uppercase leading-[0.83] tracking-[-0.07em]">{story.title}</h2><p className="mt-7 max-w-2xl text-sm leading-7 text-white/55 sm:text-base">{story.copy}</p><div className="mt-7 flex flex-wrap gap-3"><Button className="rounded-full font-bold" onClick={() => setHighlightBuilt(true)}><Play className="size-4 fill-current" /> {highlightBuilt ? 'Draft ready' : 'Build highlight'}</Button><a href="#model-lab" onClick={() => setActiveLab('trace')} className={buttonVariants({ variant: 'outline', className: 'rounded-full border-white/15 bg-white/[.03] hover:bg-white/10' })}><Eye className="size-4" /> Inspect evidence</a></div></div>
              <div className="rounded-2xl border border-white/10 bg-black/20 p-4 sm:p-5"><div className="mb-3 flex items-center justify-between gap-4"><div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-white/35">Race profile · Mile 62</p><p className="mt-1 text-xs font-semibold">Devil’s Thumb → Michigan Bluff</p></div><span className="font-mono text-xs text-primary">+2,884 ft</span></div><ElevationChart /><div className="mt-3 grid grid-cols-3 gap-2"><Signal label="Record probability" value="68%" /><Signal label="Projected win" value="13:58" /><Signal label="Pace signal" value="Steady" /></div></div>
            </div>
          </article>

          <aside className="border-t border-white/10 bg-[#0b100d] p-5 lg:border-l lg:border-t-0">
            <div className="flex items-center justify-between"><div className="flex items-center gap-2"><Radio className="size-4 text-primary" /><h2 className="text-sm font-bold">AI newswire</h2></div><Badge variant="outline" className="border-white/10 text-[9px] text-white/40">LIVE</Badge></div>
            <p className="mt-2 text-xs leading-relaxed text-white/35">Ranked moments worth covering, grounded in the race graph.</p>
            <div className="mt-5 space-y-2">{stories.map((item, index) => <button key={item.time} onClick={() => setActiveStory(index)} className={`w-full rounded-xl border p-4 text-left transition ${activeStory === index ? 'border-primary/35 bg-primary/[.08]' : 'border-white/8 bg-white/[.02] hover:border-white/20 hover:bg-white/[.04]'}`}><div className="flex items-center justify-between gap-4"><span className={`text-[9px] font-bold uppercase tracking-[0.14em] ${activeStory === index ? 'text-primary' : 'text-white/35'}`}>{item.eyebrow}</span><span className="font-mono text-[9px] text-white/25">{item.time}</span></div><p className="mt-2 text-sm font-semibold leading-snug">{item.title}</p><div className="mt-3 flex items-center justify-between"><span className="text-[10px] text-white/35">Signal</span><span className="font-mono text-[10px] text-primary">{item.signal}</span></div></button>)}</div>
            <div className="mt-5 rounded-xl border border-white/8 p-4"><div className="flex items-center justify-between"><span className="text-[10px] font-bold uppercase tracking-[0.14em] text-white/35">Grounding guard</span><Gauge className="size-4 text-primary" /></div><div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/8"><div className="h-full w-[99.2%] rounded-full bg-primary" /></div><div className="mt-2 flex justify-between font-mono text-[9px] text-white/35"><span>Fact precision</span><span>99.2%</span></div></div>
          </aside>
        </section>

        <div className="mt-3 flex overflow-hidden rounded-full border border-primary/15 bg-primary/[.06] py-2 text-[10px] font-bold uppercase tracking-[0.15em] text-primary"><div className="ticker flex min-w-max gap-12 px-6"><span>Mile 62 · Mara Velez moves +11</span><span>Record watch · 68%</span><span>Next cutoff · Foresthill 10:30 PM</span><span>287 athletes on course</span><span>Mile 62 · Mara Velez moves +11</span><span>Record watch · 68%</span></div></div>
        <p className="mt-3 text-center text-[10px] text-white/25">Concept interface · Race and athlete data shown here is simulated for demonstration.</p>

        <section id="newsroom" className="py-24 sm:py-32">
          <SectionHeading eyebrow="One race. An entire media team." title="The live newsroom that never misses the moment." copy="UltraMedia turns timing streams into accurate, broadcast-ready narratives—so small race teams can cover like a global sports network." />
          <div className="mt-12 grid gap-px overflow-hidden rounded-3xl border border-white/10 bg-white/10 md:grid-cols-2 xl:grid-cols-4">
            <Feature icon={<Zap />} index="01" title="Turning-point detector" copy="Surfaces passes, collapses, cutoff drama, and record trajectories as they emerge." />
            <Feature icon={<Film />} index="02" title="Broadcast story desk" copy="Builds commentator briefs, lower-thirds, live-blog updates, and highlight scripts." />
            <Feature icon={<Share2 />} index="03" title="Social content engine" copy="Produces channel-ready clips, captions, athlete cards, and sponsor moments." />
            <Feature icon={<ShieldCheck />} index="04" title="Evidence before publish" copy="Every number links to its timing read, course segment, and confidence score." />
          </div>
        </section>

        <section className="relative aspect-[1200/630] min-h-[420px] overflow-hidden rounded-3xl border border-white/10 bg-cover bg-center shadow-[0_30px_100px_rgba(0,0,0,.42)]" style={{ backgroundImage: "url('/ultramedia-og.png')" }} aria-label="Trail runner approaching a mountain aid station at night">
          <div className="absolute inset-0 bg-gradient-to-t from-black/65 via-transparent to-transparent" />
          <div className="absolute bottom-5 right-5 max-w-xs rounded-2xl border border-white/15 bg-black/55 p-5 backdrop-blur-md sm:bottom-8 sm:right-8">
            <p className="text-[9px] font-bold uppercase tracking-[.18em] text-primary">Night coverage · Always on</p>
            <p className="mt-2 text-sm font-semibold">A broadcast desk that follows every athlete past the final aid station.</p>
          </div>
        </section>

        <section className="grid overflow-hidden rounded-3xl border border-white/10 bg-[#0a0e0c] lg:grid-cols-[.9fr_1.1fr]">
          <div className="relative min-h-[470px] overflow-hidden border-b border-white/10 p-7 lg:border-b-0 lg:border-r sm:p-10">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_100%,rgba(196,255,74,.16),transparent_46%)]" />
            <div className="relative z-10">
              <Badge className="rounded-full bg-primary text-primary-foreground">Runner spotlight · auto-draft</Badge>
              <h2 className="mt-7 max-w-xl text-4xl font-black uppercase leading-[.92] tracking-[-.055em] sm:text-6xl">The comeback no leaderboard explains.</h2>
              <p className="mt-5 max-w-md text-sm leading-7 text-white/50">Mara was 37th at Robinson Flat. Her canyon split moved her into the top ten—the fastest position gain in the women’s field.</p>
            </div>
            <div className="absolute bottom-7 left-7 right-7 z-10 grid grid-cols-3 gap-2 sm:left-10 sm:right-10"><Signal label="Position gain" value="+27" /><Signal label="Canyon rank" value="01F" /><Signal label="Confidence" value="99%" /></div>
          </div>
          <div className="p-6 sm:p-10">
            <p className="text-[10px] font-bold uppercase tracking-[.2em] text-primary">From raw data to trusted story</p>
            <h3 className="mt-3 text-3xl font-semibold tracking-tight">An agentic pipeline with an editor in control.</h3>
            <div className="mt-8 space-y-2">
              <PipelineStep icon={<Database />} label="Ingest" detail="Timing · GPS · weather · course history" time="184 ms" />
              <PipelineStep icon={<Layers3 />} label="Retrieve" detail="Course RAG finds relevant segment context" time="420 ms" />
              <PipelineStep icon={<Bot />} label="Compose" detail="Fine-tuned race journalist drafts the angle" time="1.6 s" />
              <PipelineStep icon={<ShieldCheck />} label="Verify" detail="Fact agent checks every claim and citation" time="910 ms" />
              <PipelineStep icon={<CheckCircle2 />} label="Approve" detail="Editor reviews, revises, and publishes" time="Human" />
            </div>
          </div>
        </section>

        <section id="model-lab" className="py-24 sm:py-32">
          <SectionHeading eyebrow="Portfolio-grade AI, visible" title="The intelligence behind the story is part of the product." copy="A transparent model lab makes fine-tuning, RAG, evaluations, agent traces, and release decisions inspectable—not hidden in a notebook." />
          <div className="mt-12 overflow-hidden rounded-3xl border border-white/10 bg-card">
            <div className="flex flex-wrap gap-2 border-b border-white/10 p-3">
              <LabTab active={activeLab === 'models'} onClick={() => setActiveLab('models')} icon={<SlidersHorizontal />} label="Model comparison" />
              <LabTab active={activeLab === 'evals'} onClick={() => setActiveLab('evals')} icon={<FlaskConical />} label="Evaluation suite" />
              <LabTab active={activeLab === 'trace'} onClick={() => setActiveLab('trace')} icon={<Workflow />} label="Agent trace" />
              <Badge variant="outline" className="ml-auto hidden border-emerald-300/20 bg-emerald-300/5 text-emerald-300 sm:flex">Release candidate · PASS</Badge>
            </div>
            <div className="min-h-[430px] p-5 sm:p-8">
              {activeLab === 'models' && <ModelComparison />}
              {activeLab === 'evals' && <EvalSuite />}
              {activeLab === 'trace' && <AgentTrace />}
            </div>
          </div>
          <p className="mt-3 text-right text-[10px] text-white/25">Illustrative offline evaluation results for this product concept.</p>
        </section>

        <section className="relative overflow-hidden rounded-3xl border border-primary/20 bg-primary px-6 py-16 text-primary-foreground sm:px-12 sm:py-20">
          <div className="absolute -right-10 -top-24 size-80 rounded-full border-[50px] border-black/5" />
          <div className="relative z-10 grid gap-12 lg:grid-cols-[1fr_.8fr] lg:items-end">
            <div><p className="text-[10px] font-black uppercase tracking-[.22em] opacity-60">Commercial product</p><h2 className="mt-4 max-w-4xl text-5xl font-black uppercase leading-[.88] tracking-[-.065em] sm:text-7xl">Make your race impossible to look away from.</h2><p className="mt-6 max-w-2xl text-sm leading-7 opacity-65">For race organizers, broadcast teams, sponsors, and media crews who need richer coverage without a stadium-sized production team.</p></div>
            <div className="rounded-2xl bg-[#0d120f] p-6 text-white shadow-2xl"><p className="text-[10px] font-bold uppercase tracking-[.18em] text-primary">Race Day Studio</p><div className="mt-4 flex items-end gap-2"><span className="text-4xl font-semibold">Custom</span><span className="pb-1 text-xs text-white/40">per race</span></div><ul className="mt-6 space-y-3 text-xs text-white/60"><li className="flex gap-2"><CheckCircle2 className="size-4 text-primary" /> Live newsroom + story alerts</li><li className="flex gap-2"><CheckCircle2 className="size-4 text-primary" /> Broadcast and sponsor content packs</li><li className="flex gap-2"><CheckCircle2 className="size-4 text-primary" /> Verified recaps for every finisher</li></ul><Button className="mt-7 w-full rounded-full" variant="secondary">Book a race demo <ArrowUpRight className="size-4" /></Button></div>
          </div>
        </section>

        <footer className="flex flex-col items-start justify-between gap-6 py-10 text-xs text-white/35 sm:flex-row sm:items-center"><div className="flex items-center gap-2 font-bold text-white"><Activity className="size-4 text-primary" /> ULTRAMEDIA STUDIO</div><p>Concept product experience · Built for the future of endurance media.</p><div className="flex gap-5"><Link href="/races" className="hover:text-primary">Race atlas</Link><a href="#model-lab" className="hover:text-primary">Model lab</a></div></footer>
      </div>
    </main>
  );
}

function Metric({ value, label }: { value: string; label: string }) { return <div className="rounded-xl border border-white/8 bg-white/[.025] p-3"><p className="font-mono text-xl font-semibold">{value}</p><p className="mt-1 text-[10px] text-white/35">{label}</p></div>; }
function Signal({ label, value }: { label: string; value: string }) { return <div className="rounded-lg bg-white/[.035] px-3 py-2.5"><p className="truncate text-[9px] text-white/30">{label}</p><p className="mt-1 font-mono text-xs font-semibold text-primary">{value}</p></div>; }
function ElevationChart() { return <svg viewBox="0 0 720 120" className="h-24 w-full" role="img" aria-label="Elevation profile highlighting mile 62"><defs><linearGradient id="fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#c4ff4a" stopOpacity=".28" /><stop offset="100%" stopColor="#c4ff4a" stopOpacity="0" /></linearGradient></defs><path d="M0 98 C40 86 55 92 88 74 C118 58 128 78 160 64 C192 50 208 22 245 45 C278 64 293 70 328 47 C363 25 384 12 420 37 C455 61 478 91 512 73 C548 54 559 29 592 37 C623 44 642 74 672 57 C692 46 702 40 720 28 L720 120 L0 120Z" fill="url(#fill)" /><path d="M0 98 C40 86 55 92 88 74 C118 58 128 78 160 64 C192 50 208 22 245 45 C278 64 293 70 328 47 C363 25 384 12 420 37 C455 61 478 91 512 73 C548 54 559 29 592 37 C623 44 642 74 672 57 C692 46 702 40 720 28" fill="none" stroke="#c4ff4a" strokeWidth="2" /><line x1="450" x2="450" y1="8" y2="112" stroke="#c4ff4a" strokeDasharray="3 4" opacity=".7" /><circle cx="450" cy="59" r="4.5" fill="#0d120f" stroke="#c4ff4a" strokeWidth="2" /></svg>; }

function SectionHeading({ eyebrow, title, copy }: { eyebrow: string; title: string; copy: string }) {
  return <div className="grid gap-5 lg:grid-cols-[1fr_.65fr] lg:items-end"><div><p className="text-[10px] font-bold uppercase tracking-[.22em] text-primary">{eyebrow}</p><h2 className="mt-3 max-w-4xl text-4xl font-semibold leading-[1.02] tracking-[-.05em] sm:text-6xl">{title}</h2></div><p className="max-w-xl text-sm leading-7 text-white/45 lg:pb-1">{copy}</p></div>;
}

function Feature({ icon, index, title, copy }: { icon: React.ReactNode; index: string; title: string; copy: string }) {
  return <article className="group bg-[#101612] p-6 transition hover:bg-[#151d17] sm:p-8"><div className="flex items-start justify-between"><span className="text-primary [&>svg]:size-5">{icon}</span><span className="font-mono text-[10px] text-white/20">{index}</span></div><h3 className="mt-12 text-lg font-semibold">{title}</h3><p className="mt-3 text-xs leading-6 text-white/40">{copy}</p><ArrowUpRight className="mt-8 size-4 text-white/20 transition group-hover:translate-x-1 group-hover:-translate-y-1 group-hover:text-primary" /></article>;
}

function PipelineStep({ icon, label, detail, time }: { icon: React.ReactNode; label: string; detail: string; time: string }) {
  return <div className="grid grid-cols-[38px_1fr_auto] items-center gap-3 rounded-xl border border-white/8 bg-white/[.02] p-3.5"><span className="grid size-9 place-items-center rounded-lg bg-primary/10 text-primary [&>svg]:size-4">{icon}</span><div><p className="text-xs font-semibold">{label}</p><p className="mt-1 text-[10px] text-white/35">{detail}</p></div><span className="font-mono text-[10px] text-white/35">{time}</span></div>;
}

function LabTab({ active, onClick, icon, label }: { active: boolean; onClick: () => void; icon: React.ReactNode; label: string }) {
  return <button onClick={onClick} className={`flex items-center gap-2 rounded-full px-4 py-2 text-xs font-semibold transition [&>svg]:size-3.5 ${active ? 'bg-primary text-primary-foreground' : 'text-white/40 hover:bg-white/5 hover:text-white'}`}>{icon}{label}</button>;
}

function ModelComparison() {
  const models = [
    { name: 'Prompt only', detail: 'Qwen3-4B · zero-shot', grounded: '82.0%', latency: '1.2s', cost: '$0.00', status: 'Baseline' },
    { name: 'RAG', detail: 'Qwen3-4B + course index', grounded: '96.4%', latency: '2.8s', cost: '$0.00', status: 'Strong' },
    { name: 'LoRA + RAG', detail: '4-bit adapter + race context', grounded: '99.2%', latency: '3.4s', cost: '$0.00', status: 'Selected' },
  ];
  return <div><div className="flex items-end justify-between gap-4"><div><p className="text-[10px] font-bold uppercase tracking-[.18em] text-primary">Experiment 24-06-B</p><h3 className="mt-2 text-2xl font-semibold">Which approach earns the publish button?</h3></div><span className="hidden font-mono text-[10px] text-white/30 sm:block">600 held-out race moments</span></div><div className="mt-8 overflow-x-auto"><div className="min-w-[680px]"><div className="grid grid-cols-[1.5fr_repeat(4,1fr)] border-b border-white/10 px-4 pb-3 text-[9px] font-bold uppercase tracking-[.14em] text-white/30"><span>Variant</span><span>Grounded facts</span><span>P95 latency</span><span>Run cost</span><span>Decision</span></div>{models.map((model) => <div key={model.name} className={`grid grid-cols-[1.5fr_repeat(4,1fr)] items-center border-b border-white/6 px-4 py-5 text-xs ${model.status === 'Selected' ? 'bg-primary/[.06]' : ''}`}><div><p className="font-semibold">{model.name}</p><p className="mt-1 text-[10px] text-white/30">{model.detail}</p></div><span className="font-mono text-primary">{model.grounded}</span><span className="font-mono text-white/50">{model.latency}</span><span className="font-mono text-white/50">{model.cost}</span><Badge variant="outline" className={model.status === 'Selected' ? 'w-fit border-primary/30 text-primary' : 'w-fit border-white/10 text-white/40'}>{model.status}</Badge></div>)}</div></div><p className="mt-6 text-xs leading-6 text-white/35">Local-first stack: Qwen3-4B with QLoRA adapters for race-journalism style, backed by a course and history RAG index. Cloud models remain optional judges, not production dependencies.</p></div>;
}

function EvalSuite() {
  const evals = [
    ['Numeric grounding', '100%', 'PASS', 'Split, rank, cutoff and elevation values match source rows'],
    ['Citation precision', '99.2%', 'PASS', 'Claims point to the correct timing or context record'],
    ['Style adherence', '96.8%', 'PASS', 'Concise live-sports voice without unsupported drama'],
    ['Hallucinated facts', '0', 'PASS', 'No invented athlete, sponsor, result, or medical claim'],
  ];
  return <div className="grid gap-8 lg:grid-cols-[1fr_280px]"><div><p className="text-[10px] font-bold uppercase tracking-[.18em] text-primary">Release gate · v0.8.4</p><h3 className="mt-2 text-2xl font-semibold">Every draft must survive the hard cases.</h3><div className="mt-7 space-y-2">{evals.map(([name, score, status, description]) => <div key={name} className="grid gap-3 rounded-xl border border-white/8 bg-white/[.02] p-4 sm:grid-cols-[1fr_80px_70px]"><div><p className="text-xs font-semibold">{name}</p><p className="mt-1 text-[10px] leading-5 text-white/35">{description}</p></div><span className="font-mono text-sm text-primary sm:text-center">{score}</span><span className="text-[9px] font-bold text-emerald-300 sm:text-right">{status}</span></div>)}</div></div><div className="rounded-2xl border border-emerald-300/15 bg-emerald-300/[.04] p-6"><div className="grid size-12 place-items-center rounded-full bg-emerald-300 text-[#0d120f]"><CheckCircle2 className="size-6" /></div><p className="mt-7 text-[10px] font-bold uppercase tracking-[.18em] text-emerald-300">Release decision</p><p className="mt-2 text-4xl font-semibold">PASS</p><p className="mt-3 text-xs leading-6 text-white/40">All critical safety and grounding thresholds cleared. Candidate may advance to shadow mode.</p><div className="mt-8 border-t border-white/8 pt-4 font-mono text-[9px] text-white/30"><p>Suite: race-story-v12</p><p className="mt-2">Cases: 600 + 42 adversarial</p></div></div></div>;
}

function AgentTrace() {
  const trace = [
    ['00:00.000', 'moment-detector', 'Flagged +11 position change', '184 ms'],
    ['00:00.184', 'retrieval-agent', 'Loaded 8 course + history passages', '420 ms'],
    ['00:00.604', 'story-agent', 'Drafted comeback narrative', '1.6 s'],
    ['00:02.204', 'fact-verifier', 'Validated 7/7 claims; 3 citations', '910 ms'],
    ['00:03.114', 'policy-router', 'Routed to editor queue', '286 ms'],
  ];
  return <div><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-[10px] font-bold uppercase tracking-[.18em] text-primary">Trace 8F21 · story.generate</p><h3 className="mt-2 text-2xl font-semibold">See exactly how a story was made.</h3></div><div className="flex gap-4 font-mono text-[10px] text-white/35"><span>3.4 s total</span><span className="text-emerald-300">0 errors</span></div></div><div className="mt-8 overflow-hidden rounded-2xl border border-white/8">{trace.map(([timestamp, agent, event, duration], index) => <div key={agent} className="grid grid-cols-[18px_1fr_auto] gap-3 border-b border-white/6 bg-black/10 p-4 last:border-0 sm:grid-cols-[90px_18px_160px_1fr_auto]"><span className="hidden font-mono text-[9px] text-white/25 sm:block">{timestamp}</span><span className="mt-0.5 flex size-3 items-center justify-center rounded-full border border-primary/50"><span className="size-1 rounded-full bg-primary" /></span><span className="hidden font-mono text-[10px] text-primary sm:block">{agent}</span><div><p className="text-xs">{event}</p><p className="mt-1 font-mono text-[9px] text-white/25 sm:hidden">{agent} · {timestamp}</p></div><span className="font-mono text-[10px] text-white/30">{duration}</span></div>)}</div><div className="mt-5 flex flex-wrap gap-2"><Badge variant="outline" className="border-white/10 text-white/40">LangGraph orchestration</Badge><Badge variant="outline" className="border-white/10 text-white/40">OpenTelemetry traces</Badge><Badge variant="outline" className="border-white/10 text-white/40">Phoenix observability</Badge><Badge variant="outline" className="border-white/10 text-white/40">Human approval</Badge></div></div>;
}
