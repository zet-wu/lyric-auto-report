"""Score frozen human-reading refinement predictions after inference."""
from common import *
from evaluate import score,stats
import collections
folder=ROOT/'results/local-refinement';refs={s['id']:s for s in read(OUT/'references.json')}
cache={};metrics=[];pooled=collections.defaultdict(list)
for path in sorted((folder/'predictions').glob('*.json')):
 r=read(path);rows,_=score(refs[r['song']],r);cache[(r['song'],r['baseline'],r['variant'])]=rows
 for group in ('japanese','latin','all'):
  rr=[x for x in rows if group=='all' or x['language']==group];pooled[(r['baseline'],r['variant'],group)]+=rr
  metrics.append({'song':r['song'],'baseline':r['baseline'],'variant':r['variant'],'group':group,**stats(rr)})
for (baseline,variant,group),rows in pooled.items():
 base=pooled[(baseline,'baseline',group)]
 assert [(r['song'],r['line'],r['unit']) for r in rows]==[(r['song'],r['line'],r['unit']) for r in base]
 per=[r for r in metrics if r['baseline']==baseline and r['variant']==variant and r['group']==group and r['song']!='ALL' and r['n']]
 metrics.append({'song':'ALL','baseline':baseline,'variant':variant,'group':group,**stats(rows),'gained100':sum(b['hit100'] and not a['hit100'] for a,b in zip(base,rows)),'lost100':sum(a['hit100'] and not b['hit100'] for a,b in zip(base,rows)),'macro100_pct':sum(r['hit100_pct'] for r in per)/len(per)})
dump(folder/'metrics.json',metrics)
for r in metrics:
 if r['song']=='ALL' and r['group']=='japanese':print(r)
