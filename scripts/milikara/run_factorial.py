from common import *
from modules import *
from fast_ctc import install,original,align
import itertools,time
install()
for song,ev,cache in inputs():
    sid=song['id'];doc=document(song)
    for mode in MODES:
        y,mapping,env,activity=load_audio(song,ev,cache,mode)
        for bits in itertools.product([False,True],repeat=5):
            code=''.join(str(int(x)) for x in bits);flags=dict(zip(FACTORS,bits))
            key=f'{mode}/f{code}';dest=OUT/'predictions'/f'{sid}--{mode}--f{code}.json'
            if dest.exists():continue
            em=emission(cache,sid,mode,flags['delimiter']);t=time.perf_counter()
            units,outcome=global_decode(doc,em,activity,flags)
            dump(dest,{'song':sid,'experiment':key,'kind':'confirmed-targets','flags':flags,'predictions':predictions(doc,units,mapping),'seconds':time.perf_counter()-t,'feasible':outcome.feasible})
            if code in ['00000','00001','11111']:
                for tail in ['trim','energy']:
                    uts=[u.model_copy(deep=True) for u in units]
                    issues=apply_tail(uts,TailConfig(strategy=tail),env)
                    dump(OUT/'predictions'/f'{sid}--{mode}--f{code}-tail_{tail}.json',{'song':sid,'experiment':f'{key}-tail_{tail}','kind':'confirmed-targets','predictions':predictions(doc,uts,mapping),'tail_adjusted':sum(u.tail is not None for u in uts),'issues':[i.model_dump() for i in issues]})
        print(sid,mode,'32 factorial + 6 tail complete',flush=True)
