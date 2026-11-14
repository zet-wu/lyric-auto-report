"""Independent statistics, group-specific partitions and native reading endpoints."""
from common import *
import math,statistics
from collections import Counter
from score_reading import native
from score import ROUTES
items=read(OUT/'scores/items.json');summary=read(OUT/'scores/summary.json');states=read(OUT/'scores/status.json')
reading_items=read(OUT/'scores/reading-items.json');reading_summary=read(OUT/'scores/reading-summary.json')
assert len(states)==12*(8+8+6)
assert not any(x['status']=='pending' for x in states)

def check_metric(rows,m):
 assert len(rows)==m['n']
 good=[]
 for x in rows:
  assert x['end']>x['start']
  if not x['valid']:continue
  assert x['pred_end']>x['pred_start']>=0
  good.append((abs(x['pred_start']-x['start'])*1000,abs(x['pred_end']-x['end'])*1000))
 assert m['missing']==len(rows)-len(good) and m['valid']==len(good)
 for ms in (100,200):
  assert m[f'hit{ms}']==sum(max(a,b)<=ms+.000001 for a,b in good)
  if rows:assert abs(m[f'hit{ms}_pct']-100*m[f'hit{ms}']/len(rows))<1e-9
 assert m['over1s']==sum(max(a,b)>1000 for a,b in good)
 for i,name in enumerate(('start','end')):
  if not good:assert m[name+'_mae_ms'] is None and m[name+'_p95_ms'] is None;continue
  values=sorted(x[i] for x in good);position=(len(values)-1)*.95;lo=math.floor(position);hi=math.ceil(position)
  p95=values[lo]*(hi-position)+values[hi]*(position-lo) if lo!=hi else values[lo]
  assert abs(m[name+'_mae_ms']-statistics.mean(values))<1e-7
  assert abs(m[name+'_p95_ms']-p95)<1e-7
 if 'merged_units' in m:
  reasons=Counter(r['missing_reason'] for r in rows if not r['valid'])
  assert m['missing_reasons']==dict(reasons) and m['merged_units']==reasons['merged']
  assert m['merged_boundaries']==len({tuple(k) for r in rows for k in r['merged_boundary_keys']})
 elif 'merged_boundaries' in m:assert m['merged_boundaries']==sum(r['merged_boundaries'] for r in rows)

counts={};checked=0
for kind,data,stats in [('text',items,summary),('reading',reading_items,reading_summary)]:
 keys={}
 for group,methods in stats.items():
  for route,record in methods.items():
   rows=[x for x in data if x['group']==group and x['route']==route]
   part={(x['song'],x['id']) if kind=='reading' else (x['song'],x['line'],x['a'],x['b']) for x in rows}
   assert len(part)==len(rows)
   if group in keys:assert keys[group]==part
   else:keys[group]=part
   check_metric(rows,record['overall'])
   for sid,m in record['per_song'].items():check_metric([x for x in rows if x['song']==sid],m)
   for subset in ('s15','overlap','s15_overlap'):
    subset_rows=[r for r in rows if (subset=='overlap' or r['song']=='s15') and (subset=='s15' or r['overlap'])]
    check_metric(subset_rows,record[subset])
   checked+=1
   if kind=='reading':
    for song in songs():
     sid=song['id'];lines=native(sid,route,group)
     selected=[r for r in rows if r['song']==sid]
     if lines is None:assert all(r['missing_reason']=='source_failure' for r in selected);continue
     for li,parts in enumerate(lines):
      starts={round(u['start'],9) for p in parts for u in p['units']+[p] if isinstance(u['start'],(int,float))}
      ends={round(u['end'],9) for p in parts for u in p['units']+[p] if isinstance(u['end'],(int,float))}
      for r in selected:
       if r['line']!=li:continue
       if r['valid']:
        assert r['missing_reason'] is None and not r['merged_boundary_keys']
        assert round(r['pred_start'],9) in starts and round(r['pred_end'],9) in ends,(group,route,sid,r)
       if r['missing_reason']=='merged':assert r['merged_boundary_keys']
 counts[kind]={g:len(k) for g,k in keys.items()}

# The fixed reading denominator is defined independently from native outputs.
import unicodedata,re
expected={(s['id'],u['id']) for s in songs() for l in s['lines'] for u in l['leaves']
 if re.fullmatch('[ぁ-ゖァ-ヺー]+',''.join(c for c in unicodedata.normalize('NFKC',u['text']) if c.isalnum() or c=='ー'))
 and isinstance(u['start'],(int,float)) and isinstance(u['end'],(int,float)) and 0<=u['start']<u['end']}
assert all(k==expected for k in keys.values())
# Native manual Studio readings must exactly reproduce the original leaf scorer.
leaf=read(OUT/'scores/studio-leaf-summary.json')
for group,sep in [('G1','demucs'),('G2','bs')]:
 for model in ('nextfire','mms-fa'):
  a=reading_summary[group]['studio-'+model]['overall'];b=leaf[model+'-'+sep]['overall']
  for key,value in b.items():assert a[key]==value,(group,model,key,a[key],value)
for s in songs():
 for c in ('manual','auto'):
  project=read(OUT/'inputs'/f"{s['id']}-studio-{c}-project.json")
  for line in project['lyrics']['lines']:
   assert line['beginMs'] is None and line['endMs'] is None
   for word in line['words']:
    assert word['beginMs'] is None and word['endMs'] is None
    assert all(u['beginMs'] is None and u['endMs'] is None for u in word['rubyUnits'])
for entry in read(OUT/'input-audit.json')['checks']:assert sha(ROOT/entry['file'])==entry['sha256']
assert not read(OUT/'input-audit.json')['manual_reading_supplements']
sug_audit=read(OUT/'sug-project-audit.json')
assert len(sug_audit['projects'])==68 and sug_audit['round_trip_equal']
for entry in sug_audit['projects']:
 assert entry['round_trip_equal'] and sha(ROOT/entry['path'])==entry['sha256']
 saved=read(ROOT/entry['path'])
 assert entry['checkpoint_count']==sum(len(c['timestamps']) for l in saved['sentences'] for c in l['characters'])
dump(OUT/'verification.json',{'conditions':len(states),'metric_rows':checked,'text_items_by_group':counts['text'],'reading_items_by_group':counts['reading'],
 'independent_mae_p95':True,'untimed_inputs':True,'complete_matrix':True,'native_reading_endpoints_only':True,'manual_studio_leaf_equivalence':True,'native_sug_round_trip_projects':68})
print('Verified',len(states),'song conditions;',checked,'aggregate rows;',counts)
