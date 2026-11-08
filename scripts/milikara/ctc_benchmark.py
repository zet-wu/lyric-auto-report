"""NextFire GPU emissions and standard CTC Viterbi. Independent research, not Studio code.
Reads confirmed romanization, never invents kana/English pronunciation. Viterbi CPU via numba.
"""
from pathlib import Path
import sys,json,time,re,argparse
import numpy as np
from numba import njit
from common import ROOT,OUT,CACHE
MODEL=ROOT/'.models/nextfire'
@njit
def viterbi(em,y,blank):
 T=em.shape[0];S=2*len(y)+1
 z=np.full(S,blank,np.int64);z[1::2]=y
 prev=np.full(S,-np.inf,np.float64);prev[0]=em[0,blank];prev[1]=em[0,y[0]]
 back=np.zeros((T,S),np.int8)
 for t in range(1,T):
  cur=np.full(S,-np.inf,np.float64)
  for s in range(S):
   best=prev[s];step=0
   if s>0 and prev[s-1]>best:best=prev[s-1];step=1
   if s>1 and z[s]!=blank and z[s]!=z[s-2] and prev[s-2]>best:best=prev[s-2];step=2
   cur[s]=best+em[t,z[s]];back[t,s]=step
  prev=cur
 s=S-1 if prev[S-1]>prev[S-2] else S-2
 if not np.isfinite(prev[s]):return np.empty(0,np.int64)
 path=np.empty(T,np.int64)
 for t in range(T-1,-1,-1):path[t]=s;s-=back[t,s]
 return path

def units(line):
 return line['roman'] or line['units']
def tokens(us,vocab):
 ids=[];ranges=[]
 for u in us:
  raw=u['text'].lower().replace('’',"'");raw=''.join(raw.split())
  if not raw or any(c not in vocab or c=='|' for c in raw):raise ValueError('unsupported target '+repr(raw))
  a=len(ids);ids.extend(vocab[c] for c in raw);ranges.append((a,len(ids)))
 return np.array(ids,dtype=np.int64),ranges

def align(em,offset,us,vocab,blank):
 ids,ranges=tokens(us,vocab);path=viterbi(em,ids,blank)
 if not len(path):return None
 starts=[];ends=[];scores=[]
 for i in range(len(ids)):
  frames=np.flatnonzero(path==2*i+1)
  if not len(frames):raise RuntimeError('CTC omitted required token')
  starts.append(int(frames[0]));ends.append(int(frames[-1])+1);scores.append(float(np.exp(em[frames,ids[i]]).mean()))
 return [{'text':u['text'],'start':offset+starts[a]*.02,'end':offset+ends[b-1]*.02,'score':float(np.mean(scores[a:b]))} for u,(a,b) in zip(us,ranges)]
