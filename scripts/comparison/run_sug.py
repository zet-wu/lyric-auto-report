from common import *
import argparse,time,traceback,xml.etree.ElementTree as ET
from dataclasses import asdict
import torch
sys.path.insert(0,str(ROOT/'.deps/comparison/sug/src'))
from strange_uta_game.backend.domain import Project,Sentence,Singer,Character,Ruby,RubyPart
from strange_uta_game.backend.infrastructure.parsers.ttml_parser import TTMLParser,build_ttml_sentences
from sug_project import save_project
from strange_uta_game.backend.application.ai_timing import PronunciationResolver,build_alignment_request,MediaIdentity,checkpoint_timestamps,ApplyAiTimingCommand
from strange_uta_game.backend.application.ai_timing.worker.providers import create_provider
p=argparse.ArgumentParser();p.add_argument('--model',default='nextfire');p.add_argument('--sep',default='sug');p.add_argument('--condition',default='manual');p.add_argument('--song');a=p.parse_args()
torch.set_num_threads(8);assert torch.cuda.is_available()
spec={'provider':'wav2vec2' if a.model=='nextfire' else 'mms_fa','model_id':str(ROOT/'.models/nextfire') if a.model=='nextfire' else 'MMS_FA','device':'cuda'}
provider=create_provider(spec);provider.load(spec,lambda f,m:print(m,flush=True),lambda:False)
for s in songs():
 sid=s['id']
 if a.song and sid!=a.song:continue
 target=OUT/'sug'/f'{sid}-{a.sep}-{a.model}-{a.condition}.json'
 if exists(target) and read(target)['status']=='ok':continue
 stem=CACHE/'stems'/a.sep/(sid+'.wav')
 if not stem.exists():raise FileNotFoundError(stem)
 r={'song':sid,'model':a.model,'condition':a.condition,'separator':a.sep,'status':'error','stem_sha256':sha(stem)};start=time.monotonic()
 try:
  project=Project();project.audio_duration_ms=round(s['duration']*1000);project.singers=[Singer(id='s1',name='main')]
  if a.condition=='manual':
   source=read(OUT/'milikara/inputs/manual'/f'{sid}.json')
   project.sentences=[]
   for line in source['lines']:
    chars=[]
    for w in line['words']:
     units=w['units']
     chars.append(Character(char=w['text'],ruby=Ruby(parts=[RubyPart(u['reading']) for u in units]) if units else None,check_count=len(units),singer_id='s1'))
    chars[-1].is_line_end=True;chars[-1].is_sentence_end=True
    project.sentences.append(Sentence(characters=chars,singer_id='s1'))
  else:project.sentences=[Sentence.from_text(l['text'],singer_id='s1') for l in s['lines']]
  assert len(project.sentences)==len(s['lines'])
  for l in project.sentences:l.clear_all_timestamps()
  resolver=PronunciationResolver(chinese_mode=False)
  plan=resolver.resolve_project(project,fill_missing=a.condition=='auto')
  r['plan']=asdict(plan);r['input_characters']=[[{'text':c.char,'check_count':c.check_count,'end':c.is_sentence_end} for c in l.characters] for l in project.sentences]
  if not plan.is_complete:raise ValueError('Unresolved readings: '+repr([(u.char_text,u.location) for u in plan.pending_units]))
  tail=3 if a.model=='mms-fa' else 0
  req=build_alignment_request(plan,MediaIdentity(str(stem),sha(stem),round(s['duration']*1000)),{'tail_snap':bool(tail),'tail_correct':tail,'tail_silence':5,'latin_word_split':1})
  result=provider.align(req,str(stem),lambda f,m:print(sid,m,flush=True),lambda:False)
  r.update(request=asdict(req),result=asdict(result),checkpoint_spans=[{'location':k,'start':v[0]/1000,'end':v[1]/1000} for k,v in checkpoint_timestamps(result,req).items()])
  ApplyAiTimingCommand(project,plan,req,result).execute()
  r['sug_project']=save_project(project,OUT/'sug/projects'/target.with_suffix('.sug').name);r['status']='ok'
 except Exception:r['error']=traceback.format_exc();print(r['error'],flush=True)
 r['seconds']=time.monotonic()-start;dump(target,r);print('DONE',sid,a.sep,a.model,a.condition,r['status'],flush=True)
provider.unload()
