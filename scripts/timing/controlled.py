"""Fixed human readings + human vocal windows: backend diagnostic, NOT end-to-end."""
from common import *
timing_imports(); product_imports()
import math, re, time, traceback, unicodedata
import numpy as np, soundfile as sf, torch
from timing.llm_direct import compile_parts
from timing.tifa import run_worker
from lazulite.models.audio import AudioBuffer
from lazulite.audio.io import resample_audio
from lazulite.alignment.japanese.backend import NextFireBackend, NextFireConfig
from lazulite.alignment.japanese.run import _profile, _intervals
from lazulite.alignment.japanese.ctc import decode
from lazulite.models.japanese import JapaneseAlignmentRequest, JapaneseLine, JapaneseUnit

torch.set_num_threads(8)
assert torch.cuda.is_available()
backend=NextFireBackend(NextFireConfig(ROOT/'.models/nextfire','cuda'))
folder=CACHE/'controlled'; folder.mkdir(exist_ok=True)
clips=[]; records=[]; exclusions=[]
for song in read(OUT/'reference.json'):
    source=CACHE/'audio'/f'{Path(song["audio"]).stem}.wav'
    if not source.exists(): continue
    wave,rate=sf.read(source,dtype='float32',always_2d=True)
    wave=wave.mean(axis=1)
    for line in song['lines']:
        leaves=[u for u in line['leaves'] if any(c.isalnum() for c in u['text'])]
        values=[unicodedata.normalize('NFKC',u['text']) for u in leaves]
        if not leaves or any(not re.fullmatch('[ぁ-ゖァ-ヺー]+',s) for s in values):
            exclusions.append({'song':song['id'],'line':line['index'],'reason':'not entirely kana reference readings','reference_units':len(leaves)})
            continue
        groups=[]
        for leaf,value in zip(leaves,values):
            kana=''.join(chr(ord(c)+96) if 'ぁ'<=c<='ゖ' else c for c in value)
            if kana=='ー' and groups:
                groups[-1]['reading']+=kana; groups[-1]['text']+=kana; groups[-1]['ids'].append(leaf['id']); groups[-1]['end']=leaf['end']
            else:
                groups.append({'text':kana,'lang':'ja','reading':kana,'ids':[leaf['id']],'start':leaf['start'],'end':leaf['end']})
        try:
            text=''.join(g['text'] for g in groups)
            parts=compile_parts(text,[{k:g[k] for k in ('text','lang','reading')} for g in groups])
        except Exception as e:
            exclusions.append({'song':song['id'],'line':line['index'],'reason':str(e),'reference_units':len(leaves)}); continue
        name=f'{song["id"]}-{line["index"]:03}'
        left=max(0,math.floor(line['vocal_start']/.02)*.02); right=min(len(wave)/rate,math.ceil(line['vocal_end']/.02)*.02)
        a,b=round(left*rate),round(right*rate)
        audio=folder/f'{name}.wav'
        sf.write(audio,wave[a:b],rate,subtype='FLOAT'); audio.with_suffix('.txt').write_text(text)
        clips.append({'id':name,'audio':str(audio),'languages':['ja'],'llm_direct_parts':parts})
        units=tuple(JapaneseUnit(f'{name}-{j}',(0,len(text)),g['reading'],'ja','ruby') for j,g in enumerate(groups))
        request=JapaneseAlignmentRequest((JapaneseLine(name,text,units),))
        texts,tokens,ranges,problems=_profile(request,backend.vocab,backend.blank,backend.special_tokens)
        buffer=resample_audio(AudioBuffer(wave[a:b][None,:],rate,name),sample_rate=16000,channels=1)
        probs=backend.emissions(buffer)
        spans,score=decode(probs,tokens,blank=backend.blank)
        intervals,sources=_intervals(request,spans,ranges,backend.frames)
        pred=[None if intervals[u.unit_id] is None else [v+left for v in intervals[u.unit_id]] for u in units]
        records.append({'id':name,'song':song['id'],'line':line['index'],'language':line['language'],
                        'offset':left,'end':right,'groups':groups,'nextfire':pred,'profile_issues':problems})
    print(song['id'],'controlled prepared',len(clips),flush=True)
backend.close(); torch.cuda.empty_cache()
dump(OUT/'controlled-input-audit.json',{'rows':records,'excluded':exclusions,
     'note':'Manual kana readings and reference vocal crops. Standalone long marks merged with previous unit for BOTH models. Pure-kana lines only; no LLM called.'})
raw=run_worker(folder,clips,log=lambda s:print(s,flush=True))
dump(OUT/'controlled-tifa-raw.json',raw)
