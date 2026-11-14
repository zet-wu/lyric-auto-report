"""Score final product output on common original-text boundaries, no interpolation."""
from common import *
import math,unicodedata,xml.etree.ElementTree as ET
import numpy as np
T='{http://www.w3.org/ns/ttml}';S='{http://www.w3.org/ns/ttml#styling}'
ROUTES={'studio-nextfire':('studio','nextfire','demucs'),'studio-mms-fa':('studio','mms-fa','demucs'),'milikara':('milikara',None,'milikara'),'timing':('timing',None,'bs'),'sug-nextfire':('sug','nextfire','sug'),'sug-mms-fa':('sug','mms-fa','sug'),'yohane':('yohane',None,'yohane'),'fa-kara':('fa-kara',None,'bs')}
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKC',s).lower() if c.isalnum() or c=='ー')
def valid(a,b):return isinstance(a,(int,float)) and isinstance(b,(int,float)) and math.isfinite(a+b) and 0<=a<b

def clock(x):
 if not x:return None
 if x=='[error]':return None
 if x.startswith('['):m,s,c=map(float,x.strip('[]').split(':'));return m*60+s+c/100
 if ':' in x:
  h,m,s=map(float,x.split(':'));return h*3600+m*60+s
 return float(x.removesuffix('s'))
def row(text,a,b,scale=1):return {'text':text,'start':a/scale if a is not None else None,'end':b/scale if b is not None else None}
def envelope(parts):
 if not parts or any(not valid(x['start'],x['end']) for x in parts):return None,None
 return min(x['start'] for x in parts),max(x['end'] for x in parts)
def positioned(parts,expected):
 out=[];pos=0
 for w in parts:
  text=norm(w['text'])
  if not text:continue
  out.append({**w,'a':pos,'b':pos+len(text)});pos+=len(text)
 assert ''.join(norm(w['text']) for w in parts)==norm(expected),(expected,''.join(w['text'] for w in parts))
 return out

def load_prediction(sid,route,group):
 kind,model,own=ROUTES[route];sep='bs' if group=='G2' else own;cond='auto' if group=='G3' else 'manual'
 name=f'{sid}-{sep}'+(f'-{model}' if model else '')+f'-{cond}.json'
 folder=OUT/('milikara/runs' if kind=='milikara' else kind)
 path=folder/name
 if not exists(path):return [],{'status':'pending','path':str(path)}
 r=read(path);meta={'status':r['status'],'path':str(path),'error':r.get('error')}
 if r['status']!='ok':return [],meta
 lines=[]
 if kind=='studio':
  adopted=read(path.with_name(path.stem+'-adopt.json'))
  for l in adopted['document']['lines']:lines.append([row(w['text'],w['beginMs'],w['endMs'],1000) for w in l['words']])
 elif kind=='milikara':
  ex=r['export'];times={u['unit_id']:u for u in ex['units']}
  for l in ex['lyrics']['lines']:
   if not l['sing']:continue
   parts=[]
   for w in l['segments']:
    timed=[times.get(u['id'],{}) for u in w['units']]
    a,b=envelope([row('',u.get('start_ms'),u.get('end_ms'),1000) for u in timed])
    parts.append(row(w['surface'],a,b))
   lines.append(parts)
 elif kind=='timing':
  for l in r['result']['lines']:
   parts=[]
   for w in l['words']:
    missing=any(f in w.get('flags',[]) for f in ('lrc_review_placeholder','text_coarse_review_placeholder','tifa_unresolved_unit'))
    parts.append(row(w['text'],None if missing else w['start'],None if missing else w['end']))
   lines.append(parts)
 elif kind=='sug':
  from sug_saved import saved_segments
  lines=[[row(p['text'],p['start'],p['end']) for p in l] for l in saved_segments(r)]
 elif kind=='fa-kara':
  # Score the native ASS export: its karaoke durations can differ from the
  # postprocessed intermediate items, including cumulative gap handling.
  events=[x for x in r['ass'].splitlines() if x.startswith('Dialogue:')]
  for event in events:
   fields=event.split(',',9);t=clock(fields[1]);parts=[]
   for duration,text in re.findall(r'\{\\k(-?\d+)\}([^{}]*)',fields[9]):
    end=t+int(duration)/100
    if text.startswith('#|'):
     assert parts,'Ruby continuation without base'
     parts[-1]['end']=end
    elif text:
     base=text.split('|<',1)[0]
     parts.append(row(base,t,end))
    t=end
   lines.append(parts)
 elif kind=='yohane':
  src=read(OUT/'yohane/inputs'/f'{sid}.json')
  # ASS durations are snapped to the next syllable and rounded to centiseconds.
  events=[x for x in r['ass'].splitlines() if x.startswith('Dialogue:')]
  assert len(events)==len(src['lines'])
  for l,event in zip(src['lines'],events):
   fields=event.split(',',9);t=clock(fields[1]);chunks=re.findall(r'\{\\k(-?\d+)\}([^{}]*)',fields[9]);groups=[];cur=[]
   for dur,text in chunks:
    end=t+int(dur)/100;cur.append((t,end));t=end
    if text.endswith(' '):groups.append(cur);cur=[]
   if cur:groups.append(cur)
   words=[w for w in l['words'] if w['roman']];assert len(groups)==len(words),(sid,len(groups),len(words))
   lookup={w['id']:(g[0][0],g[-1][1]) for w,g in zip(words,groups)}
   lines.append([row(w['text'],*lookup.get(w['id'],(None,None))) for w in l['words']])
 return lines,meta

def boundaries(parts):
 # Coarse review placeholders do not force all other products to sentence granularity.
 if not parts or not any(valid(p['start'],p['end']) for p in parts):return None
 return {0,*[p['b'] for p in parts]}
def measure(items):
 good=[x for x in items if x['valid']];n=len(items)
 a=np.array([abs(x['ds'])*1000 for x in good]);b=np.array([abs(x['de'])*1000 for x in good]);h100=sum(max(abs(x['ds']),abs(x['de']))<=.100000001 for x in good);h200=sum(max(abs(x['ds']),abs(x['de']))<=.200000001 for x in good)
 return {'n':n,'valid':len(good),'missing':n-len(good),'hit100':h100,'hit200':h200,'hit100_pct':100*h100/n if n else None,'hit200_pct':100*h200/n if n else None,'start_mae_ms':float(a.mean()) if len(a) else None,'end_mae_ms':float(b.mean()) if len(b) else None,'start_p95_ms':float(np.percentile(a,95)) if len(a) else None,'end_p95_ms':float(np.percentile(b,95)) if len(b) else None,'over1s':sum(max(abs(x['ds']),abs(x['de']))>1 for x in good)}
def main():
 allrows=[];summary={};states=[];partitions=[];loaded={};shared_edges={}
 GROUPS={g:[k for k in ROUTES if g!='G3' or k not in ('yohane','fa-kara')] for g in ('G1','G2','G3')}
 for song in songs():
  sid=song['id']
  for group,routes in GROUPS.items():
   for route in routes:
    lines,meta=load_prediction(sid,route,group);states.append({'group':group,'song':sid,'route':route,**meta})
    if lines:
     assert len(lines)==len(song['lines']),(sid,route,len(lines),len(song['lines']))
     loaded[group,sid,route]=[positioned(p,l['text']) for p,l in zip(lines,song['lines'])]
    else:loaded[group,sid,route]=[[] for _ in song['lines']]
  for li,l in enumerate(song['lines']):
   gold=positioned(l['words'],l['text']);
   for group,routes in GROUPS.items():
    edges={0,*[w['b'] for w in gold]}
    for route in routes:
     b=boundaries(loaded[group,sid,route][li])
     if b is not None:edges&=b
    shared_edges[group,sid,li]=sorted(edges)
 for group,routes in GROUPS.items():
  summary[group]={}
  for song in songs():
   sid=song['id'];pred={route:loaded[group,sid,route] for route in routes}
   for li,l in enumerate(song['lines']):
    gold=positioned(l['words'],l['text']);edges=shared_edges[group,sid,li];text=norm(l['text'])
    for left,right in zip(edges,edges[1:]):
     if not re.search('[\u3040-\u30ff\u3400-\u9fff]',text[left:right]):continue
     truth=[w for w in gold if left<=w['a'] and w['b']<=right];a,b=envelope(truth)
     if not valid(a,b):continue
     overlap=any(a<bg[1] and b>bg[0] for bg in song['background_intervals'])
     key={'group':group,'song':sid,'line':li,'a':left,'b':right,'text':text[left:right],'merged_boundaries':max(0,len(truth)-1),'start':a,'end':b,'overlap':overlap};partitions.append(key)
     for route in routes:
      pieces=[w for w in pred[route][li] if left<=w['a'] and w['b']<=right]
      x,y=envelope(pieces);covered=bool(pieces) and pieces[0]['a']==left and pieces[-1]['b']==right
      ok=covered and valid(x,y)
      allrows.append({**key,'route':route,'pred_start':x,'pred_end':y,'valid':ok,'ds':x-a if ok else None,'de':y-b if ok else None})
  for route in routes:
   selected=[r for r in allrows if r['group']==group and r['route']==route];per={s['id']:measure([x for x in selected if x['song']==s['id']]) for s in songs()}
   summary[group][route]={'overall':{**measure(selected),'merged_boundaries':sum(x['merged_boundaries'] for x in selected)},'per_song':per,'overlap':measure([x for x in selected if x['overlap']]),'s15_overlap':measure([x for x in selected if x['song']=='s15' and x['overlap']]),'s15':measure([x for x in selected if x['song']=='s15']),'macro_hit100_pct':float(np.mean([x['hit100_pct'] for x in per.values() if x['n']]))}
 dump(OUT/'scores/items.json',allrows);dump(OUT/'scores/partitions.json',partitions);dump(OUT/'scores/summary.json',summary);dump(OUT/'scores/status.json',states)
 print(json.dumps({g:{r:{k:v for k,v in x['overall'].items() if k in ('n','hit100_pct','missing')} for r,x in routes.items()} for g,routes in summary.items()},indent=2))

if __name__=='__main__':main()
