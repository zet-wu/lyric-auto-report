from common import *
os.environ['NLTK_DATA']=str(ROOT/'.models/comparison/nltk')
import time,traceback,torch,librosa,unicodedata
sys.path.insert(0,str(ROOT/'.deps/comparison/fa-kara'))
import haruraw2norm as hn
from align import align_audio_with_text
from utils_audio import non_silent_recog,func_tail_correct_v250615
from utils_basic import non_silent_head_adjust
import norm2ass
from norm2lrc import process_rlf
assert torch.cuda.is_available();torch.set_num_threads(8)
# Reuse the identical official torchaudio bundle checkpoint, without a download.
import torchaudio
checkpoint=ROOT/'.models/torch/hub/checkpoints'/Path(torchaudio.pipelines.MMS_FA._path).name
if not checkpoint.exists():checkpoint.symlink_to(ROOT/'.models/mms-fa/model.pt')
for s in songs():
 sid=s['id'];target=OUT/'fa-kara'/f'{sid}-bs-manual.json'
 if exists(target) and read(target)['status']=='ok':continue
 stem=CACHE/'stems/bs'/f'{sid}.wav';r={'song':sid,'separator':'bs','condition':'manual','status':'error','stem_sha256':sha(stem)};start=time.monotonic()
 try:
  src=read(OUT/'milikara/inputs/manual'/f'{sid}.json');rows=[]
  for l in src['lines']:
   pieces=[]
   for w in l['words']:
    rd=''.join(u['reading'] for u in w['units'])
    surface=''.join(c for c in unicodedata.normalize('NFKC',w['text']) if c.isalnum() or c in "ー'’")
    pieces.append(w['text'] if not rd or surface==rd else ('['+w['text']+'|'+rd.lower()+']' if rd.isascii() else '{'+w['text']+'|'+rd+'}'))
   rows.append(''.join(pieces))
  r['input']='\n'.join(rows);items=[]
  for row in rows:items.extend(hn.process_haruhi_line(row+'\n','jaen',0,1))
  if items[-1]['orig']!='\n':items.append({'orig':'\n','type':0,'pron':''})
  indexes=[i for i,x in enumerate(items) if x.get('pron')];tokens=[items[i]['pron'] for i in indexes]
  r['input_items']=items.copy();audio,rate=librosa.load(stem,sr=None)
  ranges=non_silent_recog(audio,rate,.8,10,.1)
  result=align_audio_with_text(audio,tokens,ranges,rate,1,use_gpu=True)
  for i,x in zip(indexes,result):items[i].update(start=x['start'],end=x['end'])
  items=non_silent_head_adjust(items,ranges);items=func_tail_correct_v250615(items,audio,rate,10,.1)
  r.update(items=items,ass=norm2ass.process_norm2assV2(items),rlf=process_rlf(items),status='ok')
 except Exception:r['error']=traceback.format_exc();print(r['error'],flush=True)
 r['seconds']=time.monotonic()-start;dump(target,r);torch.cuda.empty_cache();print('DONE',sid,r['status'],flush=True)
