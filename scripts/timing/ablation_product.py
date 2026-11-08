"""Unmodified Studio projection and current NextFire completion, separator swap only."""
from ablation_common import *
product_imports()
import argparse,time
from dataclasses import asdict
import soundfile as sf
import torch
from lazulite.models.audio import AudioBuffer,VocalSegment,VocalAnalysis
from lazulite.audio.preparation import prepare_existing_vocals
from lazulite.models.japanese import JapaneseAlignmentRequest
from lazulite.alignment.japanese.backend import NextFireBackend,NextFireConfig
from lazulite.alignment.japanese.run import align_japanese,JapaneseConfig
from server.alignment_projection import project_alignment

p=argparse.ArgumentParser();p.add_argument('--separators',nargs='+',default=['bs','kim']);args=p.parse_args()
torch.set_num_threads(8)
backend=NextFireBackend(NextFireConfig(ROOT/'.models/nextfire','cuda'))
targets=read(OUT/'targets.json')
for sep in args.separators:
    for song in targets:
        sid=song['id'];target=OUT/'product'/sep/(sid+'.json')
        if present(target):continue
        start=time.monotonic()
        info=read(OUT/'audio'/sep/(sid+'.json'))
        wave,rate=sf.read(stem_path(song,sep),dtype='float32',always_2d=True)
        raw=info['analysis'];segments=tuple(VocalSegment(**s) for s in raw['segments'])
        analysis=VocalAnalysis(**{**raw,'segments':segments,'diagnostics':tuple(raw['diagnostics'])})
        vocals=AudioBuffer(wave.T.copy(),rate,analysis.source_id)
        prepared=prepare_existing_vocals(vocals,original_duration=info['duration'],analysis=analysis)
        projection=project_alignment(read(OLD_CACHE/'inputs'/(sid+'-studio.json')),False)
        result=align_japanese(prepared,JapaneseAlignmentRequest.from_dict(projection['request']),backend=backend,config=JapaneseConfig(hint_mode='off'))
        dump(target,{'song':sid,'separator':sep,'projection':projection,'result':asdict(result),'seconds':time.monotonic()-start})
        print('PRODUCT',sep,sid,result.status,round(time.monotonic()-start,2),flush=True)
backend.close()
