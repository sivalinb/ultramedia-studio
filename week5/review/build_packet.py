"""Create a blind, fillable review packet from saved outputs; never read an assignment key."""
import argparse
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'evidence/handout-smoke/blind-review.json'
INK = HexColor('#18334a')
TEAL = HexColor('#087f8c')
STYLE = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14, textColor=INK)


def build(output):
    cases = json.loads(SOURCE.read_text())
    c = canvas.Canvas(str(output), pagesize=(612, 792))
    c.setTitle('UltraMedia | Blind editorial review pilot')
    page = 0

    def start(title, subtitle):
        nonlocal page
        page += 1
        c.setFillColor(INK); c.rect(0, 702, 612, 90, fill=1, stroke=0)
        c.setFillColor(white); c.setFont('Helvetica-Bold', 20); c.drawString(40, 751, title)
        c.setFont('Helvetica', 10); c.drawString(40, 726, subtitle)
        c.setFillColor(INK); c.setFont('Helvetica', 8)
        c.drawString(40, 24, 'UltraMedia | Fictional five-case pilot | Model identities withheld')
        c.drawRightString(572, 24, str(page))

    def para(text, y, size=10):
        style = ParagraphStyle('p', parent=STYLE, fontSize=size, leading=size+4)
        p = Paragraph(escape(str(text)).replace('\n', '<br/>'), style)
        _, h = p.wrap(532, 700)
        if y-h < 48:
            raise ValueError(f'Page {page} overflow: {text[:40]}')
        p.drawOn(c, 40, y-h)
        return y-h-10

    def field(name, label, y, height=24, multiline=False):
        y = para(label, y, 9)
        c.acroForm.textfield(name=name, tooltip=label, x=40, y=y-height,
                            width=532, height=height, fontSize=10, textColor=INK,
                            borderColor=TEAL, fillColor=HexColor('#f4fafb'),
                            fieldFlags='multiline' if multiline else '', maxlen=3000)
        return y-height-14

    start('Independent editorial review', 'Read evidence. Judge each draft. Save your responses before unblinding.')
    y=676
    for text in [
        'Purpose: test whether these saved outputs are useful, accurate editorial drafts. This is an exploratory five-case synthetic pilot, not a production study or a measure of race safety.',
        'Use a separate copy per reviewer. Suggested reviewers: two race-media editors or experienced race volunteers. Founder feedback is welcome but must be labeled separately. Do not consult model scores, assignment keys, or other reviewers before completing your copy.',
        'Read each case input and all three candidates. A smaller overall position number means a better placing. A projection is not an achieved result. Check citations, missing evidence, contradictions, unsupported medical claims, grammar, and irrelevant wording.',
        'Score every candidate: meaning = supported / unsupported / unclear; readability = 1 (major rewriting) to 5 (clear and polished); usable = yes / no, meaning useful as a draft after editorial review, never permission to auto-publish. Record estimated correction minutes, or time actual edits and state that in your rationale.',
        'Choose A, B, C, tie, or neither for each case after reviewing all candidates. Explain your choice and failures. Empty fields remain pending. No scores are generated automatically.',
        'Save as a new PDF in a form-capable reader, reopen to verify your answers, and return it privately to the project owner. Identity and free text stay private. Only aggregate results should enter Git. Training permission is separate and never assumed.'
    ]: y=para(text,y)
    y=field('reviewer_id','Reviewer ID (use a pseudonym; owner keeps identity separately)',y)
    y=field('reviewer_role','Role: independent_editor / race_volunteer / founder / other',y)
    y=field('training_consent','Optional use of your review text for training: false (default) or true',y)
    c.showPage()
    for index, case in enumerate(cases, 1):
        start(f'Case {index} | Source evidence',case['id'])
        y=para('These are the complete saved inputs. They are fictional evaluation data.',676)
        for key, value in case['inputs'].items():
            y=para(f'{key}:',y)
            for item in (value if isinstance(value,list) else [value]):
                y=para(json.dumps(item,ensure_ascii=True),y,10)
        y=field(f'{index}.preferred','After reviewing A/B/C: preferred A / B / C / tie / neither',y)
        y=field(f'{index}.preference_reason','Why? Note tradeoffs or a reason no candidate is acceptable.',y,48,True)
        c.showPage()
        for label, candidate in case['candidates'].items():
            start(f'Case {index} | Candidate {label}',case['id'])
            y=676
            for key, value in candidate.items():
                value = json.dumps(value,ensure_ascii=True) if isinstance(value,(dict,list)) else str(value)
                y=para(f'{key}: {value}',y,9)
            for key,label_text,height in [
                ('meaning','Meaning: supported / unsupported / unclear',22),
                ('readability','Readability: integer 1 to 5',22),
                ('usable','Useful as an editorial draft: yes / no',22),
                ('minutes','Correction minutes: nonnegative number (estimate unless timed)',22),
                ('rationale','Rationale: cite a specific strength, error, or required edit',50),
            ]:
                y=field(f'{index}.{label}.{key}',label_text,y,height,key=='rationale')
            c.showPage()
    c.save()
    return {'pages':page,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'cases':len(cases),'human_reviews_completed':0,'contains_assignment_key':False}


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('output',type=Path)
    args=parser.parse_args();print(json.dumps(build(args.output),indent=2))
