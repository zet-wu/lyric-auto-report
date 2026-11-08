"""Reference-free CTC->acoustic/DP->local CTC research. No gold files imported."""
from pathlib import Path
import sys,json,time,dataclasses,hashlib,argparse
import numpy as np
from functools import lru_cache
from common import *
BASE=OUT
product_imports()

from ctc_benchmark import align,MODEL
from lazulite.models.audio import VocalAnalysis,VocalSegment
from lazulite.models.lyrics import LyricDocument,LyricLine
from lazulite.models.transcription import BackendInfo,TranscriptionResult,TranscriptionSegment,TimedText
from lazulite.alignment.line import align_lines
import lazulite.alignment.line as dp_module
from lazulite.models.audio import VocalSegment as _VocalSegment
# Pure-function memoization; values and DP decisions are unchanged.
dp_module.text_similarity=lru_cache(maxsize=250000)(dp_module.text_similarity)
import lazulite.transcription.evidence as evidence_module
evidence_module.quality=lru_cache(maxsize=10000)(evidence_module.quality)
p=argparse.ArgumentParser();p.add_argument('--gpu',action='store_true');p.add_argument('--mode',default='all');p.add_argument('--resume',action='store_true');a=p.parse_args()
protocol=json.loads((ROOT/'configs/iteration.json').read_text());(OUT/'protocol.json').write_text(json.dumps(protocol,ensure_ascii=False,indent=2)+'\n')
songs=json.loads((OUT/'auto-readings.json').read_text());vocab=json.loads((MODEL/'vocab.json').read_text());inv={v:k for k,v in vocab.items()}
backend=BackendInfo('nextfire-research','NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn','2ab2b5f46539ee284703c281f286b01d2410ee12','float32')
if a.gpu:
 import torch
 from transformers import Wav2Vec2ForCTC,Wav2Vec2FeatureExtractor
 torch.set_num_threads(8);assert torch.cuda.is_available()
 model=Wav2Vec2ForCTC.from_pretrained(MODEL,local_files_only=True).to('cuda').eval();feature=Wav2Vec2FeatureExtractor(**json.loads((MODEL/'processor_config.json').read_text())['feature_extractor'])

def save(name,v): (OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def bounds(ps):return [ps[0]['start'],ps[-1]['end']]
def cov(ps,segments):
 total=inside=0.
 # Cores partition into disjoint segments (verified below).
 for u in ps:
  dur=u['end']-u['start'];total+=dur
  inside+=sum(max(0,min(u['end'],s.core_end)-max(u['start'],s.core_start)) for s in segments)
 return min(1,inside/max(total,1e-8))
def diagnostic(ps,segments):return {'coverage':cov(ps,segments),'confidence':float(np.mean([u['score'] for u in ps])),'longest':max(u['end']-u['start'] for u in ps)}
def ctc(em,lo,hi,us):
 start=max(0,int(np.floor(lo/.02)));end=min(len(em),int(np.ceil(hi/.02)))
 return align(em[start:end],start*.02,us,vocab,29) if end>start else None

def evidence(preds,em,analysis,independent=False):
 buckets={s.id:[] for s in analysis.segments}
 if independent:
  ids=em.argmax(-1)
  for s in analysis.segments:
   lo=max(0,int(np.floor(s.core_start/.02)));hi=min(len(ids),int(np.ceil(s.core_end/.02)));t=lo
   while t<hi:
    token=int(ids[t]);end=t+1
    while end<hi and ids[end]==token:end+=1
    if 1<=token<=26 or inv.get(token)=="'":
     buckets[s.id].append({'text':inv[token],'start':t*.02,'end':end*.02,'score':float(np.exp(em[t:end,token]).mean())})
    t=end
 else:
  for u in [u for row in preds for u in row]:
   s=max(analysis.segments,key=lambda s:max(0,min(u['end'],s.core_end)-max(u['start'],s.core_start)))
   if min(u['end'],s.core_end)>max(u['start'],s.core_start):buckets[s.id].append(u)
 result=[]
 for s in analysis.segments:
  us=buckets[s.id]
  if not us:continue
  result.append(TranscriptionSegment(s.id,''.join(u['text'] for u in us),'ja',us[0]['start'],us[-1]['end'],None,None,tuple(TimedText(u['text'],u['start'],u['end'],'character','alignment') for u in us),{'pseudo':not independent}))
 return TranscriptionResult(backend,tuple(result))

def makegroups(dp,segments):
 byid={s.id:s for s in segments};groups=[];i=0
 while i<len(dp.lines):
  row=dp.lines[i];ids=set(row.source_segment_ids)
  if not ids:groups.append({'indices':[i],'reason':'unresolved_dp'});i+=1;continue
  indices=[i];j=i+1
  while j<len(dp.lines) and len(indices)<4 and ids.intersection(dp.lines[j].source_segment_ids):
   indices.append(j);ids.update(dp.lines[j].source_segment_ids);j+=1
  ss=[byid[k] for k in ids];groups.append({'indices':indices,'source_ids':sorted(ids),'window':[max(0,min(s.start for s in ss)-.10),max(s.end for s in ss)+.10]});i=j
 return groups

result_file='gpu-results.json' if a.gpu else 'cached-results.json'
records=json.loads((OUT/result_file).read_text())['records'] if a.resume and (OUT/result_file).exists() else []
for song in songs:
 sid=song['id'];t=time.perf_counter();em=np.load(CACHE/f'{sid}-global-emissions.npy');audio=np.load(CACHE/f'{sid}-vocals.npy')[0]
 av=json.loads((BASE/f'{sid}-analysis.json').read_text());av['segments']=tuple(VocalSegment(**s) for s in av['segments']);analysis=VocalAnalysis(**av)
 assert all(x.core_end<=y.core_start+1e-6 for x,y in zip(analysis.segments,analysis.segments[1:]))
 target=[[{'text':u['text']} for u in l['units'] if u['text']] for l in song['lines']];assert all(target)
 doc=LyricDocument(tuple(LyricLine(l['id'],''.join(u['text'] for u in us)) for l,us in zip(song['lines'],target)),'ja')
 assert all(l.source_start is None and l.source_end is None for l in doc.lines)
 allpred=align(em,0,sum(target,[]),vocab,29);assert allpred is not None
 initial=[];offset=0
 for us in target:initial.append(allpred[offset:offset+len(us)]);offset+=len(us)
 modes=['pseudo_dp_fresh','greedy_dp_fresh'] if a.gpu else ['global','self_window','pseudo_dp_cached']
 for mode in modes:
  if a.mode!='all' and mode!=a.mode:continue
  previous=[r for r in records if r['song']==sid and r['mode']==mode]
  if previous:
   final=previous[-1]
   if final.get('max_change',0)<.02-1e-6 or final['round']>=protocol['rounds']:continue
  preds=previous[-1]['predictions'] if previous else initial
  if mode=='global':records.append({'song':sid,'mode':mode,'round':0,'predictions':preds});continue
  if mode=='self_window':
   nxt=[ctc(em,max(0,ps[0]['start']-.3),min(len(audio)/16000,ps[-1]['end']+.3),us) for us,ps in zip(target,preds)];assert all(nxt)
   records.append({'song':sid,'mode':mode,'round':1,'predictions':nxt});continue
  independent_dp=None
  for iteration in range(previous[-1]['round']+1 if previous else 1,protocol['rounds']+1):
   dpstart=time.perf_counter()
   if mode.startswith('greedy') and independent_dp is not None:
    dp=independent_dp
   else:
    tr=evidence(preds,em,analysis,mode.startswith('greedy'));dp=align_lines(doc,tr,analysis)
    if mode.startswith('greedy'):independent_dp=dp
   dpsec=time.perf_counter()-dpstart
   groups=makegroups(dp,analysis.segments);new=[row.copy() for row in preds];decisions=[];raw=[row.copy() for row in preds]
   for group in groups:
    ix=group['indices'];old=sum([preds[i] for i in ix],[]);us=sum([target[i] for i in ix],[])
    if 'window' not in group:decisions.append({**group,'accepted':False});continue
    lo,hi=group['window'];hi=min(hi,len(audio)/16000);start=max(0,int(np.floor(lo/.02)));end=min(len(audio)//320,int(np.ceil(hi/.02)))
    if hi-lo>35:decisions.append({**group,'accepted':False,'reason':'group_too_long'});continue
    if a.gpu:
     clip=audio[start*320:end*320];inp=feature(clip,sampling_rate=16000,return_tensors='pt')['input_values'].to('cuda')
     with torch.inference_mode():local=model(inp).logits[0].log_softmax(-1).cpu().numpy()
     candidate=align(local,start*.02,us,vocab,29)
    else:candidate=ctc(em,lo,hi,us)
    if candidate is None:decisions.append({**group,'accepted':False,'reason':'infeasible_ctc'});continue
    oldq=diagnostic(old,analysis.segments);q=diagnostic(candidate,analysis.segments)
    shift=max(abs(u[k]-v[k]) for u,v in zip(old,candidate) for k in ['start','end'])
    dur=[u['end']-u['start'] for u in candidate]
    guard=all(0<d<=2 for d in dur[:-1]) and 0<dur[-1]<=3 and q['coverage']>=.70 and q['confidence']>=oldq['confidence']-.05 and (shift<=2 or oldq['longest']>3 or oldq['coverage']<.70)
    improves=q['coverage']>=oldq['coverage']+.03 or q['longest']<=oldq['longest']-.20 or q['confidence']>=oldq['confidence']+.01
    accepted=bool(guard and improves);pos=0
    for i in ix:
     count=len(target[i]);raw[i]=candidate[pos:pos+count]
     if accepted:new[i]=candidate[pos:pos+count]
     pos+=count
    decisions.append({**group,'accepted':accepted,'guard':bool(guard),'improves':bool(improves),'previous':oldq,'candidate':q,'max_shift':shift})
   delta=max(abs(u[k]-v[k]) for old,newrow in zip(preds,new) for u,v in zip(old,newrow) for k in ['start','end'])
   records.append({'song':sid,'mode':mode,'round':iteration,'predictions':new,'unguarded_predictions':raw,'dp_seconds':dpsec,'dp':dataclasses.asdict(dp),'decisions':decisions,'max_change':delta})
   print(sid,mode,iteration,'accepted',sum(d['accepted'] for d in decisions),'delta',delta,flush=True)
   preds=new
   if delta<.02-1e-6:break
  save('gpu-results.json' if a.gpu else 'cached-results.json',{'protocol':protocol,'records':records})
 print(sid,'done seconds',time.perf_counter()-t,flush=True)
save('gpu-results.json' if a.gpu else 'cached-results.json',{'protocol':protocol,'records':records})
