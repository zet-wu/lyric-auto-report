"""Persist and reload the native SUG project after applying frozen AI results."""
from common import *
sys.path.insert(0,str(ROOT/'.deps/comparison/sug/src'))
from strange_uta_game.backend.domain import Project,Sentence,Singer,Character,Ruby,RubyPart
from strange_uta_game.backend.infrastructure.persistence.sug_io import SugProjectParser
from strange_uta_game.backend.application.ai_timing.commands import ApplyAiTimingCommand
from strange_uta_game.backend.application.ai_timing.pronunciation import PronunciationPlan,PronunciationUnit,ScriptKind,PronunciationSource
from strange_uta_game.backend.application.ai_timing.alignment import AlignmentRequest,AlignmentToken,MediaIdentity,AlignmentResult,EmissionSpan

def prepare_auto_project(project):
 from copy import deepcopy
 from strange_uta_game.backend.application.auto_check_service import AutoCheckService
 from strange_uta_game.backend.infrastructure.parsers.ruby_analyzer import SudachiAnalyzer
 from strange_uta_game.backend.infrastructure.data.default_dictionary import DEFAULT_RL_DICT_TEXT
 from strange_uta_game.frontend.settings.app_settings import AppSettings,_parse_rl_dictionary
 # Use the pinned product's factory configuration, never local user settings.
 flags=deepcopy(AppSettings.DEFAULT_SETTINGS['auto_check'])
 service=AutoCheckService(ruby_analyzer=SudachiAnalyzer(),auto_check_flags=flags,
                         user_dictionary=_parse_rl_dictionary(DEFAULT_RL_DICT_TEXT),chinese_mode=False)
 service.analyze_and_apply_pipeline(project,only_noruby=True,apply_user_dict=True,
                                   delete_types=flags['delete_ruby_types'] or None,update_checkpoints=True)
 return {'pipeline':'AutoCheckService.analyze_and_apply_pipeline','analyzer':'SudachiAnalyzer',
         'auto_check_flags':flags,'dictionary':'pinned packaged DEFAULT_RL_DICT_TEXT','update_checkpoints':True}

def create_project(song,condition):
 project=Project();project.audio_duration_ms=round(song['duration']*1000);project.singers=[Singer(id='s1',name='main')]
 if condition=='manual':
  src=read(OUT/'milikara/inputs/manual'/f"{song['id']}.json")
  for line in src['lines']:
   chars=[Character(char=w['text'],ruby=Ruby(parts=[RubyPart(u['reading']) for u in w['units']]) if w['units'] else None,check_count=len(w['units']),singer_id='s1') for w in line['words']]
   chars[-1].is_line_end=True;chars[-1].is_sentence_end=True
   project.sentences.append(Sentence(characters=chars,singer_id='s1'))
 else:
  project.sentences=[Sentence.from_text(plain_line(l['text']),singer_id='s1') for l in song['lines']]
  prepare_auto_project(project)
 for l in project.sentences:l.clear_all_timestamps()
 return project

def save_project(project,path):
 target=path.with_suffix('.json.gz')
 dump(target,SugProjectParser.serialize(project))
 return {'path':target.relative_to(ROOT).as_posix()}
