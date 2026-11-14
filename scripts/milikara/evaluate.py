"""Post-hoc scoring. Not imported by any inference script. References never select outputs."""
from common import *
import numpy as np,csv,collections

def stats(rows):
    es=np.array([r['errors'] for r in rows if r['valid']],float).reshape(-1,2)
    n=len(rows);v=len(es)
    result={'n':n,'valid':v,'missing_or_nonpositive':n-v,'hit100':sum(r['hit100'] for r in rows),'hit200':sum(r['hit200'] for r in rows)}
    result.update({f'hit{t}_pct':100*result[f'hit{t}']/n if n else None for t in [100,200]})
    for label,vals in [('pooled',es.ravel()),('start',es[:,0]),('end',es[:,1])]:
        metrics={'mae':np.mean(np.abs(vals)),'abs_p95':np.quantile(np.abs(vals),.95),'max_abs':np.max(np.abs(vals)),**{f'q{p:g}':np.quantile(vals,p/100) for p in [2.5,5,50,95,97.5]}} if v else {k:None for k in ['mae','abs_p95','max_abs','q2.5','q5','q50','q95','q97.5']}
        result.update({f'{label}_{k}_ms':float(x) if x is not None else None for k,x in metrics.items()})
    result['over_1s']=sum(r['valid'] and max(map(abs,r['errors']))>1000 for r in rows)
    return result

def score(song,r):
    details=[];lines=[]
    assert len(song['lines'])==len(r['predictions'])
    for l,ps in zip(song['lines'],r['predictions']):
        ref=l['reference'];mapped=ps
        assert len(ref)==len(mapped)
        for j,(u,p) in enumerate(zip(ref,mapped)):
            valid=p is not None and p['end']>p['start'] and not p.get('crosses_removed_gap',False)
            es=[(p[k]-u[k])*1000 for k in ['start','end']] if valid else None
            details.append({'song':song['id'],'line':l['index'],'unit':j+1,'language':u['language'],'valid':valid,'errors':es,'hit100':bool(valid and max(map(abs,es))<=100.00001),'hit200':bool(valid and max(map(abs,es))<=200.00001)})
        timed=[p for p in ps if p and p['end']>p['start']]
        if timed:
            a=min(p['start'] for p in timed);b=max(p['end'] for p in timed)
            lines.append({'line':l['index'],'start':a,'end':b,'start_error_ms':1000*(a-l['start']),'end_error_ms':1000*(b-l['end'])})
    diagnostics={'line_max_start_abs_ms':max((abs(l['start_error_ms']) for l in lines),default=0),'line_max_end_abs_ms':max((abs(l['end_error_ms']) for l in lines),default=0),'cross_gap_units':sum(p.get('crosses_removed_gap',False) for row in r['predictions'] for p in row if p),'worst_units':sorted([x for x in details if x['valid']],key=lambda x:max(map(abs,x['errors'])),reverse=True)[:8]}
    return details,diagnostics

if __name__=='__main__':
    songs={s['id']:s for ev,_ in SOURCES for s in read(ev/'references.json')};tables=[];pooled=collections.defaultdict(list);diagnostics={};cache={}
    for path in prediction_paths():
        r=read(path);exp=r['experiment'];sid=r['song'];rows,diag=score(songs[sid],r);pooled[exp]+=(rows if sid!='s13' else []);cache[(exp,sid)]=rows;diagnostics[f'{exp}/{sid}']=diag
        for group in ['japanese','latin','all']:
            tables.append({'experiment':exp,'song':sid,'group':group,**stats([x for x in rows if group=='all' or x['language']==group])})
    for exp,rows in pooled.items():
        for group in ['japanese','latin','all']:tables.append({'experiment':exp,'song':'ALL','group':group,**stats([x for x in rows if group=='all' or x['language']==group])})
    tables.sort(key=lambda r:(r['experiment'],r['group'],r['song']))
    dump(OUT/'metrics.json',tables);dump(OUT/'diagnostics.json',diagnostics)
    with (OUT/'metrics.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(tables[0]));w.writeheader();w.writerows(tables)
    # Every toggle's paired main effect averaged over all other binary settings.
    effects=[]
    for mode in MODES:
        for bit,factor in enumerate(FACTORS):
            for sid in [*songs,'ALL']:
                deltas=[]
                for mask in range(32):
                    code=f'{mask:05b}'
                    if code[bit]=='1':continue
                    on=code[:bit]+'1'+code[bit+1:]
                    def rr(c):return sum([cache.get((f'{mode}/f{c}',s),[]) for s in songs if s!='s13'],[]) if sid=='ALL' else cache.get((f'{mode}/f{c}',sid),[])
                    a=[x for x in rr(code) if x['language']=='japanese'];b=[x for x in rr(on) if x['language']=='japanese']
                    if not a or len(a)!=len(b):continue
                    sa,sb=stats(a),stats(b)
                    deltas.append({'off':code,'on':on,'hit100_delta':sb['hit100']-sa['hit100'],'mae_delta_ms':sb['pooled_mae_ms']-sa['pooled_mae_ms']})
                if deltas:effects.append({'audio':mode,'factor':factor,'song':sid,'pairs':len(deltas),'mean_hit100_delta':float(np.mean([d['hit100_delta'] for d in deltas])),'min_hit100_delta':min(d['hit100_delta'] for d in deltas),'max_hit100_delta':max(d['hit100_delta'] for d in deltas),'mean_mae_delta_ms':float(np.mean([d['mae_delta_ms'] for d in deltas])),'comparisons':deltas})
    dump(OUT/'factor-effects.json',effects)
    # Self-contained human-readable tables, all experiments and all songs.
    for group in ['japanese','latin','all']:
        lines=[f'# MiliKara 消融完整指标：{group}','', '单位 ms；双边命中需起止同时达标。MAE（Mean Absolute Error，平均绝对误差）汇合起点和终点误差。P 表示百分位数；P5/P95 为有符号误差的第 5/95 百分位数，负值表示提前。P2.5/P97.5 给出中央 95% 的误差范围；abs（绝对值）P95 为绝对误差的第 95 百分位数。ALL 表示合并 12 首日语歌曲的全部单元后计分，s13 单列；缺失仍留分母。起止分列与极端值见 metrics.csv。实验名称中的 concat_core 为人声活动核心区间拼接，concat_padded 为带缓冲区间拼接。','', '| 实验 | 歌曲 | 有效/总数 | ≤100 ms | ≤200 ms | MAE | P5 | P95 | P2.5 | P97.5 | abs P95 |','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
        for r in tables:
            if r['group']!=group:continue
            vals=[r['experiment'],r['song'],f"{r['valid']}/{r['n']}",f"{r['hit100']}/{r['n']}",f"{r['hit200']}/{r['n']}"]+[f"{r[k]:.2f}" if r[k] is not None else '—' for k in ['pooled_mae_ms','pooled_q5_ms','pooled_q95_ms','pooled_q2.5_ms','pooled_q97.5_ms','pooled_abs_p95_ms']]
            lines.append('| '+' | '.join(vals)+' |')
        (OUT/f'tables-{group}.md').write_text('\n'.join(lines)+'\n')
    print('Scored',len(cache),'song experiments;',len(pooled),'configurations;',len(tables),'metric rows',flush=True)
    for r in tables:
        if r['song']=='ALL' and r['group']=='japanese' and r['experiment'].split('/')[-1] in ['f00000','f00001','f01111','f11111','runner-plain-d0-r1','runner-self-c1-l4-r1','runner-oracle_start']:
            print(r['experiment'],r['hit100'],r['hit200'],round(r['pooled_mae_ms'],2),flush=True)
