from common import *
import re,unicodedata,numpy as np
from score import measure,valid
rows=[];summary={}
for model in ('nextfire','mms-fa'):
 for sep in ('demucs','bs'):
  key=model+'-'+sep;items=[]
  for song in songs():
   sid=song['id'];data=read(OUT/'studio'/f'{sid}-{sep}-{model}-manual-adopt.json');times={}
   for line in data['document']['lines']:
    for w in line['words']:
     for u in w['rubyUnits'] or [w]:times[u['id']]=(u['beginMs'],u['endMs'])
   for line in song['lines']:
    for u in line['leaves']:
     clean=''.join(c for c in unicodedata.normalize('NFKC',u['text']) if c.isalnum() or c in "ー'’")
     if not re.fullmatch('[ぁ-ゖァ-ヺー]+',clean):continue
     if not valid(u['start'],u['end']):continue
     a,b=times.get(u['id'],(None,None));a=a/1000 if a is not None else None;b=b/1000 if b is not None else None;ok=valid(a,b)
     items.append({'song':sid,'route':key,'id':u['id'],'text':u['text'],'valid':ok,'start':u['start'],'end':u['end'],'pred_start':a,'pred_end':b,'ds':a-u['start'] if ok else None,'de':b-u['end'] if ok else None})
  per={s['id']:measure([x for x in items if x['song']==s['id']]) for s in songs()}
  summary[key]={'overall':measure(items),'per_song':per,'macro_hit100_pct':float(np.mean([m['hit100_pct'] for m in per.values()]))};rows+=items
 dump(OUT/'scores/studio-leaf-summary.json',summary);dump(OUT/'scores/studio-leaf-items.json',rows)
