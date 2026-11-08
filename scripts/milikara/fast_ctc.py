"""Numba execution of upstream's exact float64 recurrence; upstream builds scores/spans.
Derived from MiliKara align/ctc.py (MIT, copyright its contributors).
No fastmath, no band: banded calls fall back to the untouched upstream function.
"""
import numpy as np
from numba import njit
from kara_align.align import ctc
original=ctc.ctc_align
@njit(cache=True)
def kernel(lp,z,skip,entry_index,entry,token,gap,mask,tail):
    T=len(lp);S=len(z);bp=np.zeros((T,S),np.int8);fbp=np.zeros(T,np.int8)
    D=np.full(S,-np.inf);D[0]=lp[0,z[0]]
    D[1]=lp[0,z[1]]+token[0]+(entry[entry_index[1],0] if entry_index[1]>=0 else 0.)
    F=-np.inf
    for t in range(1,T):
        if tail>=0:
            best=F;k=0
            if D[S-1]>best:best=D[S-1];k=1
            if D[S-2]>best:best=D[S-2];k=2
            F=best+lp[t].max()-tail;fbp[t]=k
        cur=np.empty(S,np.float64)
        for s in range(S):
            cost=entry[entry_index[s],t] if entry_index[s]>=0 else 0.
            best=D[s];step=0
            if s>0 and D[s-1]+cost>best:best=D[s-1]+cost;step=1
            if s>1 and skip[s] and D[s-2]+cost>best:best=D[s-2]+cost;step=2
            # Preserve upstream operation order: emission+token+gap, then best+emission.
            e=lp[t,z[s]]
            if s%2:e+=token[t]
            if mask[s]:e+=gap[t]
            cur[s]=best+e;bp[t,s]=step
        D=cur
    end=S-1 if D[S-1]>=D[S-2] else S-2
    return bp,fbp,end,F>D[end] if tail>=0 else False,np.isfinite(D[end])
def align(logp,targets,blank,anchors=(),band=None,priors=None,tail_penalty=None):
    if band is not None:return original(logp,targets,blank,anchors,band,priors,tail_penalty)
    lp=np.asarray(logp,dtype=np.float64);targets=list(map(int,targets))
    ctc._validate(lp,targets,blank,anchors)
    z=ctc._states(targets,blank);T=len(lp);entry=ctc._entry_costs(anchors,T)
    ix=np.full(len(z),-1,np.int64);mat=np.zeros((len(entry),T))
    for k,(s,c) in enumerate(entry.items()):ix[s]=k;mat[k]=c
    pri=ctc._check_priors(priors,T,z,blank)
    token=pri[0] if pri[0] is not None else np.zeros(T)
    gap=pri[1] if pri[1] is not None else np.zeros(T)
    mask=pri[2] if pri[2] is not None else np.zeros(len(z),bool)
    bp,fbp,end,fill,ok=kernel(lp,z,ctc._allow_skip(z,blank),ix,mat,token,gap,mask,-1. if tail_penalty is None else float(tail_penalty))
    if fill:states,tail_from=ctc._tail_states(bp,fbp,len(z))
    else:
        if not ok:raise ctc.NoFeasiblePath('没有可行的 CTC 路径')
        states=ctc._backtrack(bp,end);tail_from=None
    return ctc._path_from_states(lp,z,states,entry,len(targets),pri,tail_from)
def install():
    from kara_align.align import decoding
    decoding.ctc_align=align
