'use client';

import { useState } from 'react';
import Link from '@/components/internal-link';
import {
  ArrowLeft,
  CheckCircle2,
  FlaskConical,
  RefreshCw,
  ShieldCheck,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';

const API_BASE = process.env.NEXT_PUBLIC_ULTRAMEDIA_API_URL || '';
type Draft = {
  disposition: 'draft' | 'insufficient_evidence';
  eyebrow: string;
  headline: string;
  body: string;
  social_caption: string;
  citation_ids: string[];
  claims: { metric: string; value: number; citation_id: string }[];
  reason: string;
};
type Story = Draft & {
  id: string;
  status: string;
  trace_id: string;
  review_revision: number;
  provider: string;
  citations: { id: string; title: string; excerpt: string }[];
  quality_checks: Record<string, unknown>;
};
type Span = {
  stage: string;
  duration_ms: number;
  status: string;
  detail: string;
};
const preview: Draft = {
  disposition: 'draft',
  eyebrow: 'Checkpoint update',
  headline: 'Mara Velez gains places through the canyon sector.',
  body: 'Mara Velez moved from position 31 to position 11 between two checkpoints. This fictional timing update requires editorial review.',
  social_caption:
    'Mara Velez gained 20 places in the fictional checkpoint replay.',
  citation_ids: ['timing-demo'],
  claims: [{ metric: 'position_gain', value: 20, citation_id: 'timing-demo' }],
  reason: '',
};

async function readResponse<T>(response: Response): Promise<T> {
  const payload = await response.json();
  if (!response.ok) {
    const detail =
      typeof payload === 'object' && payload !== null && 'detail' in payload
        ? payload.detail
        : null;
    throw new Error(
      typeof detail === 'string'
        ? detail
        : `Request failed (${response.status})`,
    );
  }
  return payload as T;
}

export default function StudioPage() {
  const [story, setStory] = useState<Story | null>(null);
  const [draft, setDraft] = useState<Draft>(preview);
  const [trace, setTrace] = useState<Span[]>([]);
  const [busy, setBusy] = useState(false);
  const [reviewer, setReviewer] = useState('');
  const [reviewerKey, setReviewerKey] = useState('');
  const [rationale, setRationale] = useState('');
  const [consent, setConsent] = useState(false);
  const [rightsBasis, setRightsBasis] = useState('');
  const [message, setMessage] = useState(
    API_BASE
      ? 'Generate a draft to begin an editorial review.'
      : 'Preview only. Connect the Python API to generate and save reviews.',
  );

  function acceptStory(value: Story) {
    setStory(value);
    setDraft({
      disposition: value.disposition,
      eyebrow: value.eyebrow,
      headline: value.headline,
      body: value.body,
      social_caption: value.social_caption,
      citation_ids: value.citations.map((c) => c.id),
      claims: value.claims,
      reason: value.reason,
    });
  }

  async function generate() {
    setBusy(true);
    setTrace([]);
    try {
      const result = await readResponse<Story>(
        await fetch(`${API_BASE}/api/v1/stories/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            race_id: 'wser-demo',
            moment: {
              athlete_bib: '214',
              signal_type: 'position_gain',
              headline_hint: 'A verified checkpoint position update',
            },
          }),
        }),
      );
      acceptStory(result);
      setMessage(
        'Draft saved. Review its wording, evidence, and numeric claims.',
      );
      try {
        const run = await readResponse<{ spans: Span[] }>(
          await fetch(`${API_BASE}/api/v1/traces/${result.trace_id}`),
        );
        setTrace(run.spans);
      } catch {
        setMessage('Draft saved; its trace is temporarily unavailable.');
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Generation failed.');
    } finally {
      setBusy(false);
    }
  }

  async function review(
    decision: 'approved' | 'revision_requested' | 'rejected',
  ) {
    if (!story) return;
    setBusy(true);
    try {
      const result = await readResponse<Story>(
        await fetch(`${API_BASE}/api/v1/stories/${story.id}/review`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Reviewer-Key': reviewerKey,
          },
          body: JSON.stringify({
            decision,
            reviewer,
            rationale,
            edited_story: draft,
            expected_revision: story.review_revision,
            training_consent: decision === 'approved' && consent,
            rights_basis: rightsBasis,
          }),
        }),
      );
      acceptStory(result);
      setMessage(
        `Revision ${result.review_revision} saved as ${result.status.replaceAll('_', ' ')}. Publication remains a separate editorial action.`,
      );
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : 'Review was not saved.',
      );
    } finally {
      setBusy(false);
    }
  }

  async function evaluate() {
    setBusy(true);
    try {
      const result = await readResponse<{
        suite: string;
        release_decision: string;
        cases: number;
      }>(await fetch(`${API_BASE}/api/v1/evals/run`, { method: 'POST' }));
      setMessage(
        `${result.suite}: ${result.release_decision} across ${result.cases} workflow cases. This does not establish fine-tuning quality.`,
      );
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Evaluation failed.');
    } finally {
      setBusy(false);
    }
  }

  const canReview = Boolean(
    API_BASE && story && reviewer.trim().length >= 2 && !busy,
  );
  return (
    <main className="min-h-screen bg-background text-foreground">
      <header className="border-b border-white/10">
        <nav className="mx-auto flex max-w-7xl flex-wrap items-center gap-6 px-6 py-5 text-sm">
          <Link href="/" className="flex items-center gap-2">
            <ArrowLeft size={18} /> UltraMedia
          </Link>
          <Link href="/week5" className="text-primary">
            Week 5 evidence
          </Link>
          <Link href="/observability">Observability</Link>
          <Badge variant="outline" className="ml-auto">
            {API_BASE ? 'API configured' : 'Fictional preview'}
          </Badge>
        </nav>
      </header>
      <div className="mx-auto max-w-7xl px-6 py-8">
        <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold">Race desk</h1>
            <p className="mt-2 text-base text-muted-foreground">
              Correct a draft, check its evidence, and record your editorial
              decision.
            </p>
          </div>
          <div className="flex gap-3">
            <Button
              variant="outline"
              disabled={!API_BASE || busy}
              onClick={evaluate}
            >
              <FlaskConical /> Check workflow
            </Button>
            <Button disabled={!API_BASE || busy} onClick={generate}>
              {busy ? <RefreshCw className="animate-spin" /> : null} Generate
              draft
            </Button>
          </div>
        </div>
        <p
          role="status"
          className="mb-6 rounded-xl border border-primary/25 bg-primary/5 p-4 text-sm"
        >
          {message}
        </p>
        <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_360px]">
          <section className="space-y-5 rounded-2xl border border-white/10 bg-card p-6">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <h2 className="text-xl font-semibold">Editorial draft</h2>
              <Badge variant="outline">
                {story
                  ? `${story.status} · revision ${story.review_revision}`
                  : 'Unsaved preview'}
              </Badge>
            </div>
            {(['eyebrow', 'headline', 'body', 'social_caption'] as const).map(
              (field) => (
                <label key={field} htmlFor={`draft-${field}`} className="block text-sm font-medium">
                  <span id={`draft-${field}-label`} className="mb-2 block capitalize">
                    {field.replaceAll('_', ' ')}
                  </span>
                  <Textarea
                    id={`draft-${field}`}
                    aria-labelledby={`draft-${field}-label`}
                    value={draft[field]}
                    disabled={!story || busy}
                    maxLength={
                      field === 'social_caption'
                        ? 280
                        : field === 'body'
                          ? 1600
                          : field === 'headline'
                            ? 300
                            : 120
                    }
                    className={
                      field === 'body' ? 'min-h-36 text-base' : 'text-base'
                    }
                    onChange={(event) =>
                      setDraft({ ...draft, [field]: event.target.value })
                    }
                  />
                </label>
              ),
            )}
            <p className="text-sm text-muted-foreground">
              Numeric claims stay tied to the original evidence. Unsupported
              edits are rejected; ask for new evidence when the facts change.
            </p>
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="text-sm">
                Reviewer name
                <Input
                  className="mt-2"
                  value={reviewer}
                  onChange={(event) => setReviewer(event.target.value)}
                  autoComplete="name"
                />
              </label>
              <label className="text-sm">
                Reviewer key, if required
                <Input
                  className="mt-2"
                  type="password"
                  value={reviewerKey}
                  onChange={(event) => setReviewerKey(event.target.value)}
                  autoComplete="off"
                />
              </label>
            </div>
            <label className="block text-sm">
              Review notes
              <Textarea
                className="mt-2"
                value={rationale}
                onChange={(event) => setRationale(event.target.value)}
                maxLength={500}
              />
            </label>
            <label className="flex items-center gap-3 text-sm">
              <Checkbox
                checked={consent}
                onCheckedChange={(checked) => setConsent(Boolean(checked))}
              />
              Allow this approved revision to be exported for training
            </label>
            {consent && (
              <label className="block text-sm">
                Rights and permission basis
                <Input
                  className="mt-2"
                  value={rightsBasis}
                  onChange={(event) => setRightsBasis(event.target.value)}
                  placeholder="For example: organizer permission or authored synthetic material"
                />
              </label>
            )}
            <div className="flex flex-wrap gap-3">
              <Button
                disabled={!canReview || (consent && !rightsBasis.trim())}
                onClick={() => review('approved')}
              >
                <CheckCircle2 /> Save and approve
              </Button>
              <Button
                variant="outline"
                disabled={!canReview}
                onClick={() => review('revision_requested')}
              >
                Request revision
              </Button>
              <Button
                variant="outline"
                disabled={!canReview}
                onClick={() => review('rejected')}
              >
                Reject
              </Button>
            </div>
          </section>
          <aside className="space-y-6">
            <section className="rounded-2xl border border-white/10 bg-card p-5">
              <h2 className="mb-4 text-lg font-semibold">Source evidence</h2>
              {story?.citations.map((c) => (
                <article
                  key={c.id}
                  className="mb-4 border-b border-white/10 pb-4"
                >
                  <p className="text-sm font-medium">{c.title}</p>
                  <p className="mt-2 text-sm text-muted-foreground">
                    {c.excerpt}
                  </p>
                  <code className="mt-2 block break-all text-xs">{c.id}</code>
                </article>
              ))}
              {!story && (
                <p className="text-sm text-muted-foreground">
                  The preview uses fictional positions 31 and 11. Generate a
                  draft for persisted source evidence.
                </p>
              )}
              {draft.claims.map((c, index) => (
                <p className="mt-2 text-sm" key={index}>
                  {c.metric.replaceAll('_', ' ')}: <strong>{c.value}</strong>
                </p>
              ))}
            </section>
            <section className="rounded-2xl border border-white/10 bg-card p-5">
              <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold">
                <ShieldCheck size={18} /> Evidence checks
              </h2>
              {story ? (
                Object.entries(story.quality_checks)
                  .filter(([, value]) => typeof value === 'boolean')
                  .map(([name, value]) => (
                    <p key={name} className="mb-2 text-sm">
                      {value ? '✓' : '×'} {name.replaceAll('_', ' ')}
                    </p>
                  ))
              ) : (
                <p className="text-sm text-muted-foreground">
                  No measured checks for this unsaved preview.
                </p>
              )}
              <p className="mt-4 text-sm text-muted-foreground">
                These checks cover structured facts and known language patterns.
                An editor must still verify meaning and claim support.
              </p>
            </section>
            <section className="rounded-2xl border border-white/10 bg-card p-5">
              <h2 className="mb-4 text-lg font-semibold">Recorded execution</h2>
              <p className="mb-3 break-all text-sm text-muted-foreground">
                {story?.provider || 'No provider run'}
              </p>
              {trace.map((span) => (
                <div key={span.stage} className="mb-3">
                  <p className="flex justify-between gap-2 text-sm">
                    <span>{span.stage.replaceAll('_', ' ')}</span>
                    <span>{span.duration_ms} ms</span>
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {span.detail}
                  </p>
                </div>
              ))}
              {!trace.length && (
                <p className="text-sm text-muted-foreground">
                  A recorded trace appears after generation.
                </p>
              )}
            </section>
          </aside>
        </div>
      </div>
    </main>
  );
}
