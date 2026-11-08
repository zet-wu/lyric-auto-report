"""Exploratory explicit duplicate-vowel targets for ten originally separate ー.

Same human or automatic windows for both backends. No product changes.
"""
from ablation_common import *
product_imports()
import sys,math,time,copy
import numpy as np,soundfile as sf,torch
from lazulite.audio.io import resample_audio
from lazulite.models.audio import AudioBuffer
from lazulite.models.japanese import JapaneseAlignmentRequest,JapaneseLine,JapaneseUnit
from lazulite.alignment.japanese.backend import NextFireBackend,NextFireConfig
from lazulite.alignment.japanese.run import _profile,_intervals
from lazulite.alignment.japanese.ctc import decode

torch.set_num_threads(8)
refs={s['id']:s for s in read(PREVIOUS/'reference.json')}
cases=[]
for song in read(OUT/'targets.json'):
    if song['id'] not in PRIMARY:continue
    leaves={g['id']:g for l in refs[song['id']]['lines'] for g in l['leaves']}
    for line in song['lines']:
        if not any(len(g['ids'])>1 and g['paired'] for g in line['groups']):continue
        groups=[];pairs=[]
        for g in line['groups']:
            if len(g['ids'])==1:groups.append(copy.deepcopy(g));continue
            assert len(g['ids'])==2
            left,right=[leaves[i] for i in g['ids']]
            assert right['text']=='ー'
            phones=sum(g['phone_groups'],[]);vowel=phones[-1]
            assert vowel in ['ja/a','ja/i','ja/u','ja/e','ja/o']
            base=copy.deepcopy(g);base.update(key=g['key']+':base',ids=[left['id']],reading=g['reading'].rstrip('ー'),start=left['start'],end=left['end'])
            hold=copy.deepcopy(g);hold.update(key=g['key']+':hold',ids=[right['id']],reading='ー',phone_groups=[[vowel]],start=right['start'],end=right['end'])
            groups.extend([base,hold]);pairs.append([base['key'],hold['key']])
        for sep in ('demucs','bs','kim'):
            wave,rate=sf.read(read(OUT/'audio'/sep/(song['id']+'.json'))['files']['full'],dtype='float32')
            a=max(0,math.floor(line['human_window'][0]/.02)*.02);b=min(len(wave)/rate,math.ceil(line['human_window'][1]/.02)*.02)
            pred={u['key']:u['prediction'] for u in read(result_path(sep,'nextfire','concat',song['id']))['units']}
            p,q=pred.get(line['groups'][0]['key']),pred.get(line['groups'][-1]['key'])
            auto=[max(0,p[0]-.3),min(len(wave)/rate,q[1]+.3)] if p and q else None
            if auto and not .1<=auto[1]-auto[0]<=60:auto=None
            for strategy,bounds in [('human',[a,b]),('auto_nf',auto)]:
                i,j=(math.floor(bounds[0]*rate),math.ceil(bounds[1]*rate)) if bounds else (0,0)
                cases.append({'song':song['id'],'separator':sep,'strategy':strategy,'line':line['index'],'offset':i/rate,'wave':wave[i:j] if bounds else None,'rate':rate,'groups':groups,'pairs':pairs})
backend=NextFireBackend(NextFireConfig(ROOT/'.models/nextfire','cuda'))
for case in cases:
    if case['wave'] is None:
        case['nextfire']={g['key']:None for g in case['groups']};continue
    req=JapaneseAlignmentRequest((JapaneseLine('line',''.join(g['text'] for g in case['groups']),tuple(
        JapaneseUnit(g['key'],(0,1),g['reading'],g['lang'],'ruby') for g in case['groups'])),))
    _,tokens,ranges,issues=_profile(req,backend.vocab,backend.blank,backend.special_tokens)
    audio=resample_audio(AudioBuffer(case['wave'][None,:],case['rate']),sample_rate=16000,channels=1)
    spans,_=decode(backend.emissions(audio),tokens,blank=backend.blank)
    intervals,sources=_intervals(req,spans,ranges,backend.frames)
    case['nextfire']={k:[a+case['offset'],b+case['offset']] if v else None for k,v in intervals.items() for a,b in ([v] if v else [(0,0)])}
backend.close();torch.cuda.empty_cache()
model=UPSTREAM/'models/tifa';sys.path[:0]=[str(model/'deps'),str(model/'runtime')]
from inference.api import load_inference_model
from lib.config.schema import ConfigurationScope
backend,_,_=load_inference_model(model/'model.pt',scope=ConfigurationScope.FA);backend=backend.cuda().eval()
vocab=read(model/'vocabulary.json')['symbols']
output=[]
with torch.inference_mode():
    for case in cases:
        if case['wave'] is None:
            gs={g['key']:g for g in case['groups']}
            for left,right in case['pairs']:
                for method in ('nextfire','tifa_duplicate_vowel'):
                    output.append({'song':case['song'],'separator':case['separator'],'strategy':case['strategy'],'line':case['line'],'reading':gs[left]['reading']+'ー','method':method,
                        'reference':[gs[left]['end'],gs[right]['start']],'prediction':None,'hit100':False,'error':'automatic window unavailable'})
            continue
        tokens=[];owners=[];gids=[];gid=0
        for owner,g in enumerate(case['groups']):
            for phones in g['phone_groups']:
                gid+=1
                for ph in phones:tokens.append(vocab[ph]);owners.append(owner);gids.append(gid)
        wave=torch.from_numpy(case['wave']).cuda()[None,:]
        spec=backend.spectrogram(wave,torch.tensor([wave.shape[-1]/case['rate']],device='cuda'))
        aligned=backend.align(spec,tokens=torch.tensor([tokens],device='cuda'),groups=torch.tensor([gids],device='cuda'),unit='second',skip_penalty=.5)
        spans=aligned.spans[0].cpu().tolist();pred={}
        for owner,g in enumerate(case['groups']):
            ix=[i for i,o in enumerate(owners) if o==owner]
            pred[g['key']]=[spans[ix[0]][0]+case['offset'],spans[ix[-1]][1]+case['offset']] if all(spans[i][1]>spans[i][0] for i in ix) else None
        gs={g['key']:g for g in case['groups']}
        for left,right in case['pairs']:
            truth=[gs[left]['end'],gs[right]['start']]
            for method,values in [('nextfire',case['nextfire']),('tifa_duplicate_vowel',pred)]:
                p,q=values[left],values[right];value=[p[1],q[0]] if p and q else None
                output.append({'song':case['song'],'separator':case['separator'],'strategy':case['strategy'],'line':case['line'],'reading':gs[left]['reading']+'ー','method':method,
                    'reference':truth,'prediction':value,'hit100':bool(value and max(abs(x-y) for x,y in zip(value,truth))<=.100000001),
                    'left_unit':p,'right_unit':q,'left_reference':[gs[left]['start'],gs[left]['end']],'right_reference':[gs[right]['start'],gs[right]['end']]})
dump(OUT/'duplicate-vowel-probe.json',{'scope':'Exploratory 10 internal long-mark boundaries, 8 lines x 3 stems x human/automatic NextFire windows. Explicit repeated final vowel for TIFA; original standalone hold profile for NextFire. Not included in primary ranking.','rows':output})
for sep in ('demucs','bs','kim'):
    for strategy in ('human','auto_nf'):
        for method in ('nextfire','tifa_duplicate_vowel'):
            rows=[r for r in output if r['separator']==sep and r['method']==method and r['strategy']==strategy]
            print('HOLD',sep,strategy,method,len(rows),sum(r['hit100'] for r in rows),flush=True)
