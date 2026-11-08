"""Fixed denominators, song macro primary; descriptive subsets without reweighting."""
from ablation_common import *
import collections,csv,gzip,math
import numpy as np

targets=read(OUT/'targets.json')
gold={g['key']:{**g,'song':s['id'],'line':l['index']} for s in targets for l in s['lines'] for g in l['groups']}

def summary(rows):
    n=len(rows);valid=[r for r in rows if r['prediction'] is not None]
    err=np.array([[r['prediction'][i]-r['reference'][i] for i in (0,1)] for r in valid]).reshape(-1,2)
    absolute=np.abs(err)
    result={'n':n,'valid':len(valid),'missing':n-len(valid),
            'hit100':int(np.all(absolute<=.100000001,axis=1).sum()),'hit200':int(np.all(absolute<=.200000001,axis=1).sum()),
            'gt1s':int(np.any(absolute>1,axis=1).sum())}
    for ms in (100,200):result[f'rate{ms}']=result[f'hit{ms}']/n if n else None
    if len(valid):
        for i,name in enumerate(['start','end']):
            result[name+'_mae_ms']=float(absolute[:,i].mean()*1000)
            result[name+'_p95_ms']=float(np.percentile(absolute[:,i],95)*1000)
            result[name+'_bias_ms']=float(err[:,i].mean()*1000)
        ratios=[(r['prediction'][1]-r['prediction'][0])/(r['reference'][1]-r['reference'][0]) for r in valid]
        result['duration_ratio_median']=float(np.median(ratios))
        result['collapsed']=sum(r['reference'][1]-r['reference'][0]>=.12 and (r['prediction'][1]-r['prediction'][0]<.04 or ratio<.25) for r,ratio in zip(valid,ratios))
        result['short_end_200ms']=int((err[:,1]<-.2).sum())
        result['late_end_200ms']=int((err[:,1]>.2).sum())
    return result

all_rows=[];completion=[]
files={p.with_suffix('') if p.suffix=='.gz' else p for p in (OUT/'predictions').glob('*/*/*/*.json*')}
for file in sorted(files):
    data=read(file);identity={k:data[k] for k in ('separator','backend','strategy','song')}
    pred={u['key']:u for u in data['units']}
    expected=[g for g in gold.values() if g['song']==data['song']]
    assert len(pred)==len(expected),file
    for g in expected:
        row={**identity,'key':g['key'],'line':g['line'],'text':g['text'],'reading':g['reading'],
             'paired':g['paired'],'tags':g['tags'],'reference':[g['start'],g['end']],**pred[g['key']]}
        all_rows.append(row)
    completion.append({**identity,'seconds':data['seconds'],'cases':len(data['cases']),
                       'errors':sum('error' in c for c in data['cases']),
                       'peak_gib':max((c.get('peak_gib',0) for c in data['cases']),default=0)})

# Original product result is a separate control, with original IDs and completion.
for sep in ('demucs','bs','kim'):
    for s in targets:
        file=(PREVIOUS/'baseline'/(s['id']+'.json')) if sep=='demucs' else OUT/'product'/sep/(s['id']+'.json')
        if not file.exists() and not Path(str(file)+'.gz').exists():continue
        data=read(file);native={r['unit_id']:r for r in data['result']['units']};by_object=collections.defaultdict(list)
        for m in data['projection']['mapping']:by_object[m['object_id']].append(native[m['unit_id']])
        for line in s['lines']:
            for g in line['groups']:
                first=by_object.get(g['ids'][0],[]);last=by_object.get(g['ids'][-1],[])
                a=first[0]['proposed_timing']['start'] if first else None;b=last[-1]['proposed_timing']['end'] if last else None
                value=[a['time'],b['time']] if a and b and b['time']>a['time'] else None
                all_rows.append({'separator':sep,'backend':'product','strategy':'concat','song':s['id'],
                    'key':g['key'],'line':line['index'],'text':g['text'],'reading':g['reading'],
                    'paired':g['paired'],'tags':g['tags'],'reference':[g['start'],g['end']],'prediction':value})

grouped=collections.defaultdict(list)
for r in all_rows:
    if not r['paired'] and gold[r['key']]['lang']!='yue':continue
    cohort=('mixed_yue_fixed_reading' if gold[r['key']]['lang']=='yue' else
            'primary' if r['song'] in PRIMARY else 'teochew_kana' if r['song']=='s13' else 'mixed_japanese')
    for subset in ['all']+r['tags']:
        grouped[(r['separator'],r['backend'],r['strategy'],cohort,subset)].append(r)
results=[];by_song=[]
for key,rows in grouped.items():
    identity=dict(zip(['separator','backend','strategy','cohort','subset'],key))
    individual=[]
    for sid in sorted({r['song'] for r in rows}):
        stat=summary([r for r in rows if r['song']==sid]);individual.append(stat)
        by_song.append({**identity,'song':sid,**stat})
    results.append({**identity,**summary(rows),'songs':len(individual),
                    'macro100':float(np.mean([s['rate100'] for s in individual])),
                    'macro200':float(np.mean([s['rate200'] for s in individual]))})

# Adjacent identical-phone boundary pairs: both end of left and start of right.
pairs=[]
predictions=collections.defaultdict(dict)
for r in all_rows:predictions[(r['separator'],r['backend'],r['strategy'],r['song'])][r['key']]=r
for identity,lookup in predictions.items():
    sep,backend,strategy,sid=identity
    if sid not in PRIMARY:continue
    song=next(s for s in targets if s['id']==sid)
    for l in song['lines']:
        for left,right in zip(l['groups'],l['groups'][1:]):
            if not left['paired'] or not right['paired']:continue
            a,b=sum(left['phone_groups'],[]),sum(right['phone_groups'],[])
            kind='identical' if a==b else 'same_edge_phone' if a[-1]==b[0] else None
            if kind is None:continue
            p,q=lookup[left['key']]['prediction'],lookup[right['key']]['prediction']
            pairs.append({'separator':sep,'backend':backend,'strategy':strategy,'song':sid,'kind':kind,
                          'left':left['key'],'right':right['key'],'reference':[left['end'],right['start']],
                          'prediction':[p[1],q[0]] if p and q else None})
pair_stats=[]
for key in sorted({(p['separator'],p['backend'],p['strategy'],p['kind']) for p in pairs}):
    rows=[p for p in pairs if (p['separator'],p['backend'],p['strategy'],p['kind'])==key]
    valid=[p for p in rows if p['prediction'] is not None]
    errors=np.array([[p['prediction'][i]-p['reference'][i] for i in (0,1)] for p in valid]).reshape(-1,2)
    pair_stats.append(dict(zip(['separator','backend','strategy','kind'],key))|{
        'n':len(rows),'valid':len(valid),'hit100':int(np.all(np.abs(errors)<=.100000001,axis=1).sum()),
        'left_end_mae_ms':float(np.abs(errors[:,0]).mean()*1000) if len(valid) else None,
        'right_start_mae_ms':float(np.abs(errors[:,1]).mean()*1000) if len(valid) else None,
        'gap_mae_ms':float(np.abs(errors[:,1]-errors[:,0]).mean()*1000) if len(valid) else None})

dump(OUT/'metrics.json',{'aggregate':results,'by_song':by_song,'repeat_boundaries':pair_stats,'completion':completion})
with gzip.open(OUT/'scored-units.json.gz','wt',encoding='utf-8') as f:
    import json
    json.dump(all_rows,f,ensure_ascii=False)
dump(OUT/'repeat-boundary-pairs.json',pairs)
columns=['separator','backend','strategy','cohort','subset','songs','n','valid','hit100','hit200','macro100','macro200','missing','gt1s','start_mae_ms','end_mae_ms','end_bias_ms','collapsed']
with (OUT/'summary.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');writer.writeheader();writer.writerows(results)
for r in results:
    if r['cohort']=='primary' and r['subset']=='all':
        print(r['separator'],r['backend'],r['strategy'],r['songs'],f"{r['macro100']:.4f}",r['hit100'],r['missing'],r['gt1s'])
