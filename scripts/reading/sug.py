"""Run SUG's native auto-timing pronunciation resolver on text only."""
from common import *
import time
sys.path.insert(0,str(ROOT/'.deps/comparison/sug/src'))
from strange_uta_game.backend.domain import Project,Sentence,Singer
from strange_uta_game.backend.application.ai_timing import PronunciationResolver
runtime=[]
for sid in read(ROOT/'configs/reading.json')['songs']:
 s=read(OUT/'inputs'/f'{sid}.json');t=time.perf_counter();project=Project();project.singers=[Singer(id='s1',name='main')]
 project.sentences=[Sentence.from_text(l['text'],singer_id='s1') for l in s['lines']]
 plan=PronunciationResolver(chinese_mode=False).resolve_project(project,fill_missing=True)
 lookup={}
 for u in plan.units:
  if not u.is_sentence_end:lookup.setdefault((u.line_idx,u.char_idx),[]).append(u)
 lines=[]
 for li,(line,sentence) in enumerate(zip(s['lines'],project.sentences,strict=True)):
  pairs=[]
  for ci,char in enumerate(sentence.characters):
   us=lookup.get((li,ci),[])
   reading=''.join(u.reading or ('' if u.expects_token else u.char_text) for u in us) if us else char.char
   pairs.append((char.char,reading))
  lines.append({'id':line['id'],'parts':segments(line['text'],pairs)})
 dump(OUT/'predictions/sug'/f'{sid}.json',{'song':sid,'method':'sug','lines':lines})
 runtime.append({'song':sid,'method':'sug','seconds':time.perf_counter()-t,'pending_units':len(plan.pending_units)})
 print('SUG',sid,len(plan.pending_units),flush=True)
dump(OUT/'runtime/sug.json',runtime)
