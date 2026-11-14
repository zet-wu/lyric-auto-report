"""Extract text-only inputs and isolated original TTML reading references."""
from common import *
def display(s):return s.replace('\n','').replace('\r','').replace('\t','')
selected=set(read(ROOT/'configs/reading.json')['songs'])
refs=[]
for s in read(ROOT/'results/timing/reference.json'):
 if s['id'] not in selected:continue
 data={'song':s['id'],'lines':[]};gold={'song':s['id'],'lines':[]}
 for li,l in enumerate(s['lines']):
  selection=read(ROOT/'configs/reading.json').get('line_selection',{}).get(s['id'])
  if selection and li not in selection['indices']:continue
  words=[];truth=[]
  for w in l['words']:
   leaves=[x for x in l['leaves'] if x['word_id']==w['id']]
   words.append(display(w['text']));truth.append({'text':display(w['text']),'reading':display(''.join(x['text'] for x in leaves)),'ruby':any(x['kind']=='ruby' for x in leaves)})
  assert ''.join(words)==display(l['text'])
  data['lines'].append({'id':l['id'],'text':display(l['text']),'words':words});gold['lines'].append({'id':l['id'],'words':truth})
 dump(OUT/'inputs'/f"{s['id']}.json",data);refs.append(gold)
dump(OUT/'references.json',refs)
