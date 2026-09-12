"""Synthetic software tests only. These answers are not human-review evidence."""
import tempfile
import unittest
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from collect_reviews import collect, validate


def example():
    fields={'reviewer_id':'TEST_ONLY','reviewer_role':'founder'}
    for i in range(1,6):
        fields.update({f'{i}.preferred':'neither',f'{i}.preference_reason':'TEST ONLY'})
        for label in 'ABC':
            for key,value in {'meaning':'unclear','readability':'3','usable':'no','minutes':'2.5','rationale':'TEST ONLY - not a human judgment'}.items():
                fields[f'{i}.{label}.{key}']=value
    return fields


class ReviewTests(unittest.TestCase):
    def test_blank_rejected(self):
        with self.assertRaises(ValueError): validate({})

    def test_nonfinite_negative_and_missing_rejected(self):
        for bad in ['nan','inf','-1','']:
            fields=example();fields['1.A.minutes']=bad
            with self.assertRaises(ValueError): validate(fields)

    def test_consent_defaults_false_and_invalid_choices_rejected(self):
        self.assertFalse(validate(example())['training_consent'])
        for field in ['training_consent','reviewer_role','1.preferred','1.A.meaning','1.A.readability','1.A.usable']:
            values=example();values[field]='invalid'
            with self.assertRaises(ValueError): validate(values)

    def test_pdf_roundtrip_privacy_and_duplicate_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);file=tmp/'synthetic-test.pdf'
            writer=PdfWriter();writer.clone_document_from_reader(PdfReader(Path(__file__).parent/'UltraMedia-Blind-Editorial-Review.pdf'))
            writer.update_page_form_field_values(None,example(),auto_regenerate=False)
            writer.write(file)
            result=collect([file],tmp/'aggregate.json')
            self.assertEqual(result['groups']['founder']['candidate_judgments'],15)
            self.assertNotIn('TEST_ONLY',(tmp/'aggregate.json').read_text())
            self.assertNotIn('rationale',(tmp/'aggregate.json').read_text().split('limitations')[0])
            with self.assertRaises(ValueError):collect([file,file],tmp/'duplicate.json')
            self.assertFalse((tmp/'duplicate.json').exists())


if __name__=='__main__': unittest.main()
