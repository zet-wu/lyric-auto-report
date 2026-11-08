"""Robustness to the freshly generated Studio automatic readings (no new reference inputs)."""
from common import *
from modules import *
from fast_ctc import install
install()
for song,ev,cache in inputs('auto-readings'):
    sid=song['id'];doc=document(song)
    for mode in MODES:
        y,mapping,env,activity=load_audio(song,ev,cache,mode)
        for code in ['00000','00001','01111','11111']:
            flags=dict(zip(FACTORS,[c=='1' for c in code]));em=emission(cache,sid,mode,flags['delimiter'])
            units,outcome=global_decode(doc,em,activity,flags)
            dump(OUT/'predictions'/f'{sid}--{mode}--auto-f{code}.json',{'song':sid,'experiment':f'{mode}/auto-f{code}','kind':'auto-readings','predictions':predictions(doc,units,mapping),'empty_targets':[u.id for l in doc.lines for u in l.units() if not u.reading]})
        print(sid,mode,'auto complete',flush=True)
