"""Extract text-only inputs and isolated original TTML reading references."""
from common import *
def display(s):return s.replace('\n','').replace('\r','').replace('\t','')
refs=[]
for s in read(ROOT/'results/timing/reference.json'):
 if s['id'] in ('s11','s13','s14'):continue
 data={'song':s['id'],'lines':[]};gold={'song':s['id'],'lines':[]}
 for l in s['lines']:
  words=[];truth=[]
  for w in l['words']:
   leaves=[x for x in l['leaves'] if x['word_id']==w['id']]
   words.append(display(w['text']));truth.append({'text':display(w['text']),'reading':display(''.join(x['text'] for x in leaves)),'ruby':any(x['kind']=='ruby' for x in leaves)})
  assert ''.join(words)==display(l['text'])
  data['lines'].append({'id':l['id'],'text':display(l['text']),'words':words});gold['lines'].append({'id':l['id'],'words':truth})
 dump(OUT/'inputs'/f"{s['id']}.json",data);refs.append(gold)
dump(OUT/'references.json',refs)
