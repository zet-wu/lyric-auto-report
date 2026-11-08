"""Five English lines / 22 reference words, conditional vocal-window diagnostic."""
from common import *
timing_imports();product_imports()
import math,numpy as np,soundfile as sf,torch
from timing.tifa import run_worker
from lazulite.models.audio import AudioBuffer
from lazulite.audio.io import resample_audio
from lazulite.alignment.japanese.backend import NextFireBackend,NextFireConfig
from lazulite.alignment.japanese.run import _profile,_intervals
from lazulite.alignment.japanese.ctc import decode
from lazulite.models.japanese import JapaneseAlignmentRequest,JapaneseLine,JapaneseUnit
torch.set_num_threads(8)
backend=NextFireBackend(NextFireConfig(ROOT/'.models/nextfire','cuda'))
folder=CACHE/'english';folder.mkdir(exist_ok=True)
song=next(s for s in read(OUT/'reference.json') if s['id']=='s02')
wave,rate=sf.read(CACHE/'audio'/f'{Path(song["audio"]).stem}.wav',dtype='float32',always_2d=True);wave=wave.mean(axis=1)
clips=[];records=[]
for line in song['lines']:
    if not line['text'].isascii():continue
    name=f'{line["index"]:03}';left=math.floor(line['vocal_start']/.02)*.02;right=math.ceil(line['vocal_end']/.02)*.02
    audio=folder/f'{name}.wav';cut=wave[round(left*rate):round(right*rate)]
    sf.write(audio,cut,rate,subtype='FLOAT');audio.with_suffix('.txt').write_text(line['text'])
    clips.append({'id':name,'audio':str(audio),'languages':['en']})
    units=tuple(JapaneseUnit(u['id'],(0,len(line['text'])),u['text'].strip(),'en','body') for u in line['leaves'])
    request=JapaneseAlignmentRequest((JapaneseLine(name,line['text'],units),))
    texts,tokens,ranges,problems=_profile(request,backend.vocab,backend.blank,backend.special_tokens)
    probs=backend.emissions(resample_audio(AudioBuffer(cut[None,:],rate,name),sample_rate=16000,channels=1))
    spans,score=decode(probs,tokens,blank=backend.blank)
    intervals,sources=_intervals(request,spans,ranges,backend.frames)
    records.append({'id':name,'offset':left,'reference':line['leaves'],
                    'nextfire':[None if intervals[u.unit_id] is None else [v+left for v in intervals[u.unit_id]] for u in units]})
backend.close();torch.cuda.empty_cache()
dump(OUT/'english-input-audit.json',records)
dump(OUT/'english-tifa-raw.json',run_worker(folder,clips,log=print))
