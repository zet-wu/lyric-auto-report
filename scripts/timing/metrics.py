from common import *
import collections, unicodedata, math, re
import numpy as np

def canonical(s):
    return ''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if c.isalnum())

def language(line,text):
    if line['language']!='ja_en':return line['language']
    value=canonical(text)
    if value.isascii() and any(c.isalpha() for c in value):return 'latin'
    return 'ja'

def summary(rows):
    valid=[r for r in rows if r['prediction'] is not None and r['prediction'][1]>r['prediction'][0]]
    errors=np.array([[p-r['reference'][i] for i,p in enumerate(r['prediction'])] for r in valid],dtype=float).reshape(-1,2)*1000
    return {'n':len(rows),'valid':len(valid),'missing':len(rows)-len(valid),
            'both_100':int(np.sum(np.max(np.abs(errors),axis=1)<=100+1e-6)) if len(valid) else 0,
            'both_200':int(np.sum(np.max(np.abs(errors),axis=1)<=200+1e-6)) if len(valid) else 0,
            'start_mae_ms':float(np.abs(errors[:,0]).mean()) if len(valid) else None,
            'end_mae_ms':float(np.abs(errors[:,1]).mean()) if len(valid) else None,
            'abs_p95_ms':float(np.quantile(np.abs(errors),.95)) if len(valid) else None,
            'max_ms':float(np.abs(errors).max()) if len(valid) else None,
            'over_1s':int(np.sum(np.max(np.abs(errors),axis=1)>1000)) if len(valid) else 0}

def interval(rows):
    if not rows or any(r['start'] is None or r['end'] is None or r['end']<=r['start'] for r in rows):return None
    return [rows[0]['start'],rows[-1]['end']]

def spans(words):
    result=[]; cursor=0
    for w in words:
        text=canonical(w['text']); a=cursor; cursor+=len(text)
        if text:result.append({**w,'a':a,'b':cursor})
    return result

def cover(words,a,b):
    selected=[w for w in words if w['b']>a and w['a']<b]
    if not selected or selected[0]['a']!=a or selected[-1]['b']!=b:return None
    return interval(selected)

def prediction_by_object(base):
    units={r['unit_id']:r for r in base['result']['units']}
    grouped=collections.defaultdict(list)
    for row in base['projection']['mapping']:grouped[row['object_id']].append(units[row['unit_id']])
    output={}
    for oid,rows in grouped.items():
        a=rows[0]['proposed_timing']['start'];b=rows[-1]['proposed_timing']['end']
        output[oid]=None if a is None or b is None else [a['time'],b['time']]
    return output

all_rows=[]; comparisons=[]; counts=[]
for song in read(OUT/'reference.json'):
    sid=song['id'];base=read(OUT/'baseline'/f'{sid}.json');pred=prediction_by_object(base)
    for line in song['lines']:
        for leaf in line['leaves']:
            if canonical(leaf['text']) and leaf['start'] is not None and leaf['end'] is not None and leaf['end']>leaf['start']:
                all_rows.append({'song':sid,'line':line['index'],'language':language(line,leaf['text']),'method':'studio_leaf','id':leaf['id'],
                                 'text':leaf['text'],'reference':[leaf['start'],leaf['end']],'prediction':pred.get(leaf['id'])})
    for mode in ('untimed','trusted','lead_untimed'):
        path=OUT/'timing'/f'{sid}-{mode}.json'
        failure=OUT/'timing'/f'{sid}-{mode}-error.json'
        if not exists(path) and not exists(failure):continue
        if exists(path):result=read(path)
        else:
            error=read(failure)
            result={'seconds':error['seconds'],'error':error['error'],
                    'report':{'lines':[{'text':line['text'],'words':[]} for line in song['lines']]}}
        lines=result['report']['lines']
        assert len(lines)==len(song['lines'])
        for line,output in zip(song['lines'],lines):
            assert canonical(output['text'])==canonical(line['text'])
            native=spans(output['words'])
            # Exclude retained human ranges and coarse-only fallbacks from TIFA accuracy.
            for w in native:
                if set(w.get('flags',[])) & {'lrc_review_placeholder','text_coarse_review_placeholder','tifa_unresolved_unit'}:
                    w['start']=w['end']=None
            gold=spans(line['words'])
            baseline=[]
            for w in gold:
                children=[l for l in line['leaves'] if l['word_id']==w['id']]
                first=pred.get(children[0]['id']) if children else None
                last=pred.get(children[-1]['id']) if children else None
                baseline.append({**w,'start':first[0] if first else None,'end':last[1] if last else None})
                if w['start'] is None or w['end'] is None or w['end']<=w['start']:continue
                for method,value in [('studio_surface',cover(baseline,w['a'],w['b'])),(f'timing_{mode}',cover(native,w['a'],w['b']))]:
                    all_rows.append({'song':sid,'line':line['index'],'language':language(line,w['text']),'method':method,'comparison':mode,
                                     'text':w['text'],'reference':[w['start'],w['end']],'prediction':value})
            common=sorted(({w['a'] for w in gold}|{w['b'] for w in gold}) & ({w['a'] for w in native}|{w['b'] for w in native}))
            for a,b in zip(common,common[1:]):
                truth=cover(gold,a,b)
                if truth is None: continue
                for method,words in [('studio',baseline),('timing',native)]:
                    text=''.join(w['text'] for w in gold if w['a']>=a and w['b']<=b)
                    comparisons.append({'song':sid,'line':line['index'],'language':language(line,text),'mode':mode,'method':method,
                                        'a':a,'b':b,'reference':truth,'prediction':cover(words,a,b)})
        counts.append({'song':sid,'mode':mode,'seconds':result['seconds'],'manual_lines':result['report'].get('manual_timing_lines',[]),
                       'partial_lines':result['report'].get('partial_timing_lines',[]),'error':result.get('error')})
grouped=collections.defaultdict(list)
for row in all_rows:grouped[(row['song'],row['language'],row['method'],row.get('comparison'))].append(row)
paired=collections.defaultdict(list)
for row in comparisons:paired[(row['song'],row['language'],row['mode'],row['method'])].append(row)
dump(OUT/'metrics.json',{'by_song':[{'song':k[0],'language':k[1],'method':k[2],'comparison':k[3],**summary(v)} for k,v in grouped.items()],
                         'paired_common_groups':[{'song':k[0],'language':k[1],'mode':k[2],'method':k[3],**summary(v)} for k,v in paired.items()],
                         'completion':counts})
dump(OUT/'scored-units.json',all_rows)
dump(OUT/'paired-common-units.json',comparisons)

controlled=OUT/'controlled-tifa-raw.json'
if exists(controlled):
    raw={r['id']:r for r in read(controlled)['results']};controlled_rows=[]
    for row in read(OUT/'controlled-input-audit.json')['rows']:
        output=raw[row['id']]
        assert len(output['texts'])==len(row['groups'])
        for i,g in enumerate(row['groups']):
            indices=[j for j,owner in enumerate(output['owners']) if owner==i+1]
            valid=indices and all(output['spans'][j][1]>output['spans'][j][0] for j in indices)
            tifa=[output['spans'][indices[0]][0]+row['offset'],output['spans'][indices[-1]][1]+row['offset']] if valid else None
            for method,value in [('nextfire',row['nextfire'][i]),('tifa',tifa)]:
                controlled_rows.append({'song':row['song'],'line':row['line'],'language':row['language'],'method':method,'text':g['text'],
                                        'reference':[g['start'],g['end']],'prediction':value,'reference_ids':g['ids']})
    groups=collections.defaultdict(list)
    for r in controlled_rows:groups[(r['song'],r['language'],r['method'])].append(r)
    dump(OUT/'controlled-metrics.json',[{'song':k[0],'language':k[1],'method':k[2],**summary(v)} for k,v in groups.items()])
    dump(OUT/'controlled-scored-units.json',controlled_rows)
print('metrics saved',len(all_rows),len(comparisons))

if exists(OUT/'yue-native.json'):
    song=next(s for s in read(OUT/'reference.json') if s['id']=='s11')
    gold={l['index']:l for l in song['lines']};scored=[]
    for row in read(OUT/'yue-native.json'):
        if 'error' in row:continue
        words=[]
        for i,text in enumerate(row['texts']):
            indices=[j for j,owner in enumerate(row['owners']) if owner==i+1]
            valid=indices and all(row['spans'][j][1]>row['spans'][j][0] for j in indices)
            words.append({'text':text,'start':row['spans'][indices[0]][0]+row['offset'] if valid else None,
                          'end':row['spans'][indices[-1]][1]+row['offset'] if valid else None})
        line=gold[int(row['id'])];predicted=spans(words);truth=spans(line['words'])
        assert ''.join(canonical(w['text']) for w in words)==canonical(line['text'])
        for ref in truth:
            scored.append({'line':line['index'],'text':ref['text'],'reference':[ref['start'],ref['end']],
                           'prediction':cover(predicted,ref['a'],ref['b'])})
    dump(OUT/'yue-native-metrics.json',{'summary':summary(scored),'units':scored})
    print('yue',summary(scored))

if exists(OUT/'hybrid-tifa-raw.json'):
    raw={r['id']:r for r in read(OUT/'hybrid-tifa-raw.json')['results']}
    refs={r['id']:r for r in read(OUT/'controlled-input-audit.json')['rows']}
    scored=[];decisions=[]
    for row in read(OUT/'hybrid-protocol.json')['rows']:
        ref=refs[row['id']];native=raw.get(row['id']);candidate=[]
        accepted=native is not None
        previous=row.get('offset',0)
        if native is not None:
            assert len(native['texts'])==len(ref['groups'])
            for i,g in enumerate(ref['groups']):
                indices=[j for j,owner in enumerate(native['owners']) if owner==i+1]
                valid=indices and all(native['spans'][j][1]>native['spans'][j][0] for j in indices)
                value=[native['spans'][indices[0]][0]+row['offset'],native['spans'][indices[-1]][1]+row['offset']] if valid else None
                if value is None or not previous<=value[0]<value[1]<=row['end']+.001:accepted=False
                if value is not None:previous=value[1]
                candidate.append(value)
        predictions=candidate if accepted else row['baseline']
        decisions.append({'id':row['id'],'adopted':accepted,'skipped':row.get('skipped')})
        for i,g in enumerate(ref['groups']):
            for method,predicted in [('baseline',row['baseline'][i]),('hybrid',predictions[i])]:
                scored.append({'song':row['song'],'line':row['line'],'language':row['language'],'method':method,
                                'text':g['text'],'reference':[g['start'],g['end']],'prediction':predicted})
    groups=collections.defaultdict(list)
    for row in scored:groups[(row['song'],row['language'],row['method'])].append(row)
    dump(OUT/'hybrid-metrics.json',{'by_song':[{'song':k[0],'language':k[1],'method':k[2],**summary(v)} for k,v in groups.items()],
                                  'decisions':decisions})
    dump(OUT/'hybrid-scored-units.json',scored)

if exists(OUT/'english-tifa-raw.json'):
    raw={r['id']:r for r in read(OUT/'english-tifa-raw.json')['results']};scored=[]
    for row in read(OUT/'english-input-audit.json'):
        output=raw[row['id']];words=[]
        for i,text in enumerate(output['texts']):
            indices=[j for j,owner in enumerate(output['owners']) if owner==i+1]
            valid=indices and all(output['spans'][j][1]>output['spans'][j][0] for j in indices)
            words.append({'text':text,'start':output['spans'][indices[0]][0]+row['offset'] if valid else None,
                          'end':output['spans'][indices[-1]][1]+row['offset'] if valid else None})
        predicted=spans(words);truth=spans(row['reference'])
        assert ''.join(canonical(w['text']) for w in words)==''.join(canonical(w['text']) for w in row['reference'])
        for i,ref in enumerate(truth):
            for method,value in [('nextfire',row['nextfire'][i]),('tifa',cover(predicted,ref['a'],ref['b']))]:
                scored.append({'line':row['id'],'method':method,'text':ref['text'],
                                'reference':[ref['start'],ref['end']],'prediction':value})
    dump(OUT/'english-metrics.json',{'summary':{m:summary([r for r in scored if r['method']==m]) for m in ('nextfire','tifa')},'units':scored})
