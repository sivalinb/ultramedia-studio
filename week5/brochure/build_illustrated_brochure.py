"""Illustration-led brochure. Run from any directory with --output path.pdf.

Uses the approved image_gen artwork unchanged, with exact text, links, chart
and QR codes composed in PDF. No raster image editing is performed here.
Dependencies/font choices match build_brochure.py.
"""
from pathlib import Path
from io import BytesIO
import argparse
import json
from xml.sax.saxutils import escape
import build_brochure as b
import matplotlib.pyplot as plt
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab import rl_config

# Lossless PDF stream encoding; the source artwork remains unchanged.
rl_config.useA85 = 0

HERE=Path(__file__).resolve().parent
WEEK5=HERE.parent
ART=HERE/'art'
THEMES={1:('#562B91','#F0EAF8'),2:('#AF4035','#FFF0EB'),3:('#087D81','#E7F6F4'),
        4:('#225DA6','#EAF2FE'),5:('#95620C','#FFF6DE'),6:('#5A3BA0','#F0EBFC'),
        7:('#397A30','#EBF6E6'),8:('#8D224D','#FBEAF0'),9:('#A65D17','#FFF0DF'),
        10:('#067D9C','#E5F8FB'),11:('#3E692A','#EFF5E8'),12:('#9B4737','#FBEDE7'),
        13:('#8D224D','#FBEAF0'),14:('#34664C','#EAF3EC'),15:('#097A7B','#E8F5F3')}

class Illustrated(b.Brochure):
    page_count=15
    sections=[('Story',1,{1,2,3}),('Workflow',4,{4,14}),('Data',5,{5,6}),('Learning',7,{7}),('Results',8,{8,13}),('Readiness',12,{9,12}),('Pilot',15,{15}),('Sources',11,{10,11})]

    def jump(self,label,target,x,y,w=220):
        self.rect(x,y,w,30,self.accent,r=7)
        self.text(label,x+12,y+7,w-24,10,'#FFFFFF',True,limit=17)
        self.c.linkRect('',f'p{target}',(x,b.PAGE_H-y-30,x+w,b.PAGE_H-y),relative=0,thickness=0)

    def start(self,n,kicker,title,subtitle):
        self.accent,self.tint=THEMES[n]
        b.PURPLE=self.accent
        super().start(n,kicker,title,subtitle)

    def art(self,n,y=151,h=307,x=b.M,w=b.WIDTH):
        self.image(ART/f'page-{n:02d}.png',x,y,w,h)

    def cards(self,items,y=474,h=79,size=10):
        count=len(items);gap=14;w=(b.WIDTH-(count-1)*gap)/count
        for i,(title,body) in enumerate(items):
            x=b.M+i*(w+gap)
            self.rect(x,y,w,h,self.tint,r=9)
            th=self.text(title,x+12,y+10,w-24,11,self.accent,True,limit=30)
            self.text(body,x+12,y+16+th,w-24,size,b.INK,limit=h-th-21)

    def fineprint(self,text,y=543,size=8.5):
        self.text(text,b.M,y,b.WIDTH,size,b.MUTED,limit=20)

    def qr(self,url,x,y,size=60):
        qr=QrCodeWidget(url);box=qr.getBounds();qw,qh=box[2]-box[0],box[3]-box[1]
        drawing=Drawing(size,size,transform=[size/qw,0,0,size/qh,0,0]);drawing.add(qr)
        renderPDF.draw(drawing,self.c,x,b.PAGE_H-y-size)
        self.c.linkURL(url,(x,b.PAGE_H-y-size,x+size,b.PAGE_H-y),relative=0);self.links.append(url)

    def resource(self,label,desc,url,x,y,w=220,size=10):
        h=self.text('<u>'+label+'</u>',x,y,w,size,self.accent,True,limit=28)
        if desc:self.text(desc,x,y+h+3,w,8.5,b.MUTED,limit=24)
        link_height=h+28 if desc else h+3
        self.c.linkURL(url,(x,b.PAGE_H-y-link_height,x+w,b.PAGE_H-y),relative=0)
        self.links.append(url)

    def append_review_pages(self):
        self.start(12,'Race-day readiness / proposed requirements','Know when it happened. Know what changed.',
                   'A cited record can still be stale. These are requirements for a replay pilot, not completed live-feed capabilities.')
        self.art(12,151,254)
        self.cards([('Timestamp + authority','Store event time and received time separately, with timezone, source owner and original record ID. Show last confirmed update and feed freshness.'),
                    ('Status + corrections','Mark provisional, confirmed, corrected or estimated. Keep revisions and superseded IDs. Flag affected drafts for review; handle duplicates and out-of-order arrivals.'),
                    ('Race meaning','Separate overall/category rank and checkpoint IN/OUT. Name projection assumptions. Missing timing means no confirmed update, never an inferred injury or stop.')],y=412,h=114,size=9.2)
        self.text('Read the operational source',b.M,535,260,9,self.accent,True)
        self.c.linkURL('https://www.wser.org/webcast/',(b.M,61,b.M+260,79),relative=0)
        self.links.append('https://www.wser.org/webcast/')
        self.text('WSER describes manual timing, variable connectivity and radio fallback. Reviewed 09 Sep 2026.',310,535,440,8.5,b.MUTED,limit=25)
        self.end(12,'https://www.wser.org/webcast/')

        self.start(13,'Actual saved case / automatic-check blind spot','Passing checks can still hide wrong meaning.',
                   'First case in test-file order. Headline and body excerpts are verbatim. Synthetic evidence, not a real runner.')
        case=json.loads((HERE/'saved-case.json').read_text())
        self.art(11,164,154,625,112)
        self.rect(b.M,167,561,144,self.tint,r=9)
        self.text('EXACT INPUT VALUES / '+case['id'],b.M+12,177,537,10,self.accent,True)
        self.text('Avery Hill / bib 220 / position_gain<br/>Valley station: mile 48, elapsed 30,827 seconds, overall position 34.<br/>Ridge station: mile 62, elapsed 35,627 seconds, overall position 35.<br/>Evidence fact: position_gain = -1. Hint: "Prepare a short factual update."',b.M+12,198,537,10,b.INK,limit=70)
        self.text('Citation ID: fictional-race-120-position_gain-timing',b.M+12,263,537,9,b.INK)
        self.text('Source: synthetic://fictional-race-120/position_gain',b.M+12,281,537,9,b.MUTED)
        for i,arm in enumerate(('base','adapter')):
            x=b.M+i*361;out=case[arm]['output']
            self.rect(x,323,347,157,self.tint,r=9)
            self.text(('BASE' if i==0 else 'ADAPTED')+' / saved output',x+12,333,323,11,self.accent,True)
            self.text('<b>Headline:</b> '+escape(out['headline']),x+12,355,323,10,b.INK,limit=43)
            self.text('<b>Body:</b> '+escape(out['body']),x+12,391,323,9.4,b.INK,limit=76)
        self.text('Frozen validator: all eight constituent checks PASS for BOTH outputs.',b.M,491,b.WIDTH,11,self.accent,True)
        self.text('Document review: 34th to 35th is one place lost. Base prose reverses the meaning; adapted prose says lost but retains "1 places". Independent race-editor judgment remains pending.',b.M,513,b.WIDTH,10,b.INK,limit=32)
        self.resource('Open exact input','',b.GIT+'data/synthetic/test.jsonl',b.M,549,180,8.5)
        self.resource('Open raw base output','',b.GIT+'evidence/local-comparison/test-base/predictions.jsonl',281,549,180,8.5)
        self.resource('Open raw adapted output','',b.GIT+'evidence/local-comparison/test-adapter/predictions.jsonl',520,549,220,8.5)
        self.end(13,b.GIT+'reports/LOCAL_COMPARISON_RESULTS.md')

        self.start(14,'Actual application / recorded local execution','The interface behind the illustrations.',
                   'Unaltered saved browser screenshot: trained adapter served locally with fictional timing. Captured during automated QA.')
        screenshot=WEEK5/'evidence/adapter-serving/01-generated-desktop.png'
        self.image(screenshot,b.M,164,379,382)
        url=b.GIT+'evidence/adapter-serving/01-generated-desktop.png'
        self.c.linkURL(url,(b.M,66,421,448),relative=0);self.links.append(url)
        self.art(11,163,135,590,105)
        self.text('REAL UI',446,176,132,17,self.accent,True)
        self.text('Recorded proof of the local workflow. Click the screenshot to inspect it at full resolution.',446,205,138,10,b.INK,limit=72)
        panels=[('Draft + evidence','The candidate and supplied timing facts appear together. The saved example shows Mara Velez moving from 20th to 11th.'),
                ('Checks + trace','Bounded checks and workflow spans are visible. Green checks do not establish full semantic correctness.'),
                ('Review remains human','The screenshot is pending_review. Automated QA review actions are not independent editorial approval. Publishing is separate.')]
        for i,(title,body) in enumerate(panels):
            y=305+i*79;self.rect(444,y,306,72,self.tint,r=8)
            self.text(title,456,y+9,282,11,self.accent,True)
            self.text(body,456,y+29,282,9.4,b.INK,limit=39)
        self.end(14,b.GIT+'evidence/adapter-serving/README.md')

        self.start(15,'Proposed pilot / participation brief','Help test the value with a supervised replay.',
                   'Seeking a permissioned historical export and two independent race-media reviewers. No pilot is booked or completed.')
        self.art(15,151,218)
        self.cards([('Freeze before testing','One historical event; 30 new cases, 3 approaches, 2 reviewers. Include normal, late, corrected, duplicate, conflicting and missing updates. Label injected faults.'),
                    ('Compare independently','Rules vs prompted base vs adapted model. Anonymize and counterbalance order. Record factual errors, holds, acceptance, correction time and cost per accepted brief.'),
                    ('Proposed decision gates','Zero critical false assertions; no worse major-error rate or acceptance than rules; at least 20% lower median review time vs best comparator and no higher accepted-brief cost.')],y=374,h=123,size=9)
        self.rect(b.M,506,b.WIDTH,45,self.tint,r=8)
        self.text('NEXT STEP: bring an approved export, source/version details and two reviewers; agree and freeze the protocol before running.',b.M+12,514,b.WIDTH-24,10,self.accent,True,limit=29)
        self.fineprint('Proposed thresholds, not measured outcomes. Thirty cases are exploratory. No live publication; failed gates mean revise or keep rules.',554,7.8)
        self.end(15,b.GIT+'project/HUMAN_REVIEW.md')

    def build(self):
        self.start(1,'The product in one picture','Race evidence in. Reviewed stories out.',
                   'For race organizers with small media teams: bring sources, cited drafts and review into one workspace.')
        self.art(1,160,354)
        self.link('Explore the product',b.DEMO,b.M,522,194,fill=self.accent)
        self.jump('Plan a supervised replay',15,250,522,207)
        self.text('First-customer hypothesis; no pilot completed.<br/>Public demo includes recorded examples.',477,526,273,9,b.MUTED,limit=28)
        self.end(1,b.GIT+'project/PRODUCT_PITCH.md')

        self.start(2,'The current problem and the solution','From scattered updates to a reviewable story.',
                   'Editors need to connect the facts, avoid unsupported claims and preserve the decisions behind a draft.')
        self.art(2)
        self.cards([('Scattered facts','Gather timing and course context in one evidence view.'),
                    ('Uncertain claims','Check citations and numbers; hold when support is missing.'),
                    ('Repeated drafting','Prepare a headline, body and short social caption.'),
                    ('Review history','Keep originals, edits and protected approval actions.')],y=466,h=78,size=9.5)
        self.fineprint('Targeted workflow benefits; real-world time savings and error reduction still need editor testing.',551,8)
        self.end(2,b.GIT+'project/BUSINESS_CASE.md')

        self.start(3,'Who can use it','Start with a small race media team.',
                   'First-customer hypothesis: an organizer coordinating a small editorial team. Validate demand through interviews.')
        self.art(3)
        self.cards([('Primary buyer','Race organizer: evaluate coverage, reviewer workload and source access.'),
                    ('Primary user','Media editor: verify evidence, correct meaning and approve a version.'),
                    ('Collaborator','Event creator: reuse a reviewed brief for a caption or announcer note.'),
                    ('Later audience','Running community: read reviewed updates. Crew logistics need more proof.')],y=466,h=78,size=9.5)
        self.fineprint('Creator likeness illustrates roles, not customers. Media reporting is the pilot focus; crew navigation and safety decisions are outside scope.',551,8)
        self.end(3,b.GIT+'project/PRODUCT_PITCH.md')

        self.start(4,'How it works','Choose. Retrieve. Draft. Validate. Review.',
                   'An orchestrated AI workflow with human review. Current stages follow a predefined sequence.')
        self.art(4)
        self.cards([('Recommended division of work','Code calculates facts; evidence rules gate support; the model drafts wording; bounded validators check outputs; an editor checks meaning.'),
                    ('Current boundary','Fixed LangGraph stages, not autonomous investigation. The full rule-first gate is a proposed refinement. Approval saves a version; external publishing is separate.')],y=466,h=87,size=10)
        self.end(4,b.REPO+'backend/src/ultramedia/workflow.py')

        self.start(5,'Where the data comes from','Three sources. Three different purposes.',
                   'The training corpus, demo context and measured execution evidence have separate provenance. Source register: page 11.')
        self.art(5,147,302)
        self.cards([('Authored research [S1, S2]','600 fictional records from dataset.py; generator seed 20260908; synthetic:// source IDs. CC0-1.0 records, zero human approvals. No scraped results or teacher outputs.'),
                    ('Static demo [S3-S6]','7 simulated timings for 2 fictional athletes; 5 context chunks. Four chunks cite official Western States course, guide or history pages; one is product policy.'),
                    ('Real execution [S7, S8]','Project-generated Colab logs and Mac predictions, checks and token receipts. Actual runs on synthetic inputs; no live vendor feed or real-race validation is claimed.')],y=453,h=101,size=9.1)
        self.end(5,b.GIT+'DATA_CARD.md')

        self.start(6,'What is considered','Read the signal. Check the evidence.',
                   'Four signal types (150 records each) and five evidence conditions (120 each) make a controlled research task.')
        self.art(6,149,251)
        self.rect(b.M,402,b.WIDTH,39,self.tint,r=7)
        self.text('APP DEMO: position facts derived from stored timings.',b.M+12,408,b.WIDTH-24,10,self.accent,True)
        self.text('RESEARCH ONLY: record projection, cutoff buffer and pace change supplied synthetically; no operational calculators shown.',b.M+12,425,b.WIDTH-24,8.4,b.INK)
        self.cards([('Programmed ranges and units [S1]','Position: -8 to +19 places; positive means gained.<br/>Record margin: -180 to +240 sec; positive means ahead.<br/>Cutoff: -12 to +42 min; positive means time remaining.<br/>Pace: -35 to +50 sec/mile; negative means faster.'),
                    ('Fields in each request [S9]','Moment: bib, signal type and headline hint.<br/>Timing: name/bib, checkpoint, mile, elapsed seconds, position.<br/>Evidence: ID, title, URL, excerpt, score and metric/value facts.<br/>Reference answers are not passed into inference.')],y=450,h=93,size=9)
        self.fineprint('Ranges are synthetic design choices. Boundary cases use zero; missing/conflicting cases alter the evidence.',550,8)
        self.end(6,b.REPO+'backend/src/ultramedia/dataset.py')

        self.start(7,'The Week 5 learning story','Teach the behavior. Supply the current facts.',
                   'Prompting defines the task; retrieval supplies evidence; supervised fine-tuning adapts the response behavior.')
        self.art(7)
        self.cards([('Data','600 synthetic examples: 400 train / 80 validation / 120 test. Race groups do not cross splits.'),
                    ('Train and merge','Qwen3 4B, rank-16 QLoRA, 2 epochs, 100 steps. 33,030,144 trainable parameters; merged for local serving.'),
                    ('Compare fairly','Same prompt, Q4_K_M runtime and 120 cases locally. Fireworks RFT and teacher distillation have not been run.')],y=466,h=87,size=9.5)
        self.end(7,b.GIT+'project/AGENDA_COVERAGE.md')

        self.start(8,'Measured results','A measurable gain. Failures remain visible.',
                   'Matched local comparison: the same base lineage, prompt, Q4_K_M runtime and schema constraints for both models.')
        self.art(8)
        result=json.loads((WEEK5/'evidence/local-comparison/comparison/comparison.json').read_text())
        counts=[round(result[arm]['metrics']['automatic_success']*result[arm]['cases']) for arm in ('base','adapter')]
        assert counts==[76,109] and result['automatic_success_delta']==.275
        vals=[n/120*100 for n in counts]
        fig,ax=plt.subplots(figsize=(3.5,2.65),dpi=220)
        ax.barh([1,0],vals,height=.43,color=['#B3A4AE',self.accent])
        ax.set_yticks([1,0],['Base','Adapted']);ax.set_xlim(0,119)
        ax.set_xticks([0,50,100],['0%','50%','100%']);ax.tick_params(length=0,pad=6,labelsize=10)
        for sp in ax.spines.values():sp.set_visible(False)
        ax.grid(axis='x',color='#EEE5EA');ax.set_axisbelow(True)
        for y,value,count in zip([1,0],vals,counts):ax.text(value+2,y,f'{value:.1f}%\n{count}/120',va='center',fontsize=10,fontweight='bold',color=b.INK)
        ax.set_title('All-check success',fontsize=12,loc='left',pad=15)
        fig.subplots_adjust(left=.21,right=.99,top=.81,bottom=.16)
        pic=BytesIO();fig.savefig(pic,format='png',dpi=220);plt.close(fig);pic.seek(0)
        self.image(pic,b.M,165,330,245)
        self.text('120 SYNTHETIC CASES / AUTOMATIC CHECKS',b.M+12,397,324,9,self.accent,True)
        self.text('HUMAN REVIEW PENDING',b.M+12,411,324,9,self.accent,True)
        self.text('+27.5 percentage points',b.M+12,431,324,17,self.accent,True)
        self.text('Paired 95% interval: +20 to +35 points',b.M+12,454,324,9,b.MUTED)
        self.cards([('Metric limitation','Eight checks; schemas 120/120 in both arms. Keyword checks can penalize denials of injury claims. This is not a measured reduction in false stories.'),
                    ('Negative evidence','11 adapted failures are unnecessary holds. Five new probes: base 3/5, adapted 3/5. Rules pass 120/120 engineered cases.'),
                    ('Scope and pending work','The interval covers this experiment, not real-race variation. Human review and GPU control remain open. 13 app checks passed; one quality case failed.')],y=477,h=77,size=8.5)
        self.end(8,b.GIT+'reports/LOCAL_COMPARISON_RESULTS.md')

        self.start(9,'Proposed product roadmap','Prove reliability. Earn trust. Then expand.',
                   'Current capability, proposed next steps and conditional future options. No delivery dates or funding commitments implied.')
        self.art(9)
        self.cards([('Now: research','Cited drafts, local open model and evidence reports. Human benefit is not measured.'),
                    ('Next: reliability','Add time/source status and correction handling; fix semantic gaps on fresh cases. See page 12.'),
                    ('Pilot: editor value','Permissioned historical replay; blind rules/base/adapter review. Predeclare gates on page 15.'),
                    ('Later: expand','Expand only after editor benefit. Add integrations/team access; assess hosting when needed.')],y=466,h=80,size=9)
        self.fineprint('Gate expansion on editor benefit, acceptable errors and cost/privacy checks. RFT requires validated rewards.',552,8)
        self.end(9,b.GIT+'PROJECT_REPORT.md')

        self.start(10,'Explore at your own pace','Explore today. Prepare a supervised replay.',
                   'Start with recorded work, then inspect a real saved case and the proposed independent-review plan.')
        self.art(10,149,253)
        self.jump('Saved model case',13,b.M,407,220)
        self.jump('Actual application',14,286,407,220)
        self.jump('Replay brief / next steps',15,530,407,220)
        resources=[('Project report',b.GIT+'PROJECT_REPORT.md'),('Training receipts',b.TREE+'reports/data/final-training'),
                   ('Data and provenance',b.GIT+'reports/DATA_REPORT.md'),('Paired comparison',b.GIT+'reports/LOCAL_COMPARISON_RESULTS.md'),
                   ('Case-level CSV',b.GIT+'reports/data/local-comparison-cases.csv'),('Week 5 agenda',b.GIT+'project/AGENDA_COVERAGE.md'),
                   ('Technical visual',b.GIT+'diagrams/week5-end-to-end-illustrated.png'),('Recorded walkthrough',b.GIT+'evidence/handout-page/project-walkthrough.webm')]
        for i,(label,url) in enumerate(resources):
            x=b.M+(i%2)*257;y=456+(i//2)*23
            self.resource(label,'',url,x,y,w=240,size=10)
        self.qr(b.DEMO,605,452,62);self.qr(b.HUB,687,452,62)
        self.text('Product',611,519,63,9,self.accent,True);self.text('Evidence',688,519,64,9,self.accent,True)
        self.fineprint('The public demo includes recorded examples. A recorded replay is not live cloud model inference.',549,8.5)
        self.end(10,b.GIT+'PROJECT_REPORT.md')

        self.start(11,'Source details and provenance','Open the source behind the story.',
                   'S1-S16 identify the creator, source location and role. Official sites checked 09 Sep 2026; Git links are pinned.')
        self.art(11,162,363,b.M,242)
        sources=[
            ('S1  UltraMedia generator','dataset.py: authored values, conditions and targets.',b.REPO+'backend/src/ultramedia/dataset.py'),
            ('S2  Dataset manifest','Frozen corpus counts, splits, version and file hashes.',b.GIT+'data/synthetic/manifest.json'),
            ('S3  Demo fixture','sample_race.json: simulated timing; context attributions.',b.REPO+'backend/data/sample_race.json'),
            ('S4  WSER official site','wser.org: course profile and canyon context.', 'https://www.wser.org/'),
            ('S5  WSER participant guide','wser.org/participant-guide/: finish-window context.', 'https://www.wser.org/participant-guide/'),
            ('S6  WSER history','wser.org/year-by-year/: historical context only.', 'https://www.wser.org/year-by-year/'),
            ('S7  Training receipts','Project Colab logs, loss history and verification.',b.TREE+'reports/data/final-training'),
            ('S8  Local comparison','Project Mac runs, raw predictions and failures.',b.GIT+'reports/LOCAL_COMPARISON_RESULTS.md'),
            ('S9  Input/output contract','contracts.py: fields, units and bounded checks.',b.REPO+'backend/src/ultramedia/contracts.py'),
            ('S10  Qwen publisher','Qwen3-4B-Instruct-2507 weights; Apache 2.0.', 'https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507'),
            ('S11  Dataset inventory','All 600 records: provenance and content hashes.',b.GIT+'reports/data/dataset-inventory.csv'),
            ('S12  External CSV path','ingestion.py: importer; no live vendor feed evidenced.',b.REPO+'backend/src/ultramedia/ingestion.py'),
            ('S13  WSER webcast','Operational context: manual timing and radio fallback.', 'https://www.wser.org/webcast/'),
            ('S14  Saved base output','Unchanged predictions; page 13 uses first case.',b.GIT+'evidence/local-comparison/test-base/predictions.jsonl'),
            ('S15  Saved adapted output','Same case and input hash; no editorial rewrite.',b.GIT+'evidence/local-comparison/test-adapter/predictions.jsonl'),
            ('S16  Application screenshot','Recorded local adapter QA; synthetic timing.',b.GIT+'evidence/adapter-serving/01-generated-desktop.png'),
        ]
        for i,(label,desc,url) in enumerate(sources):
            x=302+(i%2)*230;y=163+(i//2)*43
            self.resource(label,desc,url,x,y,218,10)
        self.text('Dataset SHA-256',302,513,448,9,self.accent,True)
        self.text('5c148b3d1e57a989e38c55e73f1d46ae0b5b17227be154457953bac2dcaef8cf',302,529,448,8,b.INK)
        self.fineprint('CC0 applies to authored synthetic records, not official references. External timing/editorial data needs appropriate rights and consent.',549,8.2)
        self.end(11,b.GIT+'DATA_CARD.md')
        self.append_review_pages()
        self.c.save()
        return {'pages':15,'source_snapshot':b.SNAPSHOT,'external_links':self.links,'artwork_pages':list(range(1,16)),'text_blocks':self.boxes}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'UltraMedia-Brochure.pdf');ap.add_argument('--qa-json',type=Path)
    args=ap.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    b.fonts();receipt=Illustrated(args.output).build()
    if args.qa_json:args.qa_json.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'pages':receipt['pages'],'links':len(receipt['external_links'])}))

if __name__=='__main__':main()
