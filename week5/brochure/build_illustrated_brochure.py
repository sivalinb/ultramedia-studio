"""Illustration-led brochure. Run from any directory with --output path.pdf.

Uses the approved image_gen artwork unchanged, with exact text, links, chart
and QR codes composed in PDF. No raster image editing is performed here.
Dependencies/font choices match build_brochure.py.
"""
from pathlib import Path
from io import BytesIO
import argparse
import json
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
        10:('#067D9C','#E5F8FB'),11:('#3E692A','#EFF5E8')}

class Illustrated(b.Brochure):
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

    def build(self):
        self.start(1,'The product in one picture','Race evidence in. Reviewed stories out.',
                   'UltraMedia Race Desk brings race sources, cited drafts and editorial decisions into one workspace.')
        self.art(1,160,354)
        self.link('Explore the product',b.DEMO,b.M,522,194,fill=self.accent)
        self.link('Jump to the evidence',b.HUB,250,522,207,fill=self.accent)
        self.text('Illustrative race scenes and numbers.<br/>Public demo includes recorded examples.',477,526,273,9,b.MUTED,limit=28)
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

        self.start(3,'Who can use it','One workspace. Four editorial perspectives.',
                   'Intended audiences: race organizers, sports editors, event media teams and running communities.')
        self.art(3)
        self.cards([('Organize','Prepare event updates from timing facts and context.'),
                    ('Edit','Inspect source references and revise the wording.'),
                    ('Create','Develop stories and captions from a shared starting point.'),
                    ('Explain','Help a community understand the race moment.')],y=466,h=78,size=9.5)
        self.fineprint('The characters use the creator\'s likeness. These are intended user roles, not customer testimonials.',551,8)
        self.end(3,b.GIT+'project/PRODUCT_PITCH.md')

        self.start(4,'How it works','Choose. Retrieve. Draft. Validate. Review.',
                   'A supported draft goes to an editor. Missing or conflicting evidence should produce a hold with a reason.')
        self.art(4)
        self.cards([('Illustrative evidence-to-draft example','Position 8 to 5 = 3 places gained. A candidate states that change and cites timing-01. This is an authored example, not a saved model output.'),
                    ('Human control stays visible','Check the source, correct wording and approve a version. A model or validator can still be wrong; approval does not publish externally.')],y=466,h=87,size=10)
        self.end(4,b.GIT+'PROJECT_REPORT.md')

        self.start(5,'Where the data comes from','Three sources. Three different purposes.',
                   'The training corpus, demo context and measured execution evidence have separate provenance. Source register: page 11.')
        self.art(5,147,302)
        self.cards([('Authored research [S1, S2]','600 fictional records from dataset.py; generator seed 20260908; synthetic:// source IDs. CC0-1.0 records, zero human approvals. No scraped results or teacher outputs.'),
                    ('Static demo [S3-S6]','7 simulated timings for 2 fictional athletes; 5 context chunks. Four chunks cite official Western States course, guide or history pages; one is product policy.'),
                    ('Real execution [S7, S8]','Project-generated Colab logs and Mac predictions, checks and token receipts. Actual runs on synthetic inputs; no live vendor feed or real-race validation is claimed.')],y=453,h=101,size=9.1)
        self.end(5,b.GIT+'DATA_CARD.md')

        self.start(6,'What is considered','Read the signal. Check the evidence.',
                   'Four signal types (150 records each) and five evidence conditions (120 each) make a controlled research task.')
        self.art(6,149,294)
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
        self.text('+27.5 percentage points',b.M+12,420,324,17,self.accent,True)
        self.text('Paired 95% interval: +20 to +35 points',b.M+12,446,324,10,b.MUTED)
        self.cards([('Scope of the score','Eight automatic checks; both models have 120/120 valid schemas. Synthetic test only, not editor preference.'),
                    ('Negative evidence','11 adapted failures are unnecessary holds. Five new probes: base 3/5, adapted 3/5. Rules pass 120/120 engineered cases.'),
                    ('Still pending','Human editorial review and paired GPU control. 13 app software checks passed, but the separate quality suite failed one case.')],y=477,h=77,size=9)
        self.end(8,b.GIT+'reports/LOCAL_COMPARISON_RESULTS.md')

        self.start(9,'Proposed product roadmap','Prove reliability. Earn trust. Then expand.',
                   'Current capability, proposed next steps and conditional future options. No delivery dates or funding commitments implied.')
        self.art(9)
        self.cards([('Now: research','Cited drafts, local open model and evidence reports. Human benefit is not measured.'),
                    ('Next: reliability','Fix citations, hints and projection wording. Version changes; test fresh cases.'),
                    ('Pilot: editor value','Use consented material. Measure factual quality, correction time and accepted-brief cost.'),
                    ('Later: expand','Prioritize integrations and team access; evaluate Ollama or approved cloud hosting.')],y=466,h=80,size=9)
        self.fineprint('Gate expansion on editor benefit, acceptable errors and cost/privacy checks. RFT requires validated rewards.',552,8)
        self.end(9,b.GIT+'PROJECT_REPORT.md')

        self.start(10,'Explore at your own pace','Start with the demo. Follow the evidence.',
                   'Clickable resources and QR codes take you from the product story into the recorded work and underlying data.')
        self.art(10,149,293)
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
                   'S1-S12 identify the creator, source location and role. Official sites checked 09 Sep 2026; Git links are pinned.')
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
        ]
        for i,(label,desc,url) in enumerate(sources):
            x=302+(i%2)*230;y=169+(i//2)*53
            self.resource(label,desc,url,x,y,218,10)
        self.text('Dataset SHA-256',302,496,448,9,self.accent,True)
        self.text('5c148b3d1e57a989e38c55e73f1d46ae0b5b17227be154457953bac2dcaef8cf',302,512,448,8,b.INK)
        self.fineprint('CC0 applies to authored synthetic records, not official references. External timing/editorial data needs appropriate rights and consent.',541,8.2)
        self.end(11,b.GIT+'DATA_CARD.md')
        self.c.save()
        return {'pages':11,'source_snapshot':b.SNAPSHOT,'external_links':self.links,'artwork_pages':list(range(1,12)),'text_blocks':len(self.boxes)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'UltraMedia-Brochure.pdf');ap.add_argument('--qa-json',type=Path)
    args=ap.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    b.fonts();receipt=Illustrated(args.output).build()
    if args.qa_json:args.qa_json.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'pages':receipt['pages'],'links':len(receipt['external_links'])}))

if __name__=='__main__':main()
