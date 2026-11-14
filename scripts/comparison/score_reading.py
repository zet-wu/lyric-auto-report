"""Score native reading endpoints against fixed manual leaves without interpolation."""
from common import *
from score import ROUTES, T, S, row, clock, norm, valid, positioned, envelope, measure
import xml.etree.ElementTree as ET
from collections import Counter

GROUPS={g:[r for r in ROUTES if g!='G3' or r not in ('yohane','fa-kara')] for g in ('G1','G2','G3')}
def kana(text):
 import unicodedata
 text=unicodedata.normalize('NFKC',text).lower()
 return ''.join(chr(ord(c)-96) if 'ァ'<=c<='ヶ' else c for c in text if c.isalnum() or c=='ー')
def japanese(text):return bool(re.fullmatch('[ぁ-ゖァ-ヺー]+',norm(text)))
def segment(text,units,a=None,b=None):return {'text':text,'units':units,'start':a,'end':b}
def native(sid,route,group):
 kind,model,own=ROUTES[route];sep='bs' if group=='G2' else own;cond='auto' if group=='G3' else 'manual'
 path=OUT/('milikara/runs' if kind=='milikara' else kind)/(f'{sid}-{sep}'+(f'-{model}' if model else '')+f'-{cond}.json')
 r=read(path)
 if r['status']!='ok':return None
 lines=[]
 if kind=='studio':
  for l in read(path.with_name(path.stem+'-adopt.json'))['document']['lines']:
   parts=[]
   for w in l['words']:
    us=[row(u['reading'],u['beginMs'],u['endMs'],1000) for u in w['rubyUnits']]
    if not us and not re.search('[\u3400-\u9fff]',w['text']):us=[row(w['text'],w['beginMs'],w['endMs'],1000)]
    parts.append(segment(w['text'],us,w['beginMs']/1000 if w['beginMs'] is not None else None,w['endMs']/1000 if w['endMs'] is not None else None))
   lines.append(parts)
 elif kind=='milikara':
  ex=r['export'];times={x['unit_id']:x for x in ex['units']}
  for l in ex['lyrics']['lines']:
   if not l['sing']:continue
   parts=[]
   for w in l['segments']:
    us=[]
    for u in w['units']:
     t=times.get(u['id'],{});us.append(row(u['reading'],t.get('start_ms'),t.get('end_ms'),1000))
    parts.append(segment(w['surface'],us))
   lines.append(parts)
 elif kind=='timing':
  for l in r['result']['lines']:
   parts=[]
   for w in l['words']:
    missing=any(x in w.get('flags',[]) for x in ('lrc_review_placeholder','text_coarse_review_placeholder','tifa_unresolved_unit'))
    a,b=(None,None) if missing else (w['start'],w['end'])
    rd=w.get('source_pronunciation') or w.get('reading') or (w['text'] if not re.search('[\u3400-\u9fff]',w['text']) else '')
    parts.append(segment(w['text'],[row(rd,a,b)] if rd else [],a,b))
   lines.append(parts)
 elif kind=='sug':
  from sug_saved import saved_segments
  lines=saved_segments(r)
 elif kind=='fa-kara':
  for event in (x for x in r['ass'].splitlines() if x.startswith('Dialogue:')):
   fields=event.split(',',9);t=clock(fields[1]);parts=[]
   for duration,text in re.findall(r'\{\\k(-?\d+)\}([^{}]*)',fields[9]):
    end=t+int(duration)/100
    if text.startswith('#|'):
     assert parts;parts[-1]['units'].append(row(text[2:],t,end));parts[-1]['end']=end
    elif text:
     base,sep,rd=text.partition('|<');parts.append(segment(base,[row(rd if sep else base,t,end)],t,end))
    t=end
   lines.append(parts)
 elif kind=='yohane':
  src=read(OUT/'yohane/inputs'/f'{sid}.json')
  events=[x for x in r['ass'].splitlines() if x.startswith('Dialogue:')]
  assert len(src['lines'])==len(events)
  for l,event in zip(src['lines'],events):
   fields=event.split(',',9);t=clock(fields[1]);groups=[];cur=[]
   for dur,text in re.findall(r'\{\\k(-?\d+)\}([^{}]*)',fields[9]):
    end=t+int(dur)/100;cur.append(row(text,t,end));t=end
    if text.endswith(' '):groups.append(cur);cur=[]
   if cur:groups.append(cur)
   ws=[w for w in l['words'] if w['roman']];assert len(ws)==len(groups)
   lookup={w['id']:us for w,us in zip(ws,groups)}
   lines.append([segment(w['text'],lookup.get(w['id'],[])) for w in l['words']])
 return lines

def unique_boundaries(a,b):
 """Use a boundary only when every minimum-edit alignment agrees on it."""
 n,m=len(a),len(b)
 f=[[0]*(m+1) for _ in range(n+1)]
 for i in range(n+1):f[i][0]=i
 for j in range(m+1):f[0][j]=j
 for i in range(1,n+1):
  for j in range(1,m+1):f[i][j]=min(f[i-1][j]+1,f[i][j-1]+1,f[i-1][j-1]+(a[i-1]!=b[j-1]))
 z=[[0]*(m+1) for _ in range(n+1)]
 for i in range(n+1):z[i][m]=n-i
 for j in range(m+1):z[n][j]=m-j
 for i in range(n-1,-1,-1):
  for j in range(m-1,-1,-1):z[i][j]=min(z[i+1][j]+1,z[i][j+1]+1,z[i+1][j+1]+(a[i]!=b[j]))
 mapping={}
 for i in range(n+1):
  js=[j for j in range(m+1) if f[i][j]+z[i][j]==f[n][m]]
  if len(js)==1:mapping[i]=js[0]
 # The common surface span fixes the outer endpoints even for reading changes.
 mapping[0]=0;mapping[n]=m
 return mapping

def metrics(rows):
 result=measure(rows);reasons=Counter(r['missing_reason'] for r in rows if not r['valid'])
 result.update(missing_reasons=dict(reasons),merged_units=reasons['merged'],
               merged_boundaries=len({tuple(k) for r in rows for k in r['merged_boundary_keys']}))
 return result

def main():
 items=[]
 for g,routes in GROUPS.items():
  for route in routes:
   for song in songs():
    sid=song['id'];pred=native(sid,route,g)
    romans={u['id']:u['roman'] for l in read(OUT/'yohane/inputs'/f'{sid}.json')['lines'] for w in l['words'] for u in w['units']} if route=='yohane' else {}
    if pred is not None:assert len(pred)==len(song['lines'])
    for li,line in enumerate(song['lines']):
     rows={}
     for u in line['leaves']:
      if not japanese(u['text']) or not valid(u['start'],u['end']):continue
      rows[u['id']]={'group':g,'route':route,'song':sid,'line':li,'id':u['id'],'text':u['text'],'start':u['start'],'end':u['end'],
       'pred_start':None,'pred_end':None,'ds':None,'de':None,'valid':False,'missing_reason':'source_failure' if pred is None else 'reading_mapping',
       'merged_boundary_keys':[],'overlap':any(u['start']<b and u['end']>a for a,b in song['background_intervals'])}
     if pred is None:items.extend(rows.values());continue
     gold=positioned(line['words'],line['text']);parts=positioned(pred[li],line['text'])
     edges=sorted({0,*[w['b'] for w in gold]} & {0,*[p['b'] for p in parts]})
     for left,right in zip(edges,edges[1:]):
      gw=[w for w in gold if left<=w['a'] and w['b']<=right];pw=[p for p in parts if left<=p['a'] and p['b']<=right]
      gids={w['id'] for w in gw};gu=[u for u in line['leaves'] if u['word_id'] in gids and kana(u['text'])]
      native_units=[];opaque_unmapped=False
      for p in pw:
       us=p['units']
       if not us:
        covered=[w for w in gw if p['a']<=w['a'] and w['b']<=p['b']]
        if covered and covered[0]['a']==p['a'] and covered[-1]['b']==p['b']:
         ids={w['id'] for w in covered};rd=''.join(u['text'] for u in gu if u['word_id'] in ids)
         us=[row(rd,p['start'],p['end'])]
        elif norm(p['text']):opaque_unmapped=True
       native_units.extend(us)
      if opaque_unmapped:
       # The text identifies this whole shared span, but its Han-only export
       # cannot assign inner kana boundaries. Preserve only its outer endpoints.
       x,y=envelope(pw);native_units=[row(''.join(u['text'] for u in gu),x,y)]
      pu=[];pos=0
      for u in native_units:
       rd=kana(u['text'])
       if rd:pu.append({**u,'a':pos,'b':pos+len(rd)});pos+=len(rd)
      ga=[];pos=0
      for u in gu:
       rd=kana(romans.get(u['id'],'') if route=='yohane' else u['text'])
       if rd:ga.append({**u,'a':pos,'b':pos+len(rd),'normalized':rd});pos+=len(rd)
      gs=''.join(u['normalized'] for u in ga)
      # One native interval covering the whole shared text span has no internal
      # boundary, even when its reading differs (e.g. Latin surface vs kana ruby).
      if len(pu)==1 and gs:pu=[{**pu[0],'text':gs,'a':0,'b':len(gs)}]
      ps=''.join(kana(u['text']) for u in pu)
      if not gs or not ps:continue
      mapping=unique_boundaries(gs,ps);pe={0,*[u['b'] for u in pu]}
      for u in ga:
       if u['id'] not in rows:continue
       out=rows[u['id']];a,b=mapping.get(u['a']),mapping.get(u['b'])
       out['surface_span']=[left,right];out['reference_reading_span']=[u['a'],u['b']];out['mapped_reading_span']=[a,b]
       if a is None or b is None or b<=a:continue
       merged=[k for k,v in ((u['a'],a),(u['b'],b)) if v not in pe]
       if merged:
        out['missing_reason']='merged';out['merged_boundary_keys']=[[sid,li,left,right,k] for k in merged];continue
       us=[p for p in pu if a<=p['a'] and p['b']<=b];x,y=envelope(us)
       ok=bool(us) and us[0]['a']==a and us[-1]['b']==b and valid(x,y)
       out.update(pred_start=x,pred_end=y,valid=ok,ds=x-u['start'] if ok else None,de=y-u['end'] if ok else None,missing_reason=None if ok else 'invalid_time')
     items.extend(rows.values())
 summary={}
 for g,routes in GROUPS.items():
  summary[g]={}
  for route in routes:
   rows=[r for r in items if r['group']==g and r['route']==route]
   summary[g][route]={'overall':metrics(rows),'per_song':{s['id']:metrics([r for r in rows if r['song']==s['id']]) for s in songs()},
    'overlap':metrics([r for r in rows if r['overlap']]),'s15':metrics([r for r in rows if r['song']=='s15']),
    's15_overlap':metrics([r for r in rows if r['song']=='s15' and r['overlap']])}
 dump(OUT/'scores/reading-items.json',items);dump(OUT/'scores/reading-summary.json',summary)
 print(json.dumps({g:{r:x['overall'] for r,x in rs.items()} for g,rs in summary.items()},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
