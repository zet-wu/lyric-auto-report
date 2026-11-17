import unittest
from text_units import split_timed_text
from score import norm,envelope,load_prediction

class NativeTextUnits(unittest.TestCase):
 def split(self,text,readings):
  return split_timed_text(text,[{'text':r,'start':i,'end':i+.8} for i,r in enumerate(readings)],norm,envelope)
 def test_kana_keeps_independent_times_and_gaps(self):
  self.assertEqual(self.split('こんな',['こ','ん','な']),[{'text':'こ','start':0,'end':.8},{'text':'ん','start':1,'end':1.8},{'text':'な','start':2,'end':2.8}])
 def test_okurigana_anchors_kanji_reading(self):
  p=self.split('暖かい',list('あたたかい'))
  self.assertEqual([(x['text'],x['start'],x['end']) for x in p],[('暖',0,2.8),('か',3,3.8),('い',4,4.8)])
 def test_shared_kanji_reading_is_not_guessed(self):
  self.assertEqual([x['text'] for x in self.split('明日',['あ','す'])],['明日'])
 def test_ambiguous_anchor_remains_grouped(self):
  self.assertEqual([x['text'] for x in self.split('漢あ字',list('かああじ'))],['漢あ字'])
 def test_native_combined_unit_cannot_be_split(self):
  self.assertEqual([x['text'] for x in self.split('きゃく',['きゃ','く'])],['きゃ','く'])
 def test_missing_time_stays_missing(self):
  p=split_timed_text('かな',[{'text':'か','start':None,'end':None},{'text':'な','start':1,'end':2}],norm,envelope)
  self.assertIsNone(p[0]['start']);self.assertEqual(p[1]['start'],1)
 def test_frozen_milikara_export_uses_real_unit_times(self):
  p=load_prediction('s01','milikara','G3')[0][2]
  self.assertEqual([(x['text'],x['start'],x['end']) for x in p[:3]],[('こ',23.78,24.12),('ん',24.12,24.42),('な',24.44,24.5)])
if __name__=='__main__':unittest.main()
