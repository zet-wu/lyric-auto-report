"""Reference-only diagnostics of automatic cores/windows; never used for inference."""
from ablation_common import *
import numpy as np

targets=read(OUT/'targets.json')
core_rows=[];window_rows=[]
for sep in ('demucs','bs','kim'):
    for song in targets:
        sid=song['id'];info=read(OUT/'audio'/sep/(sid+'.json'))
        segments=[(p['source_start']/48000,p['source_end']/48000) for p in info['mapping']['concat']]
        for line in song['lines']:
            for g in line['groups']:
                if not g['paired']:continue
                a,b=g['start'],g['end']
                retained=sum(max(0,min(b,y)-max(a,x)) for x,y in segments)
                core_rows.append({'separator':sep,'song':sid,'key':g['key'],'tags':g['tags'],
                                  'duration':b-a,'retained_fraction':retained/(b-a),
                                  'start_inside':any(x<=a<y for x,y in segments),
                                  'end_inside':any(x<b<=y for x,y in segments)})
        for kind in ('mms','nf','mms_pause'):
            file=(OUT/'windows'/sep/(sid+'.json') if kind=='mms' else
                  OUT/'pause-windows'/sep/(sid+'.json') if kind=='mms_pause' else result_path(sep,'nextfire','concat',sid))
            if not present(file):continue
            data=read(file)
            if kind=='nf':pred={u['key']:u['prediction'] for u in data['units']}
            for line in song['lines']:
                if kind in ('mms','mms_pause'):bounds=data.get('windows',{}).get(str(line['index']))
                else:
                    a=pred.get(line['groups'][0]['key']);b=pred.get(line['groups'][-1]['key'])
                    bounds=[a[0],b[1]] if a and b else None
                if bounds:
                    if kind!='mms_pause':bounds=[max(0,bounds[0]-.3),min(info['duration'],bounds[1]+.3)]
                    if not .1<=bounds[1]-bounds[0]<=60:bounds=None
                gold=line['human_window']
                window_rows.append({'separator':sep,'source':kind,'song':sid,'line':line['index'],
                                    'reference':gold,'window':bounds,
                                    'covers_reference':bool(bounds and bounds[0]<=gold[0]+.02 and bounds[1]>=gold[1]-.02),
                                    'cuts_start_ms':max(0,bounds[0]-gold[0])*1000 if bounds else None,
                                    'cuts_end_ms':max(0,gold[1]-bounds[1])*1000 if bounds else None})
stats=[]
for sep in ('demucs','bs','kim'):
    rows=[r for r in core_rows if r['separator']==sep and r['song'] in PRIMARY]
    stats.append({'separator':sep,'n':len(rows),'start_outside':sum(not r['start_inside'] for r in rows),
                  'end_outside':sum(not r['end_inside'] for r in rows),
                  'retained_seconds_ratio':sum(r['retained_fraction']*r['duration'] for r in rows)/sum(r['duration'] for r in rows),
                  'below_90pct':sum(r['retained_fraction']<.9 for r in rows)})
windows=[]
for sep in ('demucs','bs','kim'):
    for kind in ('mms','nf','mms_pause'):
        rows=[r for r in window_rows if r['separator']==sep and r['source']==kind and r['song'] in PRIMARY]
        windows.append({'separator':sep,'source':kind,'n':len(rows),'available':sum(r['window'] is not None for r in rows),
                        'covers':sum(r['covers_reference'] for r in rows),
                        'cuts_start_gt200ms':sum(r['cuts_start_ms'] is not None and r['cuts_start_ms']>200 for r in rows),
                        'cuts_end_gt200ms':sum(r['cuts_end_ms'] is not None and r['cuts_end_ms']>200 for r in rows)})
dump(OUT/'window-audit.json',{'cores':stats,'windows':windows,'core_units':core_rows,'line_windows':window_rows})
print(stats);print(windows)
