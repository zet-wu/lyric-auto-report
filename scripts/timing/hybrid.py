"""Additional diagnostic: frozen NextFire windows -> TIFA, no reference times in inference."""
from common import *
timing_imports()
import math, numpy as np, soundfile as sf, torch
from timing.llm_direct import compile_parts
from timing.tifa import run_worker

torch.set_num_threads(8)
folder=CACHE/'hybrid';folder.mkdir(exist_ok=True)
audit=read(OUT/'controlled-input-audit.json')
reference={s['id']:s for s in read(OUT/'reference.json')}
clips=[];records=[]
for sid in dict.fromkeys(row['song'] for row in audit['rows']):
    song=reference[sid];base=read(OUT/'baseline'/f'{sid}.json')
    units={r['unit_id']:r for r in base['result']['units']};by_object={}
    for m in base['projection']['mapping']:by_object.setdefault(m['object_id'],[]).append(units[m['unit_id']])
    def timing(ids):
        first=by_object.get(ids[0],[]);last=by_object.get(ids[-1],[])
        a=first[0]['proposed_timing']['start'] if first else None
        b=last[-1]['proposed_timing']['end'] if last else None
        return [a['time'],b['time']] if a is not None and b is not None and b['time']>a['time'] else None
    wave,rate=sf.read(CACHE/'audio'/f'{Path(song["audio"]).stem}.wav',dtype='float32',always_2d=True)
    wave=wave.mean(axis=1)
    for row in [r for r in audit['rows'] if r['song']==sid]:
        groups=row['groups'];baseline=[timing(g['ids']) for g in groups]
        record={'id':row['id'],'song':sid,'line':row['line'],'language':row['language'],'baseline':baseline}
        records.append(record)
        if not baseline or baseline[0] is None or baseline[-1] is None:
            record['skipped']='missing predicted line endpoints';continue
        left=max(0,baseline[0][0]-.3);right=min(len(wave)/rate,baseline[-1][1]+.3)
        if not .1<=right-left<=35:
            record['skipped']='predicted window outside fixed 0.1..35 second bound';continue
        a,b=math.floor(left*rate),math.ceil(right*rate)
        text=''.join(g['text'] for g in groups)
        parts=compile_parts(text,[{k:g[k] for k in ('text','lang','reading')} for g in groups])
        path=folder/f'{row["id"]}.wav';sf.write(path,wave[a:b],rate,subtype='FLOAT')
        path.with_suffix('.txt').write_text(text)
        record.update(offset=a/rate,end=b/rate)
        clips.append({'id':row['id'],'audio':str(path),'languages':['ja'],'llm_direct_parts':parts})
dump(OUT/'hybrid-protocol.json',{'reason':'Test whether TIFA can refine current predictions without human line windows',
    'window':'first/last baseline proposed endpoints +/-300 ms, original-axis shared Demucs; 0.1..35 s',
    'targets':'same kana groups as controlled diagnostic; no reference times provided to model',
    'acceptance':'all requested phonemes positive and all group intervals ordered inside clip; otherwise retain whole baseline line',
    'scoring':'all diagnostic groups retained; no per-song choice from reference scores', 'rows':records})
raw=run_worker(folder,clips,log=lambda s:print(s,flush=True))
dump(OUT/'hybrid-tifa-raw.json',raw)
