"""Supplemental no-DP ablation; one pass, same acceptance rule as DP-fresh."""
from pathlib import Path
import json,time,numpy as np,torch
from transformers import Wav2Vec2ForCTC,Wav2Vec2FeatureExtractor
from ctc_benchmark import align,MODEL
from common import *
BASE=OUT
product_imports()
(OUT/'self-fresh-protocol.json').write_text(json.dumps({'purpose':'Isolate local acoustic recomputation without DP; added after primary results, before this ablation scoring','rounds':1,'window':'initial global line bounds +/-0.3 sec; >35s kept unchanged','acceptance':'exact same gate/score thresholds as frozen main protocol','human_inputs':False},indent=2)+'\n')
autos=json.loads((OUT/'auto-readings.json').read_text());baselines=json.loads((OUT/'cached-results.json').read_text())['records'];vocab=json.loads((MODEL/'vocab.json').read_text())
torch.set_num_threads(8);assert torch.cuda.is_available();model=Wav2Vec2ForCTC.from_pretrained(MODEL,local_files_only=True).to('cuda').eval();feature=Wav2Vec2FeatureExtractor(**json.loads((MODEL/'processor_config.json').read_text())['feature_extractor'])
records=[]
for song in autos:
 sid=song['id'];old=next(r['predictions'] for r in baselines if r['song']==sid and r['mode']=='global');y=np.load(CACHE/f'{sid}-vocals.npy')[0];segments=json.loads((OUT/f'{sid}-analysis.json').read_text())['segments']
 def quality(ps):
  total=sum(u['end']-u['start'] for u in ps);inside=sum(max(0,min(u['end'],s['core_end'])-max(u['start'],s['core_start'])) for u in ps for s in segments)
  return {'coverage':min(1,inside/max(total,1e-8)),'confidence':float(np.mean([u['score'] for u in ps])),'longest':max(u['end']-u['start'] for u in ps)}
 new=[];raw=[];decisions=[]
 for i,(l,ps) in enumerate(zip(song['lines'],old)):
  lo=max(0,ps[0]['start']-.3);hi=min(len(y)/16000,ps[-1]['end']+.3);new.append(ps);raw.append(ps)
  if hi-lo>35:decisions.append({'indices':[i],'accepted':False,'reason':'group_too_long'});continue
  a=int(np.floor(lo/.02));b=min(len(y)//320,int(np.ceil(hi/.02)));clip=y[a*320:b*320]
  inp=feature(clip,sampling_rate=16000,return_tensors='pt')['input_values'].to('cuda')
  with torch.inference_mode():em=model(inp).logits[0].log_softmax(-1).cpu().numpy()
  candidate=align(em,a*.02,[{'text':u['text']} for u in l['units'] if u['text']],vocab,29);assert candidate is not None
  raw[-1]=candidate;oq=quality(ps);q=quality(candidate);shift=max(abs(u[k]-v[k]) for u,v in zip(ps,candidate) for k in ['start','end']);dur=[u['end']-u['start'] for u in candidate]
  guard=all(0<d<=2 for d in dur[:-1]) and 0<dur[-1]<=3 and q['coverage']>=.70 and q['confidence']>=oq['confidence']-.05 and (shift<=2 or oq['longest']>3 or oq['coverage']<.70)
  improves=q['coverage']>=oq['coverage']+.03 or q['longest']<=oq['longest']-.20 or q['confidence']>=oq['confidence']+.01
  accepted=bool(guard and improves)
  if accepted:new[-1]=candidate
  decisions.append({'indices':[i],'window':[a*.02,b*.02],'accepted':accepted,'guard':bool(guard),'improves':bool(improves),'previous':oq,'candidate':q,'max_shift':shift})
 records.append({'song':sid,'mode':'self_fresh','round':1,'predictions':new,'unguarded_predictions':raw,'decisions':decisions});print(sid,'accepted',sum(d['accepted'] for d in decisions),flush=True)
(OUT/'self-fresh-results.json').write_text(json.dumps({'records':records},ensure_ascii=False,indent=2)+'\n')
