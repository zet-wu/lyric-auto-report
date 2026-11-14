from common import *
import argparse,time,traceback,torch,copy
from dataclasses import asdict
sys.path.insert(0,str(ROOT/'.deps/comparison/timing'))
os.environ['PYTHONPATH']=str(ROOT/'.deps/comparison/timing')
from timing import pipeline,llm_direct,text_localization
from timing.schema import Line,Unit
from timing.audio import decode
from timing.ctc import CtcAligner
from timing.singing import english_parts
from timing.reporting import finish
import jaconv
p=argparse.ArgumentParser();p.add_argument('--condition',default='auto');p.add_argument('--song');a=p.parse_args()
assert torch.cuda.is_available();torch.set_num_threads(8)
for s in songs():
 sid=s['id']
 if a.song and sid!=a.song:continue
 target=OUT/'timing'/f'{sid}-bs-{a.condition}.json'
 if exists(target) and read(target)['status']=='ok':continue
 stem=CACHE/'stems/bs'/f'{sid}.wav';r={'song':sid,'separator':'bs','condition':a.condition,'status':'error','stem_sha256':sha(stem)};start=time.monotonic();work=CACHE/'timing'/f'{sid}-{a.condition}';work.mkdir(parents=True,exist_ok=True)
 try:
  src=read(OUT/'milikara/inputs'/('manual' if a.condition=='manual' else 'text')/f'{sid}.json')
  text='\n'.join(l['text'] for l in src['lines']);r['input']=text
  if a.condition=='auto':pipeline.run(stem,text,work,language='mixed',audio_mode='source',aligner='tifa',trust_line_timestamps=False)
  else:
   lines=[Line(l['text'],language='mixed') for l in src['lines']];records=[]
   from timing_manual import parts_for_line
   records=[{'status':'accepted','parts':parts_for_line(l)} for l in src['lines']]
   r['explicit_parts']=records
   audio,rate=decode(stem,work/'coarse.wav');engine=CtcAligner(print)
   try:
    probs,info=engine.emissions(audio,sample_rate=rate)
    located,coarse=text_localization.align_transcript(lines,probs,engine.vocab,engine.model.config.pad_token_id,info['frame_ms']/1000,len(audio)/rate,prepared=[llm_direct.coarse_units(x['parts']) for x in records])
   finally:engine.release()
   # Same whole-song MMS evidence; native explicit-reading PFML fine alignment.
   r['localization']=coarse
   audio,rate=decode(stem,work/'singing.wav',rate=44100,floating=True)
   fine=llm_direct.align(audio,rate,located,work,records,print,coarse=coarse,trust_line_timestamps=False)
   report={'source':'provided BS Karaoke vocals','aligner':'tifa','input_timing':'automatically_localized_text','explicit_manual_readings':True,'tifa':fine}
   finish(located,len(audio)/rate,'mixed',s['name'],work,report,print)
  r.update(result=read(work/'alignment.json'),status='ok')
 except Exception:r['error']=traceback.format_exc();print(r['error'],flush=True)
 r['seconds']=time.monotonic()-start;dump(target,r);torch.cuda.empty_cache();print('DONE',sid,a.condition,r['status'],flush=True)
