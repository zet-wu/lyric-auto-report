"""Prepare native app inputs: source text and isolated manual readings, never timings."""
from common import *
import re,unicodedata
DEST=ROOT/'results/milikara-native'
def layout(s):return s.replace('\n','').replace('\r','').replace('\t','')
def reading(s):return ''.join(c for c in unicodedata.normalize('NFKC',s) if c.isalnum() or c in "ー'’")
for song in read(ROOT/'results/timing/reference.json'):
 text={'song':song['id'],'name':song['name'],'audio':song['audio'],'lines':[]};manual={**text,'lines':[]}
 for l in song['lines']:
  source=layout(l['text']).strip();text['lines'].append({'id':l['id'],'text':source})
  words=[]
  for w in l['words']:
   units=[{'id':u['id'],'reading':reading(u['text'])} for u in l['leaves'] if u['word_id']==w['id'] and reading(u['text'])]
   words.append({'id':w['id'],'text':layout(w['text']),'units':units})
  # Trim outer layout spaces in the same way as the upstream plain-text importer.
  while words and not words[0]['text'].strip():words.pop(0)
  while words and not words[-1]['text'].strip():words.pop()
  if words:words[0]['text']=words[0]['text'].lstrip();words[-1]['text']=words[-1]['text'].rstrip()
  assert ''.join(w['text'] for w in words)==source
  manual['lines'].append({'id':l['id'],'text':source,'words':words})
 units=[u for line in manual['lines'] for word in line['words'] for u in word['units']]
 missing=[u['id'] for u in units if re.search('[\u3400-\u9fff]',u['reading'])]
 manual['reading_audit']={'units':len(units),'untranscribed_han_units':missing,
  'note':'Original untranscribed Han characters are retained for stress cases; they are not supplied phonetic readings.'}
 dump(DEST/'inputs/text'/f"{song['id']}.json",text);dump(DEST/'inputs/manual'/f"{song['id']}.json",manual)
