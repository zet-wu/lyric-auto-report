"""Persist and reload the native SUG project after applying frozen AI results."""
from common import *
sys.path.insert(0,str(ROOT/'.deps/comparison/sug/src'))
from strange_uta_game.backend.domain import Project,Sentence,Singer,Character,Ruby,RubyPart
from strange_uta_game.backend.infrastructure.persistence.sug_io import SugProjectParser
from strange_uta_game.backend.application.ai_timing.commands import ApplyAiTimingCommand
from strange_uta_game.backend.application.ai_timing.pronunciation import PronunciationPlan,PronunciationUnit,ScriptKind,PronunciationSource
from strange_uta_game.backend.application.ai_timing.alignment import AlignmentRequest,AlignmentToken,MediaIdentity,AlignmentResult,EmissionSpan

def create_project(song,condition):
 project=Project();project.audio_duration_ms=round(song['duration']*1000);project.singers=[Singer(id='s1',name='main')]
 if condition=='manual':
  src=read(OUT/'milikara/inputs/manual'/f"{song['id']}.json")
  for line in src['lines']:
   chars=[Character(char=w['text'],ruby=Ruby(parts=[RubyPart(u['reading']) for u in w['units']]) if w['units'] else None,check_count=len(w['units']),singer_id='s1') for w in line['words']]
   chars[-1].is_line_end=True;chars[-1].is_sentence_end=True
   project.sentences.append(Sentence(characters=chars,singer_id='s1'))
 else:project.sentences=[Sentence.from_text(l['text'],singer_id='s1') for l in song['lines']]
 for l in project.sentences:l.clear_all_timestamps()
 return project

def save_project(project,path):
 # Stable IDs make the persisted experiment easy to inspect; they do not affect timing.
 project.id=path.stem
 for i,l in enumerate(project.sentences):l.id=f'{path.stem}-line-{i}'
 SugProjectParser.save(project,str(path))
 saved=read(path);loaded=SugProjectParser.load(str(path));again=SugProjectParser.serialize(loaded)
 assert saved['sentences']==again['sentences']
 assert saved['audio_duration_ms']==again['audio_duration_ms']
 for before,after in zip(project.sentences,loaded.sentences):
  assert [(c.char,c.check_count,c.timestamps,c.sentence_end_ts) for c in before.characters]==[(c.char,c.check_count,c.timestamps,c.sentence_end_ts) for c in after.characters]
 return {'path':str(path.relative_to(ROOT)),'sha256':sha(path),'round_trip_equal':True,
         'checkpoint_count':sum(len(c['timestamps']) for l in saved['sentences'] for c in l['characters']),
         'sentence_end_count':sum(c['sentence_end_ts'] is not None for l in saved['sentences'] for c in l['characters'])}

def main():
 checks=[]
 for song in songs():
  for model in ('nextfire','mms-fa'):
   for sep,condition in [('sug','manual'),('bs','manual'),('sug','auto')]:
    path=OUT/'sug'/f"{song['id']}-{sep}-{model}-{condition}.json";r=read(path)
    if r['status']!='ok':continue
    project=create_project(song,condition)
    p=r['plan'];plan=PronunciationPlan(**{**p,'units':[PronunciationUnit(**{**u,'script':ScriptKind(u['script']),'source':PronunciationSource(u['source']) if u['source'] else None}) for u in p['units']]})
    q=r['request'];request=AlignmentRequest(**{**q,'media':MediaIdentity(**q['media']) if q['media'] else None,'tokens':[AlignmentToken(**{**t,'location':tuple(t['location'])}) for t in q['tokens']]})
    z=r['result'];result=AlignmentResult(**{**z,'spans':[EmissionSpan(**x) for x in z['spans']]})
    ApplyAiTimingCommand(project,plan,request,result).execute()
    r['sug_project']=save_project(project,OUT/'sug/projects'/path.with_suffix('.sug').name)
    r.pop('ttml',None);dump(path,r);checks.append(r['sug_project'])
 dump(OUT/'sug-project-audit.json',{'projects':checks,'source':'Native ApplyAiTimingCommand, SugProjectParser.save and load; original frozen model results reused.','round_trip_equal':True})
 print('Saved and round-trip verified',len(checks),'native SUG projects')
if __name__=='__main__':main()
