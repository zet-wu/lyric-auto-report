"""Verify accelerated CTC against upstream using random and real acoustic slices."""
from common import *
import numpy as np
from fast_ctc import original,align
from kara_align.align.ctc import NoFeasiblePath, FramePriors, AnchorSpec
from dataclasses import asdict
rng=np.random.default_rng(17)
checks=[]
def check(lp,targets,blank,tail,label,condition=False):
    kwargs=dict(tail_penalty=tail)
    if condition:
        mask=np.zeros(2*len(targets)+1,bool);mask[2:-1:2]=True
        kwargs.update(priors=FramePriors(-np.linspace(0,2,len(lp)),-np.linspace(2,0,len(lp)),mask),anchors=[AnchorSpec(1,frame=len(lp)/3,sigma_frames=6,lam=1)])
    a=original(lp,targets,blank,**kwargs)
    b=align(lp,targets,blank,**kwargs)
    da,db=asdict(a),asdict(b)
    assert np.array_equal(da.pop('states'),db.pop('states')),label
    assert da==db,label
    checks.append({'case':label,'frames':len(lp),'tokens':len(targets),'identical':True})
for index in range(12):
    lp=rng.normal(size=(40,6));lp=lp-np.log(np.exp(lp).sum(axis=1,keepdims=True))
    targets=rng.integers(1,6,size=8).tolist()
    for tail in (None,0.,1.):
        check(lp,targets,0,tail,f'random-{index}-{tail}')
        check(lp,targets,0,tail,f'priors-anchors-{index}-{tail}',True)
for song,_,cache in inputs():
    em=np.load(cache/f"{song['id']}-global-emissions.npy")
    for offset in (0,len(em)//2):
        for tail in (None,0.):
            check(em[offset:offset+80],[1,2,2,3,4],29,tail,f"{song['id']}-{offset}-{tail}")
dump(OUT/'validation-real.json',checks)
print('Identical upstream paths:',len(checks))
