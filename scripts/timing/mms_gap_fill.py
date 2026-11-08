"""Fixed, reference-free intraline gap fill followed by isolated reference scoring."""
from ablation_common import *
import collections,time,numpy as np,gzip,json
DEST=ROOT/'results/mms-gap-fill'
protocol=read(ROOT/'configs/mms-gap-fill.json')
variants=protocol['variants'];targets=read(OUT/'targets.json');songs_by_id={s['id']:s for s in targets if s['id'] in PRIMARY}
allrows=[];decisions=[];runtimes=[]
for sep in ('demucs','bs','kim'):
 for strategy in ('concat','padded','full','auto_nf','auto_mms','human','fixed_cores','auto_mms_pause'):
  if sep=='demucs' and strategy=='fixed_cores':continue
  for sid,song in songs_by_id.items():
   data=read(result_path(sep,'mms_fa',strategy,sid));base={u['key']:u['prediction'] for u in data['units']}
   for variant,cap in variants.items():
    t=time.perf_counter();pred=dict(base);edited=set()
    if variant!='baseline':
     for line in song['lines']:
      for left,right in zip(line['groups'],line['groups'][1:]):
       a,b=base[left['key']],base[right['key']]
       if a is None or b is None or a[1]<=a[0] or b[1]<=b[0]:continue
       gap=b[0]-a[1]
       if gap>0 and (cap is None or gap<=cap+1e-9):
        pred[left['key']]=[a[0],b[0]];edited.add(left['key'])
        decisions.append({'separator':sep,'strategy':strategy,'song':sid,'variant':variant,'left':left['key'],'right':right['key'],'before':a,'after':pred[left['key']],'gap_seconds':gap})
    runtimes.append({'separator':sep,'strategy':strategy,'song':sid,'variant':variant,'seconds':time.perf_counter()-t,'changed':len(edited)})
    # Reference times are consulted only after every output for this variant is fixed.
    for line in song['lines']:
     for i,g in enumerate(line['groups']):
      if not g['paired']:continue
      final=i==len(line['groups'])-1
      subsets=['all','line_final' if final else 'nonfinal']
      if g['end']-g['start']>=.6-1e-9:subsets.append('sustained')
      if not final and line['groups'][i+1]['paired'] and line['groups'][i+1]['start']-g['end']>=.1-1e-9:subsets.append('before_reference_pause')
      a,b=base[g['key']],pred[g['key']]
      allrows.append({'separator':sep,'strategy':strategy,'song':sid,'variant':variant,'key':g['key'],'reference':[g['start'],g['end']],'prediction':b,'baseline':a,'subsets':subsets,'changed':g['key'] in edited})
def summary(rows):
 valid=[r for r in rows if r['prediction'] is not None];e=np.array([[p-g for p,g in zip(r['prediction'],r['reference'])] for r in valid]).reshape(-1,2)
 hit=lambda p,g:bool(p is not None and max(abs(p[i]-g[i]) for i in (0,1))<=.100000001)
 out={'n':len(rows),'valid':len(valid),'missing':len(rows)-len(valid),'changed':sum(r['changed'] for r in rows),'hit100':int(np.all(np.abs(e)<=.100000001,axis=1).sum()),'hit200':int(np.all(np.abs(e)<=.200000001,axis=1).sum()),'over_1s':int(np.any(np.abs(e)>1,axis=1).sum()),'gained100':sum(hit(r['prediction'],r['reference']) and not hit(r['baseline'],r['reference']) for r in rows),'lost100':sum(hit(r['baseline'],r['reference']) and not hit(r['prediction'],r['reference']) for r in rows)}
 for j,name in enumerate(('start','end')):
  for label,func in [('mae',lambda x:np.abs(x).mean()),('bias',np.mean),('abs_p95',lambda x:np.quantile(np.abs(x),.95))]:out[f'{name}_{label}_ms']=float(func(e[:,j])*1000) if len(e) else None
 out['early_end_200']=int((e[:,1]<-.2).sum());out['late_end_200']=int((e[:,1]>.2).sum());out['rate100']=out['hit100']/len(rows) if rows else None
 return out
pooled=collections.defaultdict(list)
for r in allrows:
 for subset in r['subsets']:pooled[(r['separator'],r['strategy'],r['variant'],subset)].append(r)
metrics=[]
for (sep,strategy,variant,subset),rows in pooled.items():
 per=[]
 for sid in sorted(set(r['song'] for r in rows)):
  stat=summary([r for r in rows if r['song']==sid]);per.append(stat)
  metrics.append({'separator':sep,'strategy':strategy,'variant':variant,'subset':subset,'song':sid,**stat})
 metrics.append({'separator':sep,'strategy':strategy,'variant':variant,'subset':subset,'song':'ALL',**summary(rows),'macro100':sum(s['rate100'] for s in per)/len(per)})
dump(DEST/'metrics.json',metrics);dump(DEST/'runtime.json',runtimes)
with gzip.GzipFile(filename=str(DEST/'edits.json.gz'),mode='wb',mtime=0) as stream:
 stream.write((json.dumps(decisions,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode())
for r in metrics:
 if r['song']=='ALL' and r['separator']=='demucs' and r['strategy'] in ('full','concat','human') and r['subset']=='all':print(r['strategy'],r['variant'],r['hit100'],round(100*r['macro100'],2),round(r['end_mae_ms'],2),r['gained100'],r['lost100'])
