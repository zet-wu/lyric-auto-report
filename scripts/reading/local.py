"""Native deterministic readers; no manual reading/reference access."""
from common import *
import time,argparse
from server.reading import SudachiReadingProposer
from sudachipy import dictionary,tokenizer
from timing.japanese_dictionary import make_tagger
from timing.text import tokenize
from timing.singing import pronunciation_overrides
from kara_align.reading import japanese
parser=argparse.ArgumentParser();parser.add_argument('--methods',nargs='+',default=['studio','sudachi','milikara','milikara-fallback','timing','openjtalk']);args=parser.parse_args()
proposer=SudachiReadingProposer();assert proposer.available
sudachi=dictionary.Dictionary().create()
japanese._tagger_state['t']=make_tagger()
overrides=pronunciation_overrides()['ja']
runtime=[]
for method in args.methods:
 if method=='openjtalk':
  os.environ['OPEN_JTALK_DICT_DIR']=str(ROOT/'.models/openjtalk/open_jtalk_dic_utf_8-1.11')
  assert Path(os.environ['OPEN_JTALK_DICT_DIR']).is_dir(), 'Run scripts/download.py reading'
  import pyopenjtalk
 for path in sorted((OUT/'inputs').glob('*.json')):
  s=read(path);rows=[];t=time.perf_counter()
  for l in s['lines']:
   text=l['text'];error=None
   try:
    if method=='studio':
     proposals=proposer.propose([{'id':l['id'],'text':text}]);pairs=[];pos=0
     for p in proposals:
      if p.base_start>pos:pairs.append((text[pos:p.base_start],text[pos:p.base_start]))
      pairs.append((p.base,p.reading));pos=p.base_end
     if pos<len(text):pairs.append((text[pos:],text[pos:]))
    elif method=='sudachi':pairs=[(w.surface(),w.reading_form()) for w in sudachi.tokenize(text,tokenizer.Tokenizer.SplitMode.C)]
    elif method in ('milikara','milikara-fallback'):
     ss=japanese.rule_segments(text) if method=='milikara' else japanese._class_segments(text)
     pairs=[(p.surface,p.reading if p.reading is not None else ''.join(u.reading for u in p.units) if p.units else '' if p.uncertain else p.surface) for p in ss]
    elif method=='timing':
     pairs=[(w.text,overrides.get(w.spoken) or w.source_pronunciation or w.reading or w.spoken) for w in tokenize(text,fine=False)]
    else:
     nodes=pyopenjtalk.run_frontend(text)
     pairs=[(n['string'],n['pron'] if n['pron'] not in ('','*','、','？') else n['string']) for n in nodes]
    try:parts=segments(text,pairs)
    except ValueError:
     if method!='openjtalk':raise
     # OpenJTalk normalizes source spelling; retain the entire source interval.
     parts=[{'a':0,'b':len(text),'text':text,'reading':hira(''.join(r for _,r in pairs))}]
   except Exception as exc:
    parts=[{'a':0,'b':len(text),'text':text,'reading':''}];error=type(exc).__name__+': '+str(exc)
   rows.append({'id':l['id'],'parts':parts,**({'error':error} if error else {})})
  elapsed=time.perf_counter()-t
  dump(OUT/'predictions'/method/f"{s['song']}.json",{'song':s['song'],'method':method,'lines':rows})
  runtime.append({'song':s['song'],'method':method,'seconds':elapsed});print(method,s['song'],round(elapsed,3),flush=True)
 dump(OUT/'runtime'/f'{method}.json',[r for r in runtime if r['method']==method])
