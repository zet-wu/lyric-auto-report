"""Budgeted manual-reading refinement; never reads reference timestamps."""
from common import *
import math,time,numpy as np,torch
from concat import concatenate,map_unit
from ctc_benchmark import align,MODEL
product_imports()
from lazulite.alignment.japanese.backend import NextFireBackend,NextFireConfig
from lazulite.models.audio import AudioBuffer
from transformers import Wav2Vec2ForCTC,Wav2Vec2FeatureExtractor
DEST=ROOT/'results/local-refinement'
protocol=read(ROOT/'configs/local-refinement.json')
torch.set_num_threads(8);torch.manual_seed(0);assert torch.cuda.is_available()
started=time.perf_counter()
backend=NextFireBackend(NextFireConfig(MODEL,'cuda'))
model=Wav2Vec2ForCTC.from_pretrained(MODEL,local_files_only=True).to('cuda').eval()
feature=Wav2Vec2FeatureExtractor(**read(MODEL/'processor_config.json')['feature_extractor'])
vocab=read(MODEL/'vocab.json')
# Warm both forward paths and the CTC kernel outside all measurements.
backend.emissions(AudioBuffer(np.zeros((1,16000),np.float32),16000))
with torch.inference_mode():model(torch.zeros((1,16000),device='cuda'))
align(np.log(np.full((10,32),1/32,np.float32)),0,[{'text':'a'}],vocab,29)
torch.cuda.synchronize();setup_seconds=time.perf_counter()-started
runtime=[]
for song,_,cache in inputs():
 if song['id']=='s13':continue
 sid=song['id'];y=np.load(cache/f'{sid}-vocals.npy')[0]
 segments=read(OUT/f'{sid}-analysis.json')['segments']
 def quality(ps):
  valid=[p for p in ps if p and p['end']>p['start']]
  dur=sum(p['end']-p['start'] for p in valid)
  inside=sum(max(0,min(p['end'],s['core_end'])-max(p['start'],s['core_start'])) for p in valid for s in segments)
  return {'coverage':min(1,inside/max(dur,1e-8)),'confidence':float(np.mean([p['score'] for p in valid])) if valid else 0.,'longest':max((p['end']-p['start'] for p in valid),default=0.),'cross_gap':any(p and p.get('crosses_removed_gap',False) for p in ps)}
 for mode in ('global','concat_core'):
  mapping=read(OUT/f'{sid}-{mode}-map.json')['pieces'] if mode!='global' else None
  signal=concatenate(y,mapping) if mapping else y
  torch.cuda.synchronize();t=time.perf_counter();em=backend.emissions(AudioBuffer(signal[None,:],16000));torch.cuda.synchronize();forward=time.perf_counter()-t
  usable=[u for l in song['lines'] for u in l['units'] if u['text']]
  t=time.perf_counter();fresh=align(em,0,usable,vocab,29);decode_seconds=time.perf_counter()-t
  assert fresh is not None
  if mapping:fresh=[map_unit(p,mapping) for p in fresh]
  frozen=read(OUT/'predictions'/f'{sid}--{mode}--f00000.json')['predictions']
  rows=[];offset=0;max_difference=0.
  for l,ps in zip(song['lines'],frozen):
   row=[]
   for u,p in zip(l['units'],ps):
    if not u['text']:row.append(None);continue
    f=fresh[offset];offset+=1
    assert p is not None
    max_difference=max(max_difference,abs(f['start']-p['start']),abs(f['end']-p['end']))
    row.append({**p,'score':f['score']})
   rows.append(row)
  assert max_difference<=.00101,(sid,mode,max_difference)
  choices=[];decisions=[]
  for i,(l,ps) in enumerate(zip(song['lines'],rows)):
   q=quality(ps);valid=[p for p in ps if p and p['end']>p['start']];reasons=[]
   emitting=sum(bool(u['text']) for u in l['units'])
   if len(valid)!=emitting:reasons.append('invalid')
   if q['cross_gap']:reasons.append('cross_gap')
   if any(p['end']-p['start']>(3 if j==len(valid)-1 else 2) for j,p in enumerate(valid)):reasons.append('duration')
   if q['coverage']<.70:reasons.append('coverage')
   if q['confidence']<.60:reasons.append('confidence')
   d={'line':i,'line_id':l['id'],'reasons':reasons,'quality':q,'selected':False}
   decisions.append(d)
   if not reasons or not valid:continue
   a=max(0,math.floor((valid[0]['start']-.3)/.02));b=min(len(y)//320,math.ceil((valid[-1]['end']+.3)/.02))
   d['window']=[a*.02,b*.02]
   if not 0<b-a<=1750:d['skip']='window_length';continue
   rank=(not ('cross_gap' in reasons or 'invalid' in reasons),'duration' not in reasons,-q['longest'] if 'duration' in reasons else 0,q['coverage'],q['confidence'],i)
   choices.append((rank,i,a,b))
  chosen=[];used=0.;cap=.20*len(y)/16000;limit=math.ceil(.20*len(rows))
  for _,i,a,b in sorted(choices):
   cost=(b-a)*.02
   if len(chosen)>=limit or used+cost>cap:decisions[i]['skip']='budget';continue
   chosen.append((i,a,b));used+=cost;decisions[i]['selected']=True
  variants={v:[list(r) for r in rows] for v in ('cached_window','local_fresh')}
  elapsed={v:0. for v in variants};accepted={v:0 for v in variants}
  for i,a,b in chosen:
   l=song['lines'][i];ps=rows[i];us=[u for u in l['units'] if u['text']];oq=quality(ps)
   for variant in variants:
    torch.cuda.synchronize();t=time.perf_counter()
    if variant=='local_fresh':
     inp=feature(y[a*320:b*320],sampling_rate=16000,return_tensors='pt')['input_values'].to('cuda')
     with torch.inference_mode():lp=model(inp).logits[0].float().log_softmax(-1).cpu().numpy()
     candidate=align(lp,a*.02,us,vocab,29)
    else:
     if mapping:
      overlaps=[(max(a*320,p['source_start']),min(b*320,p['source_end']),p) for p in mapping if min(b*320,p['source_end'])>max(a*320,p['source_start'])]
      ca=(overlaps[0][0]-overlaps[0][2]['source_start']+overlaps[0][2]['concat_start']) if overlaps else 0
      cb=(overlaps[-1][1]-overlaps[-1][2]['source_start']+overlaps[-1][2]['concat_start']) if overlaps else 0
      fa=max(0,math.floor(ca/320));fb=min(len(em),math.ceil(cb/320))
     else:fa,fb=a,min(b,len(em))
     candidate=align(em[fa:fb],fa*.02,us,vocab,29) if fb>fa else None
     if candidate and mapping:candidate=[map_unit(p,mapping) for p in candidate]
    torch.cuda.synchronize();seconds=time.perf_counter()-t;elapsed[variant]+=seconds
    detail={'seconds':seconds,'accepted':False}
    if candidate:
     row=[];k=0
     for u in l['units']:
      if u['text']:row.append(candidate[k]);k+=1
      else:row.append(None)
     q=quality(row);shift=max(abs(p[key]-c[key]) for p,c in zip(ps,row) if p and c for key in ('start','end'))
     ds=[p['end']-p['start'] for p in candidate]
     guard=all(0<d<=2 for d in ds[:-1]) and 0<ds[-1]<=3 and not q['cross_gap'] and q['coverage']>=.70 and q['confidence']>=oq['confidence']-.05 and (shift<=2 or oq['longest']>3 or oq['coverage']<.70 or oq['cross_gap'])
     improves=q['coverage']>=oq['coverage']+.03 or q['longest']<=oq['longest']-.20 or q['confidence']>=oq['confidence']+.01 or (oq['cross_gap'] and not q['cross_gap'])
     take=bool(guard and improves)
     detail.update(accepted=take,guard=bool(guard),improves=bool(improves),quality=q,max_shift=shift,predictions=row)
     if take:variants[variant][i]=row;accepted[variant]+=1
    else:detail['failure']='no_feasible_path'
    decisions[i][variant]=detail
  for variant,preds in {'baseline':rows,**variants}.items():
   dump(DEST/'predictions'/f'{sid}--{mode}--{variant}.json',{'song':sid,'kind':'confirmed-targets','experiment':f'{mode}/{variant}','baseline':mode,'variant':variant,'predictions':preds})
  dump(DEST/'decisions'/f'{sid}--{mode}.json',{'song':sid,'baseline':mode,'decisions':decisions})
  record={'song':sid,'baseline':mode,'audio_seconds':len(y)/16000,'first_pass_audio_seconds':len(signal)/16000,'first_forward_seconds':forward,'first_decode_seconds':decode_seconds,'selected_lines':len(chosen),'total_lines':len(rows),'selected_audio_seconds':used,'additional_seconds':elapsed,'accepted_lines':accepted,'baseline_max_endpoint_difference_seconds':max_difference}
  runtime.append(record);dump(DEST/'runtime.json',{'model_setup_and_warmup_seconds':setup_seconds,'gpu':torch.cuda.get_device_name(),'torch':torch.__version__,'records':runtime})
  print(sid,mode,len(chosen),accepted,'seconds',elapsed,flush=True)
backend.close()
