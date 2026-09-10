"""Build the eleven-page, clickable UltraMedia product/evidence brochure.

Run: python week5/brochure/build_brochure.py --output UltraMedia-Brochure.pdf
Dependencies: reportlab, matplotlib, pillow. Source evidence is pinned.
The original personal reference photographs are intentionally not included.
"""
from pathlib import Path
from io import BytesIO
import argparse
import json
import os

os.environ.setdefault('MPLCONFIGDIR', '/tmp/ultramedia-brochure-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

HERE = Path(__file__).resolve().parent
WEEK5 = HERE.parent
SNAPSHOT = 'cc8f42cbc73f6efe92c49d21437f4e4b16fd1089'
REPO = f'https://github.com/sivalinb/ultramedia-studio/blob/{SNAPSHOT}/'
GIT = REPO + 'week5/'
TREE = f'https://github.com/sivalinb/ultramedia-studio/tree/{SNAPSHOT}/week5/'
DEMO = 'https://ultramedia-studio.siva-babu.chatgpt.site/'
HUB = DEMO + 'week5'
PURPLE, INK, MUTED = '#562B91', '#20223C', '#626678'
LILAC, GREEN, PALE = '#F0EAF8', '#24745B', '#EAF5EF'
AMBER, CREAM, LINE = '#9B650C', '#FFF5DD', '#E1DCEA'
PAGE_W, PAGE_H, M = 792, 612, 42
WIDTH = PAGE_W - 2*M

def fonts():
    pairs = [
        ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
        ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
    ]
    for normal, bold in pairs:
        if Path(normal).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont('Body', normal))
            pdfmetrics.registerFont(TTFont('Strong', bold))
            pdfmetrics.registerFontFamily('Body', normal='Body', bold='Strong')
            return
    raise RuntimeError('Install Arial or DejaVu Sans regular and bold fonts.')

class Brochure:
    def __init__(self, output):
        self.c = canvas.Canvas(str(output), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
        self.c.setTitle('UltraMedia Race Desk | From race updates to reviewed stories')
        self.c.setAuthor('Siva Babu | UltraMedia Studio')
        self.c.setSubject('Product brochure, workflow, Week 5 fine-tuning results and evidence links')
        self.links = []
        self.boxes = []

    def text(self, text, x, y, w, size=12, color=INK, bold=False, limit=None, leading=None):
        style = ParagraphStyle('p', fontName='Strong' if bold else 'Body', fontSize=size,
                               leading=leading or size*1.32, textColor=HexColor(color))
        para = Paragraph(text, style)
        _, h = para.wrap(w, PAGE_H)
        if limit is not None:
            assert h <= limit + .1, (text, h, limit)
        assert y+h <= PAGE_H-20, (text, y+h)
        para.drawOn(self.c, x, PAGE_H-y-h)
        self.boxes.append({'page':self.c.getPageNumber(), 'x':x,'y':y,'w':w,'h':h})
        return h

    def rect(self,x,y,w,h,fill=white,stroke=None,r=12):
        self.c.setFillColor(HexColor(fill) if isinstance(fill,str) else fill)
        self.c.setStrokeColor(HexColor(stroke or fill) if isinstance(stroke or fill,str) else fill)
        self.c.roundRect(x,PAGE_H-y-h,w,h,r,fill=1,stroke=bool(stroke))

    def line(self,x1,y1,x2,y2,color=LINE,width=1):
        self.c.setStrokeColor(HexColor(color)); self.c.setLineWidth(width)
        self.c.line(x1,PAGE_H-y1,x2,PAGE_H-y2)

    def arrow(self,x1,y,x2,color=PURPLE):
        self.line(x1,y,x2,y,color,1.6)
        self.line(x2-5,y-3,x2,y,color,1.6); self.line(x2-5,y+3,x2,y,color,1.6)

    def number(self,n,x,y,color=PURPLE):
        self.c.setFillColor(HexColor(color)); self.c.circle(x+12,PAGE_H-y-12,12,fill=1,stroke=0)
        self.c.setFont('Strong',11);self.c.setFillColor(white)
        self.c.drawCentredString(x+12,PAGE_H-y-16,str(n))

    def link(self,label,url,x,y,w=180,h=32,fill=PURPLE):
        self.rect(x,y,w,h,fill,r=7)
        self.text(label,x+12,y+8,w-24,11,white.hexval(),True,limit=h-10)
        self.c.linkURL(url,(x,PAGE_H-y-h,x+w,PAGE_H-y),relative=0)
        self.links.append(url)

    def image(self,path,x,y,w,h):
        self.c.drawImage(ImageReader(path),x,PAGE_H-y-h,w,h,preserveAspectRatio=True,anchor='c',mask='auto')

    def start(self,n,kicker,title,subtitle):
        self.c.bookmarkPage(f'p{n}');self.c.addOutlineEntry(title,f'p{n}',level=0,closed=False)
        self.text('ULTRAMEDIA / RACE DESK',M,22,220,9,PURPLE,True)
        sections=getattr(self,'sections',[('Story',1,{1,3}),('Problem',2,{2}),('Workflow',4,{4}),('Data',5,{5,6}),('Learning',7,{7}),('Results',8,{8}),('Roadmap',9,{9}),('Sources',11,{10,11})])
        for i,(label,target,active_pages) in enumerate(sections):
            x=286+i*58;active=n in active_pages
            self.text(label,x,22,56,8.5,PURPLE if active else MUTED,active)
            self.c.linkRect('',f'p{target}',(x,PAGE_H-37,x+56,PAGE_H-18),relative=0,thickness=0)
        self.line(M,46,PAGE_W-M,46)
        self.text(kicker.upper(),M,62,WIDTH,9,GREEN,True)
        self.text(title,M,82,WIDTH,28,INK,True,limit=70)
        self.text(subtitle,M,123,WIDTH,12,MUTED,limit=36)

    def end(self,n,source=None):
        self.line(M,566,PAGE_W-M,566)
        self.text('RESEARCH PROTOTYPE  /  Human review required  /  09 SEP 2026',M,577,490,8,MUTED)
        if source:
            self.text('Source evidence',568,577,113,8,PURPLE,True)
            self.c.linkURL(source,(568,22,681,37),relative=0); self.links.append(source)
        self.text(f'{n:02d} / {getattr(self,"page_count",11)}',698,577,52,8,MUTED,True)
        self.c.showPage()

    def build(self):
        # 1. Sales story: reuse the approved personalized illustration intact.
        self.start(1,'Understand it in 30 seconds','Race evidence in. Reviewed stories out.',
                   'A race-reporting workspace that brings sources, cited drafts and editorial decisions together.')
        self.image(WEEK5/'diagrams/ultramedia-product-pitch-siva.png',M,166,WIDTH,354)
        self.link('Explore the product',DEMO,M,524,194)
        self.link('Jump to the evidence',HUB,250,524,207)
        self.text('Meet the workflow first. Inspect every claim next.',477,530,271,10,MUTED,limit=28)
        self.end(1,GIT+'project/PRODUCT_PITCH.md')

        # 2. Explain the current workflow problem and its product counterpart.
        self.start(2,'The current problem and the solution','Race updates move fast. Verification takes work.',
                   'The editorial challenge: connect scattered facts, handle uncertainty and keep decisions traceable.')
        for x,w,label,fill,color in [(M,210,'CURRENT PROBLEM',CREAM,AMBER),(268,280,'HOW ULTRAMEDIA ADDRESSES IT',LILAC,PURPLE),(564,186,'WHAT THE EDITOR GETS',PALE,GREEN)]:
            self.rect(x,169,w,30,fill,r=6)
            self.text(label,x+12,179,w-24,9,color,True)
        rows=[
            ('Scattered race facts','Timing updates and course context need to be reconciled.',
             'Bring evidence into one view','Retrieve facts relevant to the selected race moment.',
             'Traceable context','Inspect the sources behind the story.'),
            ('Unsupported claims','Missing or conflicting facts can become confident prose.',
             'Draft with citations or hold','Check citation IDs and numeric claims; flag insufficient evidence.',
             'Visible uncertainty','See what supports a claim and what is missing.'),
            ('Repeated draft assembly','Headlines, body copy and captions need a consistent starting point.',
             'Prepare a structured candidate','Generate a headline, body, social caption and structured claims.',
             'A reviewable draft','Edit a candidate in the same workspace.'),
            ('Review without a trail','Edits and approval decisions need to remain traceable.',
             'Keep review history','Preserve original drafts, revisions and protected approval actions.',
             'Editorial control','Approve a version; publishing remains a separate action.'),
        ]
        for i,row in enumerate(rows):
            y=211+i*81
            for x,w,title,body,fill,color in [(M,210,row[0],row[1],CREAM,AMBER),(268,280,row[2],row[3],LILAC,PURPLE),(564,186,row[4],row[5],PALE,GREEN)]:
                self.rect(x,y,w,72,fill,r=8)
                self.text(title,x+12,y+10,w-24,12,color,True,limit=18)
                self.text(body,x+12,y+33,w-24,10,INK,limit=32)
            self.arrow(254,y+36,264)
            self.arrow(552,y+36,560)
        self.text('These are the workflow problems the prototype targets. Time saved and real-world error reduction still need editor testing.',M,540,WIDTH,9,MUTED)
        self.end(2,GIT+'project/BUSINESS_CASE.md')

        # 3. Audience and concrete product value, without invented commercial claims.
        self.start(3,'Who can use it','For the people behind every race update.',
                   'Designed for teams that need to explain what changed, show the source and keep an editor in control.')
        cards=[('01','Race organizers','Prepare event updates from timing facts and course context.','Clearer event communications'),
               ('02','Sports editors','Inspect citations and revise the story before approving a version.','A reviewable editorial draft'),
               ('03','Event media teams','Start with a structured story and a short social caption.','A shared starting point'),
               ('04','Running communities','Explain position, pace, cutoff and record-projection signals.','Race moments with context')]
        for i,(n,title,body,benefit) in enumerate(cards):
            x=M+(i%2)*363; y=169+(i//2)*134
            self.rect(x,y,345,118,LILAC)
            self.text(n,x+16,y+15,28,10,PURPLE,True)
            self.text(title,x+50,y+14,278,17,INK,True)
            self.text(body,x+16,y+45,313,11,limit=34)
            self.text(benefit,x+16,y+91,313,10,GREEN,True)
        self.rect(M,442,WIDTH,91,CREAM)
        self.text('The product promise',M+18,456,170,12,AMBER,True)
        self.text('One place to move from a race signal to a sourced draft, a documented check and an editorial decision.',
                  M+204,456,484,15,INK,True,limit=44)
        self.text('Intended audiences and benefits; no customer adoption, time savings or revenue claim is implied.',M+18,512,670,9,MUTED)
        self.end(3,GIT+'project/PRODUCT_PITCH.md')

        # 4. Product walkthrough. The numerical example is explicitly illustrative.
        self.start(4,'How it works','A visible path from signal to editorial decision.',
                   'The model prepares a candidate. Validation and human review determine what happens next.')
        steps=[('Choose','Select a race moment.'),('Retrieve','Gather relevant evidence.'),('Draft','Generate cited, structured text.'),('Validate','Check format, IDs and claims.'),('Review','Inspect, edit and approve a version.')]
        for i,(title,body) in enumerate(steps):
            x=M+i*144
            self.rect(x,169,132,106,LILAC)
            self.number(i+1,x+12,180)
            self.text(title,x+12,212,108,14,PURPLE,True)
            self.text(body,x+12,234,108,10,limit=32)
            if i<4:self.arrow(x+134,221,x+142)
        self.rect(M,293,222,190,'#F6F6FA',LINE)
        self.text('EVIDENCE',M+16,308,190,9,PURPLE,True)
        self.text('A supported position change',M+16,330,190,15,INK,True)
        self.text('Previous position: <b>8</b><br/>Latest position: <b>5</b><br/>Places gained: <b>3</b><br/>Source ID: <b>timing-01</b>',M+16,376,190,12,limit=78)
        self.rect(282,293,270,190,PALE)
        self.text('CANDIDATE DRAFT',298,308,238,9,GREEN,True)
        self.text('Runner gains three places',298,330,238,17,INK,True)
        self.text('The runner moved from eighth to fifth, gaining three places. [timing-01]',298,379,238,12,limit=48)
        self.text('Headline + body + social caption<br/>Citations + structured claims',298,444,238,10,GREEN,limit=28)
        self.rect(570,293,180,190,CREAM)
        self.text('IF EVIDENCE IS MISSING',586,308,148,9,AMBER,True)
        self.text('Hold the claim.',586,347,148,18,INK,True)
        self.text('Return an insufficient-evidence decision with a reason. The model can still make mistakes.',586,385,148,11,limit=78)
        self.text('Illustrative example, not a saved model output or real race result.',M,493,WIDTH,9,MUTED)
        self.rect(M,516,WIDTH,34,LILAC,r=7)
        self.text('Editor control: source inspection, protected revisions and history. Approval does not publish externally.',M+12,526,WIDTH-24,10,INK,limit=18)
        self.end(4,GIT+'PROJECT_REPORT.md')

        # 5. Explicit provenance: authored research, static demo and execution receipts.
        self.start(5,'Data provenance','Three sources. Three different purposes.',
                   'The training corpus, application demo and measured experiment outputs must be read separately.')
        blocks=[
            (171,105,'01 / TRAINING','Authored synthetic corpus',LILAC,PURPLE,
             'UltraMedia dataset.py generates 600 fictional chat records with seed 20260908. Values and target stories come from programmed rules; source IDs use synthetic://. [S1, S2]',
             'CC0-1.0 for these records. Zero human-approved examples; no scraped race results or teacher-model outputs.'),
            (288,108,'02 / APPLICATION','Static race simulation',PALE,GREEN,
             'sample_race.json contains 7 simulated timing events for 2 fictional athletes, plus 5 context chunks: 4 attributed to official Western States pages and 1 product policy. [S3-S6]',
             'Course/rules/history references provide context. Athlete names and timing values are simulated, not official live results.'),
            (408,99,'03 / EVALUATION','Actual run receipts',LILAC,PURPLE,
             'Colab training logs and local Mac model outputs were generated by this project. Reports retain raw predictions, case checks, token receipts and conversion lineage. [S7, S8]',
             'Real execution on synthetic inputs. The 120 held-out cases are not real-race validation or editor judgments.'),
        ]
        for y,h,label,title,fill,color,body,note in blocks:
            self.rect(M,y,WIDTH,h,fill)
            self.text(label,M+16,y+14,178,9,color,True)
            self.text(title,M+16,y+37,178,16,INK,True,limit=45)
            self.text(body,M+220,y+13,472,11,INK,limit=48)
            self.text(note,M+220,y+h-38,472,9,color,True,limit=29)
        self.text('Current demo derives position facts from stored timing. Other research signals use supplied synthetic measurements.',M,523,WIDTH,10,MUTED,limit=28)
        self.end(5,GIT+'DATA_CARD.md')

        # 6. The fields, units and deliberate experimental factors.
        self.start(6,'What the model considers','Inputs, units and difficult evidence conditions.',
                   'Each request carries moment, timing and evidence. Reference answers are kept out of inference inputs. [S1, S9]')
        inputs=[('Moment','Athlete bib, signal type and a headline hint. The hint cannot override the facts.'),
                ('Timing','Athlete name/bib, checkpoint, mile, elapsed seconds and overall position.'),
                ('Evidence','Citation ID, title, source URL, excerpt, retrieval score and any metric/value facts.')]
        for i,(title,body) in enumerate(inputs):
            x=M+i*242;self.rect(x,169,224,91,LILAC)
            self.text(title,x+14,182,196,14,PURPLE,True)
            self.text(body,x+14,211,196,10,INK,limit=40)
        self.text('Four signal types - 150 records each',M,278,WIDTH,16,INK,True)
        self.rect(M,310,WIDTH,24,PURPLE,r=0)
        for x,w,t in [(M+10,150,'SIGNAL'),(214,157,'GENERATOR RANGE'),(393,345,'MEANING / UNIT')]:
            self.text(t,x,317,w,9,white.hexval(),True)
        metrics=[('Position change','-8 to +19 places','Positive = gained; zero = unchanged.'),
                 ('Record projection','-180 to +240 seconds','Positive = ahead of target; not an achieved record.'),
                 ('Cutoff buffer','-12 to +42 minutes','Positive = time remaining; negative = beyond cutoff.'),
                 ('Pace change','-35 to +50 sec/mile','Negative = faster; positive = slower.')]
        for i,(signal,ran,meaning) in enumerate(metrics):
            y=334+i*27;self.rect(M,y,WIDTH,27,'#F4F1F8' if i%2==0 else '#FAF9FC',r=0)
            self.text(signal,M+10,y+7,152,10,INK,True)
            self.text(ran,214,y+7,166,10,INK)
            self.text(meaning,393,y+7,347,10,INK)
        self.text('Five evidence conditions - 120 records each',M,457,WIDTH,14,INK,True)
        for i,label in enumerate(['Complete','Missing','Conflicting','Misleading hint','Zero / boundary']):
            x=M+i*144;self.rect(x,485,132,28,PALE,r=6);self.text(label,x+10,493,112,10,GREEN,True)
        self.text('Ranges are programmed, not observed race limits. Boundary cases use zero; missing/conflicting cases alter evidence.',M,527,WIDTH,9,MUTED,limit=24)
        self.end(6,REPO+'backend/src/ultramedia/dataset.py')

        # 7. Explain the learning lifecycle with legible vector graphics.
        self.start(7,'The Week 5 learning story','Teach the response behavior. Supply the race facts.',
                   'Prompting defines the task; retrieval supplies current evidence; fine-tuning adapts the response behavior.')
        pipeline=[('Data','600 fictional examples'),('SFT / QLoRA','Train small adapters'),('Merge','Combine with pinned base'),('Serve locally','GGUF / llama.cpp'),('Compare','Same 120 test cases')]
        for i,(title,body) in enumerate(pipeline):
            x=M+i*144
            self.rect(x,171,132,96,LILAC)
            self.number(i+1,x+12,181)
            self.text(title,x+12,214,108,12,PURPLE,True)
            self.text(body,x+12,236,108,9.5,limit=27)
            if i<4:self.arrow(x+134,220,x+142)
        self.text('A dataset with a separate test set',M,290,WIDTH,17,INK,True)
        segments=[(400,PURPLE,'TRAIN 400'),(80,'#9B83BF','VAL 80'),(120,GREEN,'TEST 120')]
        x=M
        for count,color,label in segments:
            w=WIDTH*count/600
            self.rect(x,322,w,38,color,r=0)
            self.text(label,x+12,334,w-18,10,white.hexval(),True)
            x+=w
        self.text('150 fictional race groups; no group crosses splits. Four signal types, five evidence conditions.',M,372,WIDTH,11,MUTED)
        self.rect(M,406,345,124,PALE)
        self.text('Demonstrated',M+16,420,313,13,GREEN,True)
        self.text('Qwen3-4B-Instruct-2507; rank-16 LoRA.<br/>NF4 training: 2 epochs, 100 steps.<br/>33,030,144 trainable parameters.<br/>Adapter merged and evaluated locally.',M+16,447,313,11,limit=67)
        self.rect(405,406,345,124,CREAM)
        self.text('Future experiments / pending proof',421,420,313,13,AMBER,True)
        self.text('Fireworks RFT and teacher distillation: not run.<br/>Native Ollama API demo: not demonstrated.<br/>Human editorial benefit: not measured.<br/>Full agenda mapping is linked on page 10.',421,447,313,11,limit=67)
        self.text('All training examples are programmatic synthetic references; none are human-approved.',M,542,WIDTH,9,MUTED)
        self.end(7,GIT+'project/AGENDA_COVERAGE.md')

        # 8. Standard plotting tools for a publishable quantitative figure.
        self.start(8,'What the data actually shows','A measured gain, with the limits beside it.',
                   'Matched local comparison: same base lineage, prompt, Q4_K_M runtime and schema constraints.')
        fig,ax=plt.subplots(figsize=(4.35,2.9),dpi=200)
        fig.patch.set_facecolor('#FFFFFF');ax.set_facecolor('#FFFFFF')
        values=[76/120*100,109/120*100]
        ax.barh([1,0],values,height=.42,color=['#AAA5B8',PURPLE])
        ax.set_yticks([1,0],['Base','Fine-tuned']);ax.set_xlim(0,115)
        ax.set_xticks([0,25,50,75,100],['0%','25%','50%','75%','100%'])
        ax.tick_params(axis='both',length=0,labelsize=10,pad=8,colors=INK)
        for spine in ax.spines.values():spine.set_visible(False)
        ax.grid(axis='x',color='#EBE7F0');ax.set_axisbelow(True)
        for y,value,count in zip([1,0],values,[76,109]):
            ax.text(value+2,y,f'{value:.1f}%\n{count}/120',va='center',fontsize=10,color=INK,fontweight='bold')
        ax.set_title('All automatic checks passed',loc='left',fontsize=12,color=INK,pad=16)
        fig.subplots_adjust(left=.20,right=.95,top=.83,bottom=.17)
        stream=BytesIO();fig.savefig(stream,format='png',dpi=200);plt.close(fig);stream.seek(0)
        self.image(stream,M,171,395,264)
        self.rect(457,175,293,92,LILAC)
        self.text('+27.5 points',475,188,257,27,PURPLE,True)
        self.text('Paired 95% interval: +20 to +35 points',475,230,257,11,INK)
        self.text('What passed',475,288,257,14,INK,True)
        self.text('Both models: 120/120 valid schemas.<br/>The score combines eight checks for structure, citations, claims, numeric support, decision and selected wording.',475,315,257,11,limit=84)
        self.rect(M,436,WIDTH,101,CREAM)
        self.text('Evidence that keeps the claim in bounds',M+16,449,WIDTH-32,13,AMBER,True)
        self.text('11 fine-tuned failures: unnecessary holds.<br/>Five new probes: base 3/5; adapted 3/5.<br/>Rules: 120/120 on the engineered test.',M+16,477,319,10.5,limit=48)
        self.text('13 app software checks passed; separate quality suite failed one case. Human review and the paired explicit-schema GPU control remain pending.',421,477,313,10.5,limit=48)
        self.text('Synthetic benchmark only; not editor preference. Rules share the task design. Bootstrap: 30 groups, 1,000 resamples.',M,545,WIDTH,8.5,MUTED)
        self.end(8,GIT+'reports/LOCAL_COMPARISON_RESULTS.md')

        # 9. Proposed sequence tied to current evidence gaps, not delivery promises.
        self.start(9,'Product roadmap','Prove reliability. Earn trust. Then expand.',
                   'An evidence-led sequence: current capability, proposed next priorities and conditional future options.')
        stages=[
            ('01 / NOW','Research prototype',PALE,GREEN,
             'Cited draft/hold workflow, protected revisions and a local fine-tuned open model. Public evidence and recorded examples are available.',
             'Status: demonstrated in synthetic research; human editorial benefit remains unmeasured.'),
            ('02 / NEXT','Close the reliability gaps',LILAC,PURPLE,
             'Address invented citations, misleading hints and record-projection wording. Clarify input conventions; version changes and test fresh cases.',
             'Gate: fresh challenge results and complete the paired GPU control when capacity is available.'),
            ('03 / PILOT','Measure value with editors',LILAC,PURPLE,
             'Use consented race material in a bounded pilot. Compare rules, base and adapted drafts for acceptance, correction effort and factual quality.',
             'Gate: measured editor benefit, acceptable errors and cost per accepted brief before broader use.'),
            ('04 / LATER','Expand access and coverage',CREAM,AMBER,
             'Prioritize source integrations and team access from pilot feedback. Evaluate native Ollama or budget-approved Fireworks hosting.',
             'Gate: hosting, privacy and cost checks. RFT or distillation only after data/reward validation.'),
        ]
        for i,(stage,title,fill,color,body,gate) in enumerate(stages):
            x=M+(i%2)*363;y=171+(i//2)*176
            self.rect(x,y,345,158,fill,r=12)
            self.text(stage,x+16,y+13,313,9,color,True)
            self.text(title,x+16,y+34,313,17,INK,True,limit=25)
            self.text(body,x+16,y+64,313,11,INK,limit=59)
            self.text(gate,x+16,y+122,313,9,color,True,limit=29)
        self.text('Proposed roadmap, not committed dates. New model versions require new evidence; existing results stay frozen.',M,526,WIDTH,10,MUTED,limit=28)
        self.end(9,GIT+'PROJECT_REPORT.md')

        # 10. Progressive disclosure: visual introduction, demonstration, then raw data.
        self.start(10,'Go deeper at your own pace','Start with the demo. Follow the evidence.',
                   'Every underlined resource and colored button is clickable. QR codes also work from a printed copy.')
        for x,title,desc,url in [(M,'Explore UltraMedia','Product and editorial workflow',DEMO),(405,'Open the evidence hub','Week 5 results and recorded examples',HUB)]:
            self.rect(x,170,345,122,LILAC)
            qr=QrCodeWidget(url)
            bounds=qr.getBounds(); qw,qh=bounds[2]-bounds[0],bounds[3]-bounds[1]
            drawing=Drawing(98,98,transform=[98/qw,0,0,98/qh,0,0]);drawing.add(qr)
            self.rect(x+12,181,98,98,white,r=0)
            renderPDF.draw(drawing,self.c,x+12,PAGE_H-181-98)
            self.text(title,x+122,187,208,17,INK,True)
            self.text(desc,x+122,219,206,11,MUTED,limit=30)
            self.link('Open online',url,x+122,253,137,28)
        resources=[
            ('01  Product walkthrough','Watch the recorded workflow.',GIT+'evidence/handout-page/project-walkthrough.webm'),
            ('02  Complete project report','Requirements, tradeoffs and decisions.',GIT+'PROJECT_REPORT.md'),
            ('03  Data and provenance','Split design, examples and hashes.',GIT+'reports/DATA_REPORT.md'),
            ('04  Training receipts','Configuration, loss and verification.',TREE+'reports/data/final-training'),
            ('05  Paired model comparison','Scores, raw outputs and failures.',GIT+'reports/LOCAL_COMPARISON_RESULTS.md'),
            ('06  Case-level CSV','Inspect all paired test rows.',GIT+'reports/data/local-comparison-cases.csv'),
            ('07  Week 5 agenda map','Executed topics versus future work.',GIT+'project/AGENDA_COVERAGE.md'),
            ('08  End-to-end visual','See the full technical illustration.',GIT+'diagrams/week5-end-to-end-illustrated.png'),
        ]
        for i,(label,desc,url) in enumerate(resources):
            x=M+(i%2)*363;y=311+(i//2)*48
            self.text('<u>'+label+'</u>',x,y,345,11,PURPLE,True)
            self.text(desc,x,y+18,345,9.5,MUTED)
            self.c.linkURL(url,(x,PAGE_H-y-33,x+345,PAGE_H-y),relative=0);self.links.append(url)
        self.rect(M,510,WIDTH,40,CREAM,r=7)
        self.text('Public demo includes recorded examples. This brochure does not claim live cloud model hosting or production approval.',M+12,520,WIDTH-24,10,INK,limit=28)
        self.end(10,GIT+'PROJECT_REPORT.md')
        # 11. Direct source register, plus identity and rights boundaries.
        self.start(11,'Source register','Open the source behind every data claim.',
                   'S1-S12 identify the creator, location and role. Git links are pinned; official websites were checked 09 Sep 2026.')
        sources=[
            ('S1 / UltraMedia generator','dataset.py - authored values, conditions and target stories.',REPO+'backend/src/ultramedia/dataset.py'),
            ('S2 / Frozen dataset manifest','Counts, split audit, file hashes and dataset version.',GIT+'data/synthetic/manifest.json'),
            ('S3 / Demo fixture and attribution','sample_race.json - simulated timing and context records.',REPO+'backend/data/sample_race.json'),
            ('S4 / Western States official site','wser.org - course profile and canyon context.', 'https://www.wser.org/'),
            ('S5 / Western States participant guide','wser.org/participant-guide/ - finish-window context.', 'https://www.wser.org/participant-guide/'),
            ('S6 / Western States history','wser.org/year-by-year/ - historical background only.', 'https://www.wser.org/year-by-year/'),
            ('S7 / Project training receipts','Colab run, loss history and verification manifests.',TREE+'reports/data/final-training'),
            ('S8 / Paired local comparison','Mac execution, raw predictions and failed cases.',GIT+'reports/LOCAL_COMPARISON_RESULTS.md'),
            ('S9 / Input and response contract','contracts.py - fields, units and bounded validation.',REPO+'backend/src/ultramedia/contracts.py'),
            ('S10 / Qwen model publisher','Qwen3-4B-Instruct-2507 weights; Apache 2.0 license.', 'https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507'),
            ('S11 / Every synthetic record','600-row inventory with provenance and content hashes.',GIT+'reports/data/dataset-inventory.csv'),
            ('S12 / Future external timing import','ingestion.py - CSV path; no live vendor feed evidenced.',REPO+'backend/src/ultramedia/ingestion.py'),
        ]
        for i,(label,desc,url) in enumerate(sources):
            x=M+(i%2)*363;y=174+(i//2)*47
            self.text('<u>'+label+'</u>',x,y,345,11,PURPLE,True)
            self.text(desc,x,y+18,345,9.5,MUTED,limit=27)
            self.c.linkURL(url,(x,PAGE_H-y-40,x+345,PAGE_H-y),relative=0);self.links.append(url)
        self.rect(M,465,WIDTH,82,CREAM,r=8)
        self.text('Dataset identity and usage boundaries',M+12,475,WIDTH-24,11,AMBER,True)
        self.text('ultramedia-synthetic-research-v1 | SHA-256:',M+12,496,WIDTH-24,9,INK)
        self.text('5c148b3d1e57a989e38c55e73f1d46ae0b5b17227be154457953bac2dcaef8cf',M+12,511,WIDTH-24,9,INK)
        self.text('Official references are separate from the CC0 corpus. External timing and editorial exports need appropriate rights/consent.',M+12,531,WIDTH-24,8.5,MUTED,limit=14)
        self.end(11,GIT+'reports/DATA_REPORT.md')
        self.c.save()
        return {'pages':11,'source_snapshot':SNAPSHOT,'external_links':self.links,'text_blocks':len(self.boxes)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'UltraMedia-Brochure.pdf')
    parser.add_argument('--qa-json',type=Path)
    args=parser.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    fonts(); receipt=Brochure(args.output).build()
    if args.qa_json:args.qa_json.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'pages':receipt['pages'],'links':len(receipt['external_links'])}))

if __name__=='__main__':main()
