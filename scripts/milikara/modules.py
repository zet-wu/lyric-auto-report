"""Composable adapters: emissions, positional targets, priors, decoder, tail, timeline.
All accuracy reference access is isolated to evaluate.py / explicit anchor preparation.
"""
from common import *
import numpy as np
from concat import concatenate,map_unit
from kara_align.models import Line,LyricsDoc,Segment,Unit,DecodeConfig,TailConfig
from kara_align.interfaces import Emission
from kara_align.timebase import FrameMap
from kara_align.align.decoding import prepare,decode_task,unit_timings_for_line
from kara_align.align.planning import Task
from kara_align.align.activity import detect_activity
from kara_align.align.tail import apply_tail
from kara_align.align.backends.wav2vec2_ctc import tokenize_chars
from kara_align.audio.analysis import rms_envelope_db
VOCAB=read(ROOT/'.models/nextfire/vocab.json')
class IdentityProfile:
    name='frozen-romanization'
    def unit_texts(self,readings,langs,flags):return list(readings)
PROFILE=IdentityProfile()
def tokenize(ids,texts):return tokenize_chars(ids,texts,VOCAB,{'[UNK]','[PAD]','[BOS]','[EOS]'})
def document(song):
    return LyricsDoc(lines=[Line(id=l['id'],text=l['text'],segments=[Segment(id=f's{i}',surface='基準',units=[Unit(id=f'u{i}_{j}',reading=u['text']) for j,u in enumerate(l['units'])])]) for i,l in enumerate(song['lines'])])
def load_audio(song,evidence,cache,mode):
    sid=song['id'];y=np.load(cache/f'{sid}-vocals.npy')[0]
    mapping=None if mode=='global' else read(evidence/f'{sid}-{mode}-map.json')['pieces']
    if mapping:y=concatenate(y,mapping)
    env=rms_envelope_db(y,16000)
    return y,mapping,(env,10.),detect_activity(env,10.)
def emission(cache,sid,mode,delimiter,context=2):
    path=cache/f'{sid}-{mode}-emissions.npy' if context==2 else CACHE/f'{sid}-{mode}-context{context}.npy'
    lp=np.load(path)
    if delimiter:
        lp[:,29]=np.logaddexp(lp[:,29],lp[:,0]);lp[:,0]=-1e4
    return Emission(lp,FrameMap(16000,320,0,0),29)
def decode_config(flags):
    return DecodeConfig(line_gap_cost=1. if flags['line_gap'] else 0.,rest_gap_cost=4. if flags['rest_gap'] else 0.,rest_token_cost=25. if flags['rest_token'] else 0.)
def global_decode(doc,em,activity,flags):
    prep=prepare(doc,PROFILE,tokenize)
    order=prep.order
    task=Task('global','main',order,order,0,em.num_frames,free_tail=flags['free_tail'])
    outcome=decode_task(task,em,prep,decode_config(flags),'vocals',activity=activity)
    return [u for lid in order for u in unit_timings_for_line(prep,outcome,lid)],outcome

def predictions(doc,units,mapping):
    by_id={u.unit_id:u for u in units};result=[]
    for line in doc.lines:
        row=[]
        for unit in line.units():
            u=by_id[unit.id]
            p={'text':unit.reading,'start':u.start_ms/1000.,'end':u.end_ms/1000.,'flags':u.flags} if u.start_ms is not None and u.end_ms is not None else None
            if p and mapping and p['end']>p['start']:p=map_unit(p,mapping)
            row.append(p)
        result.append(row)
    return result
