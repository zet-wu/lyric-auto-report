from common import *
product_imports()
import numpy as np, soundfile as sf, torch, time, traceback
from dataclasses import asdict
from lazulite.audio.io import decode_audio
from lazulite.audio.preparation import prepare_existing_vocals
from lazulite.audio.separation import DemucsSeparator, DemucsConfig
from lazulite.models.audio import AudioBuffer
from lazulite.models.japanese import JapaneseAlignmentRequest
from lazulite.alignment.japanese.backend import NextFireBackend, NextFireConfig
from lazulite.alignment.japanese.run import align_japanese, JapaneseConfig
from server.alignment_projection import project_alignment

torch.set_num_threads(8)
assert torch.cuda.is_available()
backend=NextFireBackend(NextFireConfig(ROOT/'.models/nextfire','cuda'))
sep=DemucsSeparator(DemucsConfig())
for song in read(OUT/'reference.json'):
    sid=song['id']; target=OUT/'baseline'/f'{sid}.json'
    if exists(target): continue
    started=time.monotonic()
    try:
        original=decode_audio(ROOT/song['audio'],sample_rate=44100,channels=2)
        shared=CACHE/'audio'/f'{Path(song["audio"]).stem}.wav'; shared.parent.mkdir(exist_ok=True)
        if shared.exists():
            samples,rate=sf.read(shared,dtype='float32',always_2d=True); vocals=AudioBuffer(samples.T.copy(),rate,original.source_id); origin='this evaluation cache'
        else:
            vocals=sep.separate(original); origin='fresh current DemucsSeparator default seed=0'
            sf.write(shared,vocals.samples.T,vocals.sample_rate,subtype='FLOAT')
        prepared=prepare_existing_vocals(vocals,reference=original,original_duration=original.duration)
        projection=project_alignment(read(CACHE/'inputs'/f'{sid}-studio.json'),False)
        result=align_japanese(prepared,JapaneseAlignmentRequest.from_dict(projection['request']),backend=backend,config=JapaneseConfig(hint_mode='off'))
        dump(target,{'song':sid,'seconds':time.monotonic()-started,'stem_origin':origin,'stem':str(shared),
                     'analysis':asdict(prepared.analysis),'projection':projection,'result':asdict(result)})
        print(sid,song['name'],result.status,round(time.monotonic()-started,2),flush=True)
    except Exception:
        dump(OUT/'baseline'/f'{sid}-error.json',{'error':traceback.format_exc()}); print(traceback.format_exc(),flush=True)
backend.close(); sep.close()
