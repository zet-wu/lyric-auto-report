"""Reading correspondence regressions; run with the scoring-only environment."""
import unittest
from score_reading import unique_boundaries,native
from score import clock

class ReadingBoundaries(unittest.TestCase):
 def test_identity_preserves_sokuon_and_long_mark(self):
  s='ぜったいはーと'
  self.assertEqual(unique_boundaries(s,s),dict(enumerate(range(len(s)+1))))
 def test_repeated_kana_do_not_pick_an_arbitrary_deletion(self):
  self.assertEqual(unique_boundaries('ああい','あい'),{0:0,2:1,3:2})
 def test_inserted_reading_has_no_invented_internal_boundary(self):
  self.assertNotIn(2,unique_boundaries('わたし','わたくし'))
 def test_manual_milikara_keeps_ruby_inside_surface_word(self):
  parts=native('s01','milikara','G1')[0]
  self.assertEqual(parts[0]['text'],'絶')
  self.assertEqual([u['text'] for u in parts[0]['units']],['ぜ','っ'])
 def test_native_ass_combines_sokuon_but_preserves_other_ruby(self):
  parts=native('s01','fa-kara','G1')[0]
  self.assertEqual([u['text'] for u in parts[0]['units']],['ぜっ'])
  self.assertEqual([u['text'] for u in parts[1]['units']],['た','い'])
 def test_sug_saved_points_keep_manual_ruby(self):
  parts=native('s01','sug-nextfire','G1')[0]
  self.assertEqual([u['text'] for u in parts[0]['units']],['ぜ','っ'])
  self.assertEqual(parts[0]['units'][0]['end'],parts[0]['units'][1]['start'])
 def test_sug_auto_uses_the_saved_character_checkpoint(self):
  from common import OUT,read
  r=read(OUT/'sug/s02-sug-nextfire-auto.json')
  saved=read(OUT.parents[1]/r['sug_project']['path'])
  parts=native('s02','sug-nextfire','G3')[0]
  self.assertEqual(parts[0]['start'],saved['sentences'][0]['characters'][0]['timestamps'][0]/1000)
  self.assertEqual(parts[0]['end'],saved['sentences'][0]['characters'][1]['timestamps'][0]/1000)
 def test_ass_negative_hour_uses_libass_arithmetic(self):
  self.assertAlmostEqual(clock('-1:59:59.96'),-.04)
if __name__=='__main__':unittest.main()
