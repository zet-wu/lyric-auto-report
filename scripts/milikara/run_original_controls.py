from common import *
from modules import *
from fast_ctc import install
install()
for song,ev,cache in inputs():
    sid=song['id'];doc=document(song)
    for mode in MODES:
        y,mapping,env,activity=load_audio(song,ev,cache,mode)
        em=Emission(np.load(CACHE/f'{sid}-{mode}-original.npy'),FrameMap(16000,320,0,0),29)
        for code in ['00000','00001']:
            flags=dict(zip(FACTORS,[c=='1' for c in code]));us,out=global_decode(doc,em,activity,flags)
            name=f'original-control-f{code}'
            dump(OUT/'predictions'/f'{sid}--{mode}--{name}.json',{'song':sid,'experiment':f'{mode}/{name}','kind':'confirmed-targets','predictions':predictions(doc,us,mapping),'note':'original mixture logits; frozen vocal activity available but all activity costs off'})
