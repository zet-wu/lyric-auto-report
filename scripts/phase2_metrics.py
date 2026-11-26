"""Phase 2 scoring on common body spans and original human reading units."""
import collections
import csv
import math
import re
import sys
import unicodedata
from shared import ROOT, read, dump, exists, portable
sys.path.insert(0,str(ROOT/'scripts/comparison'))
from comparison import score as legacy
import numpy as np


def measure(rows):
    result=legacy.measure(rows)
    errors=np.array([[row['ds'],row['de']] for row in rows if row['valid']],float).reshape(-1,2)*1000
    result['abs_p95_ms']=float(np.percentile(np.abs(errors),95)) if len(errors) else None
    return result


def table(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    fields=list(dict.fromkeys(key for row in rows for key,value in row.items() if not isinstance(value,(dict,list))))
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        writer.writerows({key:value for key,value in row.items() if not isinstance(value,(dict,list))} for row in rows)


def publish(module,summary,rows,details=None):
    dump(ROOT/'results'/module/'summary.json',summary)
    table(ROOT/'results'/module/'metrics.csv',rows)
    if details is not None:dump(ROOT/'results'/module/'items.json.gz',details)


def span(timing):
    a,b=timing.get('start'),timing.get('end')
    return (a['time'],b['time']) if a and b and legacy.valid(a['time'],b['time']) else (None,None)


def item(song,line,unit,ref,pred,**meta):
    a,b=ref;x,y=pred
    valid=legacy.valid(x,y)
    return {'song':song,'line':line,'unit':unit,'start':a,'end':b,'pred_start':x,'pred_end':y,
            'valid':valid,'ds':x-a if valid else None,'de':y-b if valid else None,**meta}


def primary_reference_unit(line,leaf):
    if not legacy.valid(leaf['start'],leaf['end']) or not any(char.isalnum() for char in leaf['text']):return False
    clean=''.join(char for char in unicodedata.normalize('NFKC',leaf['text']) if char.isalnum() or char in "ー'’")
    return line.get('language','ja')!='ja' or bool(re.fullmatch('[ぁ-ゖァ-ヺー]+',clean))


def reading_items(song,data):
    result=[]
    times=data.get('object_timings',{})
    for line in song['lines']:
        for index,leaf in enumerate(line['leaves']):
            if not legacy.valid(leaf['start'],leaf['end']) or not any(char.isalnum() for char in leaf['text']):continue
            row=item(song['id'],line['index'],leaf['id'],(leaf['start'],leaf['end']),span(times.get(leaf['id'],{})),text=leaf['text'],reference_kind=leaf['kind'],unit_index=index,primary_reading_unit=primary_reference_unit(line,leaf))
            result.append(row)
    return result


def native_lines(song,data):
    if 'projection' not in data:return [[] for _ in song['lines']]
    times=data.get('object_timings',{}); mapping={entry['unit_id']:entry for entry in data['projection']['mapping']};output={}
    for line in data['projection']['request']['lines']:
        groups=collections.defaultdict(set)
        for unit in line['units']:
            groups[tuple(unit['source_range'])].add(mapping[unit['unit_id']]['object_id'])
        parts=[]
        for (a,b),ids in sorted(groups.items()):
            spans=[span(times.get(key,{})) for key in ids]
            valid=all(legacy.valid(*value) for value in spans)
            x=min(value[0] for value in spans) if valid else None;y=max(value[1] for value in spans) if valid else None
            parts.append({'text':line['text'][a:b],'a':len(legacy.norm(line['text'][:a])),'b':len(legacy.norm(line['text'][:b])),'start':x,'end':y})
        output[line['line_id']]=parts
    return [output.get(line['id'],[]) for line in song['lines']]


def external_lines(song,view):
    legacy.ROUTES['phase2']=(view['tool'],view.get('model','nextfire') if view['tool']=='sug' else None,view['separator'])
    group='G3' if view['input_condition']=='auto' else 'G1'
    lines,state=legacy.load_prediction(song['id'],'phase2',group)
    if lines:
        if len(lines)!=len(song['lines']):raise ValueError(f"Native exported line count {len(lines)} differs from source text {len(song['lines'])}")
        return [legacy.positioned(parts,line['text']) for parts,line in zip(lines,song['lines'],strict=True)],state
    return [[] for _ in song['lines']],state


def common_rows(song,conditions):
    output=[]
    for index,line in enumerate(song['lines']):
        gold=legacy.positioned(line['words'],line['text']); edges={0,*[word['b'] for word in gold]}
        for parts in conditions.values():
            present=legacy.boundaries(parts[index])
            if present is not None:edges &= present
        edges=sorted(edges)
        for a,b in zip(edges,edges[1:]):
            if line.get('language','ja')=='ja' and not re.search('[\u3040-\u30ff\u3400-\u9fff]',legacy.norm(line['text'])[a:b]):continue
            truth=[word for word in gold if a<=word['a'] and word['b']<=b]
            start,end=legacy.envelope(truth)
            if not legacy.valid(start,end):continue
            overlap=any(start<bg[1] and end>bg[0] for bg in song['background_intervals'])
            for name,predictions in conditions.items():
                parts=[word for word in predictions[index] if a<=word['a'] and word['b']<=b]
                covered=bool(parts) and parts[0]['a']==a and parts[-1]['b']==b
                pred=legacy.envelope(parts) if covered else (None,None)
                output.append(item(song['id'],line['index'],f'{line["id"]}:{a}:{b}',(start,end),pred,condition=name,text=legacy.norm(line['text'])[a:b],overlap=overlap))
    return output


def score_alignment_modules(config,jobs,views,refs):
    all_native={};datasets={};states={}
    for module in ('M1','M2','M3','M5','M6'):
        conditions={};state=[]
        for job in jobs:
            if job['module']!=module or job['kind'] not in ('native','tifa'):continue
            condition=job['condition'];conditions[condition]={}
            for sid,path in zip(job['songs'],job['outputs'],strict=True):
                data=read(ROOT/path) if exists(ROOT/path) else {'status':'pending'}
                state.append({'condition':condition,'song':sid,'status':data.get('status','ok'),'error':data.get('error'),'failed_stage':data.get('failed_stage'),'native_cases':data.get('cases',[]),'line_failures':[check for check in data.get('checks',[]) if check.get('status')=='failed']})
                if job['kind']=='native':
                    conditions[condition][sid]=native_lines(refs[sid],data)
                    all_native[module,condition,sid]=data
                else:
                    lines=data.get('result',{}).get('lines',[])
                    conditions[condition][sid]=[legacy.positioned([dict(word,start=None,end=None) if any(flag in word.get('flags',[]) for flag in ('lrc_review_placeholder','tifa_unresolved_unit')) else word for word in line['words']],ref['text']) for line,ref in zip(lines,refs[sid]['lines'])] if lines else [[] for _ in refs[sid]['lines']]
        for view in views:
            if view['module']!=module:continue
            name=view['condition'];conditions[name]={}
            for sid in view['songs']:
                try:lines,status=external_lines(refs[sid],view)
                except Exception as exc:lines=[[] for _ in refs[sid]['lines']];status={'status':'failed','failed_stage':'export','error':{'type':type(exc).__name__,'message':portable(exc)[:500]}}
                conditions[name][sid]=lines;state.append({'condition':name,'song':sid,**status})
        rows=[]
        groups=('G1','G2','G3') if module=='M1' else ('all',)
        for group in groups:
            names=[name for name in conditions if group=='all' or name.startswith(group+'-')]
            for sid in config['modules'][module]['songs']:
                selected={name:conditions[name][sid] for name in names if sid in conditions[name]}
                rows.extend(common_rows(refs[sid],selected))
        table_rows=[]
        for name in conditions:
            rr=[row for row in rows if row['condition']==name]
            for sid in ['ALL',*config['modules'][module]['songs']]:
                selected=[row for row in rr if sid=='ALL' or row['song']==sid]
                if not selected:continue
                table_rows.append({'condition':name,'song':sid,'scope':'all',**measure(selected)})
                if module=='M1':table_rows.append({'condition':name,'song':sid,'scope':'overlap',**measure([row for row in selected if row['overlap']])})
                if module=='M2' and sid in ('y01','jy01'):
                    for subset,(lo,hi) in config['modules']['M2']['line_subsets'][sid].items():table_rows.append({'condition':name,'song':sid,'scope':subset,**measure([row for row in selected if lo<=row['line']<=hi])})
        leaf=[]
        for (mod,name,sid),data in all_native.items():
            if mod==module and data.get('condition') not in ('auto','dictionary'):
                leaf.extend(dict(row,condition=name) for row in reading_items(refs[sid],data))
        leaf_metrics=[{'condition':name,'song':sid,**measure([row for row in leaf if row['primary_reading_unit'] and row['condition']==name and (sid=='ALL' or row['song']==sid)])} for name in conditions for sid in ['ALL',*config['modules'][module]['songs']] if any(row['condition']==name and (sid=='ALL' or row['song']==sid) for row in leaf)]
        all_leaf_metrics=[{'condition':name,'song':sid,**measure([row for row in leaf if row['condition']==name and (sid=='ALL' or row['song']==sid)])} for name in conditions for sid in ['ALL',*config['modules'][module]['songs']] if any(row['condition']==name and (sid=='ALL' or row['song']==sid) for row in leaf)]
        macro=[{'condition':name,'macro_hit100_pct':float(np.mean([row['hit100_pct'] for row in table_rows if row['condition']==name and row['song']!='ALL' and row['scope']=='all' and row['n']]))} for name in conditions if any(row['condition']==name and row['song']!='ALL' and row['scope']=='all' and row['n'] for row in table_rows)]
        summary={'macro':macro,'surface':table_rows,'reading_units':leaf_metrics,'all_reading_units':all_leaf_metrics,'completion':state,'surface_policy':'Shared original body boundaries among native exports; Japanese spans require Japanese body characters as in Phase 1. Missing predictions remain misses.','reading_policy':'Original timed human reading leaves; Japanese primary units use the Phase 1 kana-only criterion. All alphanumeric leaves are retained separately. No interpolation.'}
        publish(module,summary,table_rows+[{**row,'scope':'reading_units'} for row in leaf_metrics]+[{**row,'scope':'all_reading_units'} for row in all_leaf_metrics],rows)
        dump(ROOT/'results'/module/'reading-items.json.gz',leaf)
        datasets[module]=leaf;states[module]=state
    return all_native,datasets,states
