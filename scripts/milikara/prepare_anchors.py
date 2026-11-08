"""Explicit conditional experiment only: supply line-start hints, never word times."""
from common import *
import numpy as np
rng=np.random.default_rng(17);hints={}
for ev,cache in SOURCES:
    for song in read(ev/'references.json'):
        starts=[round(l['start']*1000) for l in song['lines']]
        noise=rng.integers(-1000,1001,len(starts)).tolist()
        hints[song['id']]={
            'oracle_start':starts,
            'oracle_minus500':[max(0,t-500) for t in starts],
            'oracle_plus500':[t+500 for t in starts],
            'oracle_jitter1000':[max(0,t+n) for t,n in zip(starts,noise)]}
dump(OUT/'conditional-line-hints.json',{'description':'reference line starts only; conditional diagnostic, NOT automatic input','seed':17,'songs':hints})
