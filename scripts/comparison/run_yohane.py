from common import *
import time,traceback,types,torch,soundfile as sf,argparse
p=argparse.ArgumentParser();p.add_argument('--sep',default='yohane');p.add_argument('--condition',choices=['manual','auto'],default='manual');a=p.parse_args()
sys.path.insert(0,str(ROOT/'.deps/comparison/yohane'))
from yohane.audio import Wav2Vec2ForcedAligner
from yohane.lyrics import Lyrics
from yohane.subtitles import make_ass,time_lyrics
from dataclasses import asdict
assert torch.cuda.is_available();torch.set_num_threads(8)
model=Wav2Vec2ForcedAligner(str(ROOT/'.models/nextfire'))
for s in songs():
 sid=s['id'];target=OUT/'yohane'/f'{sid}-{a.sep}-{a.condition}.json'
 if exists(target) and read(target)['status']=='ok':continue
 stem=CACHE/'stems'/a.sep/f'{sid}.wav';r={'song':sid,'separator':a.sep,'condition':a.condition,'status':'failed','stem':stem.relative_to(ROOT).as_posix()};stage='frontend_g2p';start=time.monotonic()
 try:
  source=read(OUT/'yohane/inputs'/f'{sid}.json');r['input']='\n'.join(' '.join(w['roman'] for w in l['words'] if w['roman']) for l in source['lines']) if a.condition=='manual' else '\n'.join(plain_line(l['text']) for l in s['lines'])
  lyrics=Lyrics(r['input']);audio,rate=sf.read(stem,always_2d=True,dtype='float32');wave=torch.from_numpy(audio.T)
  stage='alignment_inference'
  emission,spans=model.align(model.tokenize(lyrics.transcript),wave,rate)
  stage='export'
  subs=make_ass(lyrics,wave,rate,model.tokenize,emission,spans)
  r.update(ass=subs.to_string('ass'),syllables=[[asdict(x) if x else None for x in l] for l in time_lyrics(lyrics,wave,rate,model.tokenize,emission,spans)],status='ok')
  del emission,spans
 except Exception as exc:r['error']={'type':type(exc).__name__,'message':portable(exc)[:800]};r['failed_stage']=stage;print(portable(traceback.format_exc()),flush=True)
 r['seconds']=time.monotonic()-start;dump(target.with_suffix('.json.gz'),r);torch.cuda.empty_cache();print('DONE',sid,a.sep,r['status'],flush=True)
