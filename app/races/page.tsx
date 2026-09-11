'use client';
/* eslint-disable next/no-img-element */

import Link from '@/components/internal-link';
import { useState } from 'react';
import { Activity, ArrowLeft, ArrowUpRight, CalendarDays, CheckCircle2, Database, Download, ExternalLink, Flag, MapPin, Mountain, ShieldCheck, Sparkles, Trophy } from 'lucide-react';
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Badge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';

type Edition = {
  year: number;
  status?: 'cancelled';
  starters?: number;
  finishers?: number;
  finishRate?: number;
  sub24?: number;
  winner?: string;
  winnerTime?: string;
  women?: string;
  womenTime?: string;
  distance?: string;
};

type Race = {
  id: string;
  short: string;
  name: string;
  location: string;
  distance: string;
  accent: string;
  image: string;
  photoCredit: string;
  photoUrl: string;
  source: string;
  sourceLabel: string;
  coverage: string;
  metric: 'finishRate' | 'winnerHours';
  editions: Edition[];
};

const races: Race[] = [
  {
    id: 'utmb', short: 'UTMB', name: 'Ultra-Trail du Mont-Blanc', location: 'France · Italy · Switzerland', distance: '170–176 KM', accent: '#c4ff4a',
    image: 'https://commons.wikimedia.org/wiki/Special:Redirect/file/UTMB%202019%20in%20Chamonix.jpg', photoCredit: 'UTMB 2019 in Chamonix · Wikimedia Commons', photoUrl: 'https://commons.wikimedia.org/wiki/File:UTMB_2019_in_Chamonix.jpg', source: 'https://montblanc.utmb.world/en/results', sourceLabel: 'Official UTMB results', coverage: '2016–2025 · 9 contested editions', metric: 'finishRate',
    editions: [
      { year: 2016, starters: 2555, finishers: 1468, finishRate: 57.5, winner: 'Ludovic Pommeret', winnerTime: '22:00:02', women: 'Caroline Chaverot', womenTime: '25:15:40', distance: '170 km' },
      { year: 2017, starters: 2537, finishers: 1687, finishRate: 66.5, winner: "François D'Haene", winnerTime: '19:01:54', women: 'Núria Picas', womenTime: '25:46:43', distance: '167 km' },
      { year: 2018, starters: 2561, finishers: 1778, finishRate: 69.4, winner: 'Xavier Thévenard', winnerTime: '20:44:16', women: 'Francesca Canepa', womenTime: '26:03:48', distance: '170 km' },
      { year: 2019, starters: 2543, finishers: 1556, finishRate: 61.2, winner: 'Pau Capell', winnerTime: '20:19:07', women: 'Courtney Dauwalter', womenTime: '24:34:26', distance: '170 km' },
      { year: 2020, status: 'cancelled' },
      { year: 2021, starters: 2346, finishers: 1521, finishRate: 64.8, winner: "François D'Haene", winnerTime: '20:45:59', women: 'Courtney Dauwalter', womenTime: '22:30:54', distance: '170 km' },
      { year: 2022, starters: 2795, finishers: 1789, finishRate: 64.0, winner: 'Kilian Jornet', winnerTime: '19:49:30', women: 'Katie Schide', womenTime: '23:15:12', distance: '170 km' },
      { year: 2023, starters: 2693, finishers: 1757, finishRate: 65.2, winner: 'Jim Walmsley', winnerTime: '19:37:43', women: 'Courtney Dauwalter', womenTime: '23:29:14', distance: '172 km' },
      { year: 2024, starters: 2761, finishers: 1760, finishRate: 63.7, winner: 'Vincent Bouillard', winnerTime: '19:54:23', women: 'Katie Schide', womenTime: '22:09:31', distance: '176.4 km' },
      { year: 2025, starters: 2492, finishers: 1665, finishRate: 66.8, winner: 'Tom Evans', winnerTime: '19:18:58', women: 'Ruth Croft', womenTime: '22:56:23', distance: '175.3 km' },
    ],
  },
  {
    id: 'western-states', short: 'WSER', name: 'Western States 100', location: 'Olympic Valley → Auburn, California', distance: '100.2 MI', accent: '#ff8b5c',
    image: 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Foot%20repair%2C%20Michigan%20Bluff.jpg', photoCredit: 'Michigan Bluff · Wikimedia Commons', photoUrl: 'https://commons.wikimedia.org/wiki/File:Foot_repair,_Michigan_Bluff.jpg', source: 'https://www.wser.org/results/', sourceLabel: 'Official WSER results', coverage: '2016–2025 · official decade rollup', metric: 'finishRate',
    editions: [
      { year: 2016, starters: 353, finishers: 280, finishRate: 79.3, sub24: 102 }, { year: 2017, starters: 369, finishers: 248, finishRate: 67.2, sub24: 76 },
      { year: 2018, starters: 369, finishers: 299, finishRate: 81.0, sub24: 123 }, { year: 2019, starters: 369, finishers: 319, finishRate: 86.4, sub24: 130 },
      { year: 2020, status: 'cancelled' }, { year: 2021, starters: 315, finishers: 208, finishRate: 66.0, sub24: 57 },
      { year: 2022, starters: 383, finishers: 305, finishRate: 79.6, sub24: 101 }, { year: 2023, starters: 379, finishers: 328, finishRate: 86.5, sub24: 110 },
      { year: 2024, starters: 375, finishers: 286, finishRate: 76.3, sub24: 109 }, { year: 2025, starters: 369, finishers: 285, finishRate: 77.2, sub24: 92 },
    ],
  },
  {
    id: 'hardrock', short: 'HR100', name: 'Hardrock 100', location: 'Silverton, Colorado', distance: '100.5–101.8 MI', accent: '#67d7ff',
    image: 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Number%20486%20leaves%20Silverton%2C%20%287644100208%29.jpg', photoCredit: 'Runner leaves Silverton · Wikimedia Commons', photoUrl: 'https://commons.wikimedia.org/wiki/File:Number_486_leaves_Silverton,_(7644100208).jpg', source: 'https://www.hardrock100.com/hardrock-pastresults.php', sourceLabel: 'Official Hardrock archive', coverage: '2016–2025 · 8 contested editions', metric: 'winnerHours',
    editions: [
      { year: 2016, winner: 'Kilian Jornet', winnerTime: '22:58:28' }, { year: 2017, winner: 'Kilian Jornet', winnerTime: '24:32:19' },
      { year: 2018, winner: 'Jeff Browning', winnerTime: '26:20:21' }, { year: 2019, status: 'cancelled' }, { year: 2020, status: 'cancelled' },
      { year: 2021, winner: "François D'Haene", winnerTime: '21:45:50' }, { year: 2022, winner: 'Kilian Jornet', winnerTime: '21:36:24' },
      { year: 2023, winner: 'Aurélien Dunand-Pallaz', winnerTime: '23:00:30' }, { year: 2024, winner: 'Ludovic Pommeret', winnerTime: '21:33:06' },
      { year: 2025, winner: 'Ludovic Pommeret', winnerTime: '22:21:53' },
    ],
  },
  {
    id: 'cocodona', short: 'COCO250', name: 'Cocodona 250', location: 'Black Canyon City → Flagstaff, Arizona', distance: '249–256 MI', accent: '#f6c453',
    image: 'https://s3.amazonaws.com/www.irunfar.com/wp-content/uploads/2025/05/08073341/2025-Cocodona-250-Mile-women-champion-Rachel-Entrekin-in-fog-feature.jpg', photoCredit: 'Rachel Entrekin, Cocodona 2025 · iRunFar', photoUrl: 'https://www.irunfar.com/2025-cocodona-250-mile-results', source: 'https://www.aravaiparunning.com/cocodona/', sourceLabel: 'Official Cocodona archive', coverage: 'All 5 editions in the 2016–2025 window', metric: 'winnerHours',
    editions: [
      { year: 2021, starters: 174, finishers: 108, finishRate: 62.1, winner: 'Michael Versteeg', winnerTime: '72:50:25', women: 'Maggie Guterl', womenTime: '85:30:38' },
      { year: 2022, winner: 'Joe McConaughy', winnerTime: '59:28:54', women: 'Annie Hughes', womenTime: '71:10:22' },
      { year: 2023, starters: 193, finishers: 139, finishRate: 72.0, winner: 'Michael McKnight', winnerTime: '69:41:31', women: 'Sarah Ostaszewski', womenTime: '72:50:27' },
      { year: 2024, starters: 220, finishers: 151, finishRate: 68.6, winner: 'Harry Subertas', winnerTime: '59:50:55', women: 'Rachel Entrekin', womenTime: '73:31:25' },
      { year: 2025, winner: 'Dan Green', winnerTime: '58:47:18', women: 'Rachel Entrekin', womenTime: '63:50:55' },
    ],
  },
];

function hours(value?: string) {
  if (!value) return undefined;
  const [h, m, s] = value.split(':').map(Number);
  return Number((h + m / 60 + s / 3600).toFixed(2));
}

export default function RaceAtlasPage() {
  const [raceId, setRaceId] = useState('utmb');
  const race = races.find((item) => item.id === raceId) ?? races[0];
  const raced = race.editions.filter((row) => row.status !== 'cancelled');
  const chartData = race.editions.map((row) => ({ year: row.year, value: race.metric === 'finishRate' ? row.finishRate : hours(row.winnerTime), cancelled: row.status === 'cancelled' }));
  const starters = raced.reduce((sum, row) => sum + (row.starters ?? 0), 0);
  const finishers = raced.reduce((sum, row) => sum + (row.finishers ?? 0), 0);
  const values = chartData.map((row) => row.value).filter((value): value is number => typeof value === 'number');
  const stats = { starters, finishers, average: values.length ? values.reduce((a, b) => a + b, 0) / values.length : 0 };

  return (
    <main className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-50 border-b border-white/10 bg-[#090d0b]/92 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-[1600px] items-center justify-between px-4 sm:px-6">
          <Link href="/" className="flex items-center gap-3"><span className="grid size-8 place-items-center rounded-full bg-primary text-primary-foreground"><Activity className="size-4" /></span><span className="text-sm font-black">ULTRAMEDIA <span className="text-white/45">STUDIO</span></span></Link>
          <div className="hidden items-center gap-6 text-xs font-semibold text-white/45 md:flex"><Link href="/" className="hover:text-white">Overview</Link><span className="text-primary">Race atlas</span><Link href="/studio" className="hover:text-white">Newsroom</Link><Link href="/observability" className="hover:text-white">Observability</Link></div>
          <Link href="/studio" className={buttonVariants({ size: 'sm', className: 'rounded-full font-bold' })}>Open newsroom <ArrowUpRight className="size-4" /></Link>
        </div>
      </header>

      <div className="mx-auto max-w-[1600px] px-4 py-8 sm:px-6">
        <section className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-[#0b100d] p-6 sm:p-10">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_0%,rgba(196,255,74,.14),transparent_36%)]" />
          <div className="relative grid gap-10 xl:grid-cols-[1fr_430px] xl:items-end">
            <div><Badge className="rounded-full bg-primary text-primary-foreground"><Database className="mr-1 size-3" /> Public race intelligence</Badge><h1 className="mt-6 max-w-5xl text-[clamp(3.4rem,7vw,7.4rem)] font-black uppercase leading-[.84] tracking-[-.07em]">The decade<br />behind the drama.</h1><p className="mt-6 max-w-2xl text-sm leading-7 text-white/50 sm:text-base">Explore ten seasons of major ultra results, compare field outcomes, and turn verified history into race-day context. Every displayed statistic links back to a public source.</p></div>
            <div className="grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-white/10 bg-white/10"><Kpi value="4" label="Iconic races" /><Kpi value="31" label="Contested editions" /><Kpi value="25K+" label="Recorded starts*" /><Kpi value="2016–25" label="Fixed window" /></div>
          </div>
          <p className="relative mt-6 text-[10px] text-white/25">*Where public aggregate starter counts are available. Athlete-level records are not duplicated in this interface.</p>
        </section>

        <section className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {races.map((item) => <button key={item.id} onClick={() => setRaceId(item.id)} className={`group relative min-h-56 overflow-hidden rounded-2xl border text-left transition ${race.id === item.id ? 'border-primary shadow-[0_0_0_1px_rgba(196,255,74,.3)]' : 'border-white/10 hover:border-white/25'}`}>
            <img src={item.image} alt={`${item.name} event`} className="absolute inset-0 size-full object-cover transition duration-700 group-hover:scale-105" />
            <div className="absolute inset-0 bg-gradient-to-t from-black via-black/35 to-transparent" />
            <div className="absolute inset-x-0 bottom-0 p-5"><div className="flex items-end justify-between gap-4"><div><p className="text-[9px] font-bold uppercase tracking-[.18em]" style={{ color: item.accent }}>{item.short}</p><h2 className="mt-1 text-xl font-bold">{item.name}</h2><p className="mt-1 flex items-center gap-1 text-[10px] text-white/50"><MapPin className="size-3" /> {item.location}</p></div><CheckCircle2 className={`size-5 ${race.id === item.id ? 'text-primary' : 'text-white/30'}`} /></div></div>
          </button>)}
        </section>

        <section className="mt-5 grid overflow-hidden rounded-3xl border border-white/10 bg-card xl:grid-cols-[270px_minmax(0,1fr)_330px]">
          <aside className="border-b border-white/10 bg-[#0b100d] p-6 xl:border-b-0 xl:border-r">
            <p className="text-[10px] font-bold uppercase tracking-[.2em] text-white/30">Selected race</p><h2 className="mt-3 text-2xl font-bold">{race.name}</h2><p className="mt-2 text-xs leading-5 text-white/45">{race.location}</p><Badge variant="outline" className="mt-4 border-white/15 text-white/60">{race.distance}</Badge>
            <div className="mt-8 space-y-3"><MiniStat icon={<CalendarDays />} value={`${raced.length}`} label="Contested editions" /><MiniStat icon={<Flag />} value={stats.starters ? stats.starters.toLocaleString() : 'Winner data'} label={stats.starters ? 'Public starts in view' : 'Coverage in view'} /><MiniStat icon={<Trophy />} value={race.metric === 'finishRate' ? `${stats.average.toFixed(1)}%` : `${stats.average.toFixed(1)}h`} label={race.metric === 'finishRate' ? 'Average finish rate' : 'Average winning time'} /></div>
            <a href={race.source} target="_blank" rel="noreferrer" className="mt-8 flex items-center justify-between rounded-xl border border-primary/20 bg-primary/5 p-3 text-xs text-primary hover:bg-primary/10"><span><span className="block font-semibold">{race.sourceLabel}</span><span className="mt-1 block text-[10px] text-white/35">{race.coverage}</span></span><ExternalLink className="size-4" /></a>
          </aside>

          <article className="min-w-0 border-b border-white/10 p-5 sm:p-8 xl:border-b-0">
            <div className="flex flex-wrap items-start justify-between gap-4"><div><p className="text-[10px] font-bold uppercase tracking-[.2em] text-primary">Decade signal</p><h3 className="mt-2 text-2xl font-semibold">{race.metric === 'finishRate' ? 'Completion rate by edition' : 'Overall winning time by edition'}</h3></div><Badge variant="outline" className="border-emerald-300/20 bg-emerald-300/5 text-emerald-300"><ShieldCheck className="mr-1 size-3" /> Source linked</Badge></div>
            <div className="mt-8 h-[300px] min-w-0"><ResponsiveContainer width="100%" height="100%" minWidth={0}><LineChart data={chartData} margin={{ top: 10, right: 10, bottom: 0, left: -20 }}><CartesianGrid stroke="rgba(255,255,255,.08)" vertical={false} /><XAxis dataKey="year" stroke="rgba(255,255,255,.28)" tickLine={false} axisLine={false} fontSize={10} /><YAxis domain={race.metric === 'finishRate' ? [50, 90] : ['dataMin - 3', 'dataMax + 3']} stroke="rgba(255,255,255,.28)" tickLine={false} axisLine={false} fontSize={10} tickFormatter={(value) => `${value}${race.metric === 'finishRate' ? '%' : 'h'}`} /><Tooltip contentStyle={{ background: '#0b100d', border: '1px solid rgba(255,255,255,.12)', borderRadius: 12, fontSize: 12 }} formatter={(value) => [`${Number(value).toFixed(1)}${race.metric === 'finishRate' ? '%' : ' hours'}`, race.metric === 'finishRate' ? 'Finish rate' : 'Winning time']} /><Line type="monotone" dataKey="value" connectNulls={false} stroke={race.accent} strokeWidth={3} dot={{ r: 4, fill: '#0b100d', stroke: race.accent, strokeWidth: 2 }} activeDot={{ r: 6 }} /></LineChart></ResponsiveContainer></div>
            <div className="mt-6 rounded-2xl border border-primary/15 bg-primary/[.05] p-5"><div className="flex items-center gap-2 text-primary"><Sparkles className="size-4" /><p className="text-[10px] font-bold uppercase tracking-[.18em]">Analyst note</p></div><p className="mt-3 text-sm leading-6 text-white/65"><Insight race={race} /></p></div>
          </article>

          <aside className="bg-[#0b100d] p-5"><div className="flex items-center justify-between"><div><p className="text-[10px] font-bold uppercase tracking-[.18em] text-white/30">Edition ledger</p><p className="mt-1 text-xs text-white/45">2016 → 2025</p></div><a href="/data/race-history-2016-2025.json" download className="grid size-9 place-items-center rounded-full border border-white/10 text-white/45 hover:border-primary/40 hover:text-primary" aria-label="Download race dataset"><Download className="size-4" /></a></div>
            <div className="mt-4 max-h-[540px] overflow-y-auto pr-1">{race.editions.slice().reverse().map((row) => <EditionRow key={row.year} row={row} race={race} />)}</div>
          </aside>
        </section>

        <section className="py-20"><div className="grid gap-6 lg:grid-cols-[.75fr_1fr] lg:items-end"><div><p className="text-[10px] font-bold uppercase tracking-[.2em] text-primary">Real race texture</p><h2 className="mt-3 text-4xl font-semibold tracking-tight sm:text-6xl">Four courses.<br />Four different worlds.</h2></div><p className="text-sm leading-7 text-white/45">Event photography is shown with a visible source link. Wikimedia files retain their individual licenses; the Cocodona image is displayed from iRunFar with publisher and event attribution.</p></div>
          <div className="mt-10 grid gap-4 sm:grid-cols-2">{races.map((item) => <figure key={item.id} className="group relative aspect-[16/9] overflow-hidden rounded-2xl border border-white/10"><img src={item.image} alt={`${item.name} race photography`} className="size-full object-cover transition duration-700 group-hover:scale-105" /><div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/10 to-transparent" /><figcaption className="absolute inset-x-0 bottom-0 flex items-end justify-between gap-5 p-5"><div><p className="text-lg font-semibold">{item.name}</p><p className="mt-1 text-[10px] text-white/45">{item.photoCredit}</p></div><a href={item.photoUrl} target="_blank" rel="noreferrer" className="grid size-9 shrink-0 place-items-center rounded-full border border-white/20 bg-black/35 text-white hover:border-primary hover:text-primary" aria-label={`Open ${item.name} photo source`}><ExternalLink className="size-4" /></a></figcaption></figure>)}</div>
        </section>

        <section className="mb-10 grid overflow-hidden rounded-3xl border border-primary/20 bg-primary text-primary-foreground lg:grid-cols-[1fr_.75fr]"><div className="p-7 sm:p-10"><p className="text-[10px] font-black uppercase tracking-[.2em] opacity-55">From archive to air</p><h2 className="mt-4 text-4xl font-black uppercase leading-[.9] tracking-[-.055em] sm:text-6xl">Give every live moment a decade of context.</h2><p className="mt-5 max-w-xl text-sm leading-7 opacity-65">This race atlas is the retrieval layer for UltraMedia’s newsroom: public results become grounded context, while the model turns only cited facts into human-approved stories.</p></div><div className="flex flex-col justify-end bg-[#0b100d] p-7 text-white sm:p-10"><div className="space-y-3 text-xs text-white/55"><p className="flex items-center gap-2"><Database className="size-4 text-primary" /> Versioned public-data snapshot</p><p className="flex items-center gap-2"><Mountain className="size-4 text-primary" /> Race-aware retrieval and comparisons</p><p className="flex items-center gap-2"><ShieldCheck className="size-4 text-primary" /> Citations and cancellation handling</p></div><Link href="/studio" className={buttonVariants({ className: 'mt-7 rounded-full font-bold' })}>Use it in the newsroom <ArrowUpRight className="size-4" /></Link></div></section>

        <footer className="flex flex-col items-start justify-between gap-5 border-t border-white/10 py-8 text-xs text-white/35 sm:flex-row sm:items-center"><Link href="/" className="flex items-center gap-2 font-bold text-white"><ArrowLeft className="size-4 text-primary" /> UltraMedia home</Link><p>Public data snapshot · 2016–2025 · sources linked per race</p><a href="https://github.com/sivalinb/ultramedia-studio" target="_blank" rel="noreferrer" className="hover:text-primary">View source <ArrowUpRight className="inline size-3" /></a></footer>
      </div>
    </main>
  );
}

function Kpi({ value, label }: { value: string; label: string }) { return <div className="bg-[#101612] p-5"><p className="font-mono text-2xl font-semibold">{value}</p><p className="mt-1 text-[10px] uppercase tracking-[.12em] text-white/35">{label}</p></div>; }
function MiniStat({ icon, value, label }: { icon: React.ReactNode; value: string; label: string }) { return <div className="grid grid-cols-[34px_1fr] items-center gap-3 rounded-xl border border-white/8 bg-white/[.025] p-3"><span className="grid size-8 place-items-center rounded-lg bg-white/5 text-primary [&>svg]:size-4">{icon}</span><div><p className="font-mono text-sm font-semibold">{value}</p><p className="mt-0.5 text-[9px] text-white/35">{label}</p></div></div>; }
function EditionRow({ row, race }: { row: Edition; race: Race }) { if (row.status === 'cancelled') return <div className="mb-2 flex items-center justify-between rounded-xl border border-dashed border-white/10 p-3"><span className="font-mono text-xs text-white/55">{row.year}</span><Badge variant="outline" className="border-white/10 text-[9px] text-white/35">CANCELLED</Badge></div>; return <div className="mb-2 rounded-xl border border-white/8 bg-white/[.02] p-3"><div className="flex items-center justify-between"><span className="font-mono text-xs font-semibold">{row.year}</span><span className="font-mono text-[10px]" style={{ color: race.accent }}>{race.metric === 'finishRate' ? `${row.finishRate}% finished` : row.winnerTime}</span></div>{race.metric === 'finishRate' ? <p className="mt-2 text-[10px] text-white/35">{row.finishers?.toLocaleString()} / {row.starters?.toLocaleString()} finishers {row.sub24 ? `· ${row.sub24} under 24h` : ''}</p> : <><p className="mt-2 text-[10px] font-semibold text-white/65">{row.winner}</p>{row.women && <p className="mt-1 text-[9px] text-white/35">Women · {row.women} · {row.womenTime}</p>}</>}</div>; }
function Insight({ race }: { race: Race }) { if (race.id === 'utmb') return <>UTMB’s finish rate stayed within a relatively narrow 61–67% band from 2019 onward. The 2025 field finished at 66.8%, while the men’s winning time fell below 20 hours in four of the last five contested editions.</>; if (race.id === 'western-states') return <>Completion swung by more than 20 points across the decade: 66.0% in 2021 versus 86.5% in 2023. That variation is precisely the context a live newsroom needs before calling a year “fast” or “brutal.”</>; if (race.id === 'hardrock') return <>Hardrock lost two consecutive editions to snow and COVID-19, then returned with a faster winning-time era. The 2021–2025 average is about four hours quicker than the 2017–2018 average.</>; return <>Cocodona is new enough that every edition matters. The overall winning time improved from 72:50:25 in its 2021 debut to 58:47:18 in 2025, while major route changes make course context essential to any comparison.</>; }
