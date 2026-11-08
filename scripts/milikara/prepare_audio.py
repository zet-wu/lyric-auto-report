from common import *
product_imports()
import numpy as np, soundfile as sf, torch
from lazulite.models.audio import AudioBuffer
from lazulite.audio.io import resample_audio
from lazulite.alignment.japanese.backend import NextFireBackend,NextFireConfig
from concat import make_map,concatenate
torch.set_num_threads(8)
backend=NextFireBackend(NextFireConfig(ROOT/'.models/nextfire','cuda'))
refs={s['id']:s for s in read(ROOT/'results/timing/reference.json')}
for song,ev,cache in inputs():
    sid=song['id'];ref=refs[sid]
    wave,rate=sf.read(ROOT/'.cache/timing/audio'/(Path(ref['audio']).stem+'.wav'),dtype='float32',always_2d=True)
    audio=resample_audio(AudioBuffer(wave.T.copy(),rate),sample_rate=16000,channels=1)
    y=audio.samples[0];np.save(CACHE/(sid+'-vocals.npy'),y[None,:])
    baseline=read(ROOT/'results/timing/baseline'/(sid+'.json'))
    segments=baseline['analysis']['segments']
    dump(OUT/(sid+'-analysis.json'),baseline['analysis'])
    for mode in MODES:
        mapping=None if mode=='global' else make_map(segments,len(y),mode=='concat_padded')
        if mapping:dump(OUT/(sid+'-'+mode+'-map.json'),{'pieces':mapping})
        signal=y if mapping is None else concatenate(y,mapping)
        path=CACHE/(sid+'-'+mode+'-emissions.npy')
        if not path.exists():np.save(path,backend.emissions(AudioBuffer(signal[None,:].copy(),16000)))
    print('ACOUSTICS',sid,flush=True)
backend.close()
