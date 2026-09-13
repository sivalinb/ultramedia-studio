"""Software fixtures only: no test answer is independent human evidence."""
import copy
import json
import unittest
from pathlib import Path
from prepare import cases, judge_probes
from collect_independent import agreement, expected_ids, validate

ROOT=Path(__file__).resolve().parent


def fake_review(kind,reviewer='TEST-A'):
    return {'reviewer_id':reviewer,'role':'independent_editor','completed_at':'TEST ONLY',
        'labels':[{'id':i,'decision':'ambiguous','supported_facts':[],'rationale':'TEST ONLY, not actual review'} for i in expected_ids(kind)]}


class CalibrationTests(unittest.TestCase):
    def test_frozen_cases_reproduce_and_hint_only_pairs_match(self):
        rows=cases();self.assertEqual(rows,json.loads((ROOT/'interaction-cases.json').read_text()));self.assertEqual(len(rows),48)
        for group in {r['group_id'] for r in rows}:
            for condition in ['complete','missing','contradictory']:
                a,b=[r for r in rows if r['group_id']==group and r['condition']==condition]
                self.assertEqual(a['inputs']['evidence'],b['inputs']['evidence']);self.assertEqual(a['inputs']['timing'],b['inputs']['timing'])
                self.assertNotEqual(a['inputs']['moment']['headline_hint'],b['inputs']['moment']['headline_hint'])

    def test_packets_do_not_expose_labels_or_scores(self):
        for name in ['independent-label-packet.json','judge-review-packet.json']:
            for row in json.loads((ROOT/name).read_text()):
                self.assertFalse({'expected','author_expected_acceptable','checks','label_status'} & row.keys())

    def test_blank_missing_and_duplicate_cases_rejected(self):
        with self.assertRaises(ValueError):validate({},'labels')
        for change in ['empty','duplicate','missing']:
            r=fake_review('labels')
            if change=='empty':r['labels'][0]['decision']=None
            if change=='duplicate':r['labels'][0]=copy.deepcopy(r['labels'][1])
            if change=='missing':r['labels'].pop()
            with self.assertRaises(ValueError):validate(r,'labels')

    def test_distinct_independent_reviewers_required(self):
        a=fake_review('judge');b=fake_review('judge')
        with self.assertRaises(ValueError):agreement([a,b],'judge')
        b['reviewer_id']='TEST-B';b['role']='founder'
        with self.assertRaises(ValueError):agreement([a,b],'judge')

    def test_agreement_preserves_ambiguity_and_is_not_calibration(self):
        a=fake_review('judge');b=fake_review('judge','TEST-B');r=agreement([a,b],'judge')
        self.assertEqual(r['raw_agreement'],1);self.assertEqual(r['ambiguous_cases'],10)
        self.assertEqual(len(r['cases_requiring_adjudication']),10);self.assertFalse(r['judge_calibrated'])
        self.assertNotIn('TEST-A',json.dumps(r))


if __name__=='__main__':unittest.main()
