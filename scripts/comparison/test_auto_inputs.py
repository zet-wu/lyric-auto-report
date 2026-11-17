"""Automatic preparation must consume plain text, not reference segmentation."""
import copy
import unittest
from common import plain_line


class PlainTextInput(unittest.TestCase):
 def test_xml_layout_is_removed_but_internal_spaces_remain(self):
  self.assertEqual(plain_line('\n\t粉\r\n\t雪 In  the\n'), '粉雪 In  the')

 def test_sug_uses_native_reading_checkpoints(self):
  from sug_project import create_project
  song={'duration':10,'lines':[{'text':'粉\n\t雪が空から'}]}
  project=create_project(song,'auto')
  chars=project.sentences[0].characters
  self.assertEqual([(c.char,c.check_count) for c in chars[:2]],[('粉',2),('雪',2)])
  self.assertEqual([p.text for p in chars[0].ruby.parts],['こ','な'])
  self.assertTrue(all(not c.timestamps and c.sentence_end_ts is None for c in chars))

 def test_reference_words_readings_and_times_cannot_affect_auto_input(self):
  from sug_project import create_project
  song={'duration':10,'lines':[{'text':'粉雪が空から'}]}
  altered=copy.deepcopy(song)
  altered['lines'][0].update(words=[{'text':'wrong','start':8,'end':9}],leaves=[{'text':'まちがい'}],start=8,end=9)
  def shape(p):
   return [[(c.char,c.check_count,[x.text for x in c.ruby.parts] if c.ruby else []) for c in l.characters] for l in p.sentences]
  self.assertEqual(shape(create_project(song,'auto')),shape(create_project(altered,'auto')))


if __name__=='__main__':unittest.main()
