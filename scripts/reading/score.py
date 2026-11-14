"""Shared source-span and full-line reading accuracy; no alignment scoring."""
from common import *
import argparse
PROTOCOL=read(ROOT/'configs/reading.json')
METHODS=PROTOCOL['methods']
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--method',choices=METHODS,help='Refresh only this method; require all other results to agree with saved scores.')
args=parser.parse_args()
def distance(a,b):
 row=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  nxt=[i]
  for j,y in enumerate(b,1):nxt.append(min(nxt[-1]+1,row[j]+1,row[j-1]+(x!=y)))
  row=nxt
 return row[-1]
def parts(words,readings):
 out=[];pos=0
 for w,r in zip(words,readings,strict=True):out.append({'a':pos,'b':pos+len(w),'text':w,'reading':r});pos+=len(w)
 return out
def summarize(rows):
 n=len(rows);chars=sum(len(r['reference']) for r in rows)
 return {'n':n,'exact':sum(r['exact'] for r in rows),'accuracy_pct':100*sum(r['exact'] for r in rows)/n if n else None,'edits':sum(r['edits'] for r in rows),'reference_characters':chars,'cer_pct':100*sum(r['edits'] for r in rows)/chars if chars else None,'kana_coverage_pct':100*sum(r['kana_output'] for r in rows)/n if n else None}
items=[];excluded=[];lineitems=[];errors=[]
for song in read(OUT/'references.json'):
 sid=song['song'];inputs=read(OUT/'inputs'/f'{sid}.json')
 predictions={m:read(OUT/'predictions'/m/f'{sid}.json') for m in METHODS}
 for idx,(gold,inp) in enumerate(zip(song['lines'],inputs['lines'],strict=True)):
  assert gold['id']==inp['id'];source=inp['text'];gg=parts(inp['words'],[w['reading'] for w in gold['words']]);pp={}
  boundaries={0,len(source),*[p['b'] for p in gg]}
  for m in METHODS:
   row=predictions[m]['lines'][idx];assert row['id']==gold['id']
   pp[m]=parts(inp['words'],row['readings']) if 'readings' in row else row['parts']
   assert ''.join(p['text'] for p in pp[m])==source
   assert [(p['a'],p['b']) for p in pp[m]]==[(sum(len(x['text']) for x in pp[m][:i]),sum(len(x['text']) for x in pp[m][:i+1])) for i,p in enumerate(pp[m])]
   boundaries&={0,len(source),*[p['b'] for p in pp[m]]}
   if row.get('error'):errors.append({'song':sid,'line':gold['id'],'method':m,'error':row['error']})
  spans=list(zip(sorted(boundaries)[:-1],sorted(boundaries)[1:]))
  for a,b in spans:
   ref=clean(''.join(p['reading'] for p in gg if a<=p['a'] and p['b']<=b));text=source[a:b]
   needs=bool(re.search('[一-鿿々〆]',text))
   if not needs or not kana(ref):
    excluded.append({'song':sid,'line':gold['id'],'text':text,'reference':ref,'reason':'no_kanji' if not needs else 'reference_not_kana'});continue
   for m in METHODS:
    pred=clean(''.join(p['reading'] for p in pp[m] if a<=p['a'] and p['b']<=b))
    items.append({'song':sid,'line':gold['id'],'a':a,'b':b,'source':text,'method':m,'reference':ref,'prediction':pred,'exact':pred==ref,'edits':distance(ref,pred),'kana_output':kana(pred)})
  ref=clean(''.join(p['reading'] for p in gg))
  if kana(ref):
   for m in METHODS:
    pred=clean(''.join(p['reading'] for p in pp[m]))
    lineitems.append({'song':sid,'line':gold['id'],'source':source,'method':m,'reference':ref,'prediction':pred,'exact':pred==ref,'edits':distance(ref,pred),'kana_output':kana(pred)})
metrics=[]
for scope,rows in [('kanji_spans',items),('japanese_lines',lineitems)]:
 for m in METHODS:
  selected=[r for r in rows if r['method']==m]
  for sid in ['ALL','PRIMARY',*[s['song'] for s in read(OUT/'references.json')]]:
   rr=[r for r in selected if sid=='ALL' or (sid=='PRIMARY' and r['song'] in PROTOCOL['primary_songs']) or r['song']==sid]
   result={'scope':scope,'method':m,'song':sid,**summarize(rr)}
   metrics.append(result)
def save(name,rows):
 if args.method:
  previous=read(OUT/f'{name}.json')
  assert len(previous)==len(rows),f'{name}: scoring population changed'
  kept=[]
  for old,new in zip(previous,rows,strict=True):
   identity=('scope','method','song') if name=='metrics' else ('song','line','method','a','b','source','reference')
   assert {k:old.get(k) for k in identity}=={k:new.get(k) for k in identity},f'{name}: scoring partitions changed'
   if new.get('method')==args.method:
    kept.append(new);continue
   assert old==new,(name,'Other method changed')
   kept.append(old)
  rows=kept
 dump(OUT/f'{name}.json',rows)
save('metrics',metrics);save('items',items);save('lines',lineitems);save('excluded',excluded);save('errors',errors)
for r in metrics:
 if r['song']=='ALL':print(r['scope'],r['method'],r['exact'],r['n'],round(r['accuracy_pct'],2),round(r['cer_pct'],2))
