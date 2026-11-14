from common import *
import argparse,time,traceback
os.environ['PYTHONPATH']=str(ROOT/'.deps/comparison/milikara')
os.environ['KARA_ALIGN_MODELS']=str(ROOT/'.models/milikara-native');os.environ['KARA_ALIGN_HOME']=str(CACHE/'milikara-home')
sys.path.insert(0,str(ROOT/'.deps/comparison/milikara'))
import torch
from kara_align import service as S
from kara_align.models import Segment,Unit
torch.set_num_threads(8);assert torch.cuda.is_available()
p=argparse.ArgumentParser();p.add_argument('--song');p.add_argument('--sep',default='milikara');p.add_argument('--condition',default='manual');a=p.parse_args()
for song in songs():
 sid=song['id'];sep=a.sep;condition=a.condition
 if a.song and sid!=a.song:continue
 target=OUT/'milikara/runs'/f'{sid}-{sep}-{condition}.json'
 if exists(target) and read(target)['status']=='ok':continue
 source=read(OUT/'milikara/inputs'/('manual' if condition=='manual' else 'text')/f'{sid}.json')
 stem=CACHE/'stems'/sep/(sid+'.wav')
 if not stem.exists():raise FileNotFoundError(stem)
 record={'song':sid,'condition':condition,'separator':sep,'status':'error','stem_sha256':sha(stem)};start=time.monotonic()
 try:
  work=CACHE/'milikara-projects'/f'{sid}-{sep}-{condition}'
  h=S.open_dir(work) if (work/'project.json').exists() else S.create_dir(work,source['name'],mode='plain')
  if h.project.asset('original') is None:S.add_media(h,ROOT/source['audio'],role='original')
  if h.project.asset('vocals') is None:S.add_media(h,stem,role='vocals')
  if h.project.asset('instrumental') is None:
   # Native imported-stem contract requires both stems; residual is never aligned.
   import librosa,numpy as np,soundfile as sf
   vocals,rate=sf.read(stem,always_2d=True,dtype='float32')
   original,_=librosa.load(ROOT/source['audio'],sr=rate,mono=False)
   if original.ndim==1:original=original[None,:]
   original=original.T
   n=min(len(original),len(vocals));residual=CACHE/'stems'/sep/(sid+'-instrumental.wav')
   sf.write(residual,original[:n]-vocals[:n],rate,subtype='FLOAT')
   S.add_media(h,residual,role='instrumental')
  preview=S.parse_lyrics(h,'\n'.join(l['text'] for l in source['lines']),mode='plain')
  if preview.get('error'):raise RuntimeError(preview['error'])
  S.apply_lyrics(h,preview['preview_id'],prepare=condition=='auto')
  assert len(h.project.lyrics.lines)==len(source['lines'])
  for line,original in zip(h.project.lyrics.lines,source['lines']):
   assert line.text==original['text'];line.id=original['id']
   assert line.imported_start_ms is None and line.imported_end_ms is None and line.anchor is None
   if condition=='manual':
    line.segments=[]
    for word in original['words']:
     units=[Unit(id=u['id'],reading=u['reading']) for u in word['units']];reading=''.join(u.reading for u in units)
     lang='en' if reading.isascii() and any(c.isalpha() for c in reading) else 'ja'
     line.segments.append(Segment(id=word['id'],surface=word['text'],reading=reading,lang=lang,units=units,reading_source='manual',confirmed=True))
  h.save();record['lyrics']=h.project.lyrics.model_dump(mode='json')
  S.update_settings(h,config={'device':'cuda','model_id':str(ROOT/'.models/nextfire')})
  record['config']=h.project.config.model_dump(mode='json')
  result=S.run_align(h,audio_role='vocals',progress=lambda f,m='':print(sid,sep,condition,m,flush=True))
  record['result']=result.model_dump(mode='json');record['export']=json.loads(S.export(h,'alignment').content);record['status']='ok'
 except Exception:record['error']=traceback.format_exc();print(record['error'],flush=True)
 record['seconds']=time.monotonic()-start;dump(target,record);print('DONE',sid,sep,condition,record['status'],flush=True)
