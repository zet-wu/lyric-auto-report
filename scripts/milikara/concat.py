"""Sample-exact, discontinuity-aware concatenation mapping; no reference inputs."""
import math
import numpy as np

RATE = 16000

def make_map(segments, length, padded=False):
    intervals=[]
    for s in segments:
        a=max(0, math.floor(s['start' if padded else 'core_start']*RATE))
        b=min(length, math.ceil(s['end' if padded else 'core_end']*RATE))
        if b>a: intervals.append((a,b))
    merged=[]
    for a,b in sorted(intervals):
        if merged and a<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],b)
        else: merged.append([a,b])
    offset=0; result=[]
    for a,b in merged:
        result.append({'source_start':a,'source_end':b,'concat_start':offset,'concat_end':offset+b-a})
        offset+=b-a
    assert result
    return result

def concatenate(y, mapping):
    result=np.concatenate([y[p['source_start']:p['source_end']] for p in mapping])
    assert len(result)==mapping[-1]['concat_end']
    return result

def map_unit(unit, mapping):
    a=unit['start']*RATE; b=unit['end']*RATE
    assert 0<=a<b<=mapping[-1]['concat_end']+1e-5
    fragments=[]
    for p in mapping:
        lo=max(a,p['concat_start']);hi=min(b,p['concat_end'])
        # Strict interval intersection gives right-side start / left-side end
        # at exact seams, without mapping the end into the next retained piece.
        if hi>lo+1e-6:
            fragments.append({'start':(p['source_start']+lo-p['concat_start'])/RATE,
                              'end':(p['source_start']+hi-p['concat_start'])/RATE})
    assert fragments
    return {**unit,'concat_start':unit['start'],'concat_end':unit['end'],
            'start':fragments[0]['start'],'end':fragments[-1]['end'],
            'fragments':fragments,'crosses_removed_gap':len(fragments)>1,
            'removed_gap_seconds':sum(y['start']-x['end'] for x,y in zip(fragments,fragments[1:]))}

def validate():
    m=make_map([{'core_start':1,'core_end':2},{'core_start':4,'core_end':5}],RATE*6)
    assert np.array_equal(concatenate(np.arange(RATE*6),m),np.r_[np.arange(RATE,RATE*2),np.arange(RATE*4,RATE*5)])
    assert map_unit({'start':0,'end':1},m)['end']==2
    assert map_unit({'start':1,'end':2},m)['start']==4
    p=map_unit({'start':.9,'end':1.1},m)
    assert abs(p['start']-1.9)<1e-10 and abs(p['end']-4.1)<1e-10 and p['crosses_removed_gap']
    assert len(make_map([{'start':1,'end':3},{'start':2,'end':4}],RATE*5,True))==1
    rng=np.random.default_rng(7)
    for _ in range(200):
        a,b=np.sort(rng.uniform(0,2,2));p=map_unit({'start':float(a),'end':float(b)},m)
        assert abs(sum(f['end']-f['start'] for f in p['fragments'])-(b-a))<1e-10
    return {'sample_concatenation':True,'seam_sidedness':True,'overlap_union':True,'random_duration_conservation_cases':200}
