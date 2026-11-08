"""Expose fine boundaries hidden by shared long-mark merges."""
from ablation_common import *
import collections
refs={s['id']:s for s in read(PREVIOUS/'reference.json')}
rows=[]
for song in read(OUT/'targets.json'):
    if song['id'] not in PRIMARY:continue
    leaves={g['id']:g for l in refs[song['id']]['lines'] for g in l['leaves']}
    merged=[(l,g) for l in song['lines'] for g in l['groups'] if g['paired'] and len(g['ids'])>1]
    if not merged:continue
    for sep in ('demucs','bs','kim'):
        file=PREVIOUS/'baseline'/(song['id']+'.json') if sep=='demucs' else OUT/'product'/sep/(song['id']+'.json')
        record=read(file);units={u['unit_id']:u for u in record['result']['units']};by_object=collections.defaultdict(list)
        for m in record['projection']['mapping']:by_object[m['object_id']].append(units[m['unit_id']])
        for line,g in merged:
            for left,right in zip(g['ids'],g['ids'][1:]):
                a=by_object[left][-1]['proposed_timing']['end'];b=by_object[right][0]['proposed_timing']['start']
                truth=[leaves[left]['end'],leaves[right]['start']]
                pred=[a['time'],b['time']] if a and b else None
                rows.append({'separator':sep,'song':song['id'],'line':line['index'],'text':g['text'],
                    'left_text':leaves[left]['text'],'right_text':leaves[right]['text'],'reference':truth,
                    'product_prediction':pred,'endpoint_sources':[a['source'] if a else None,b['source'] if b else None],
                    'hit100':bool(pred and all(abs(x-y)<=.100000001 for x,y in zip(pred,truth))),
                    'tifa_internal_boundary':None,'reason':'No separate phoneme target for standalone long mark; envelope scores do not measure this internal boundary.'})
dump(OUT/'standalone-hold-boundaries.json',rows)
print('standalone hold boundaries',len(rows),'across three separators')
