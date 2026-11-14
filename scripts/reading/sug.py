"""Run SUG text reading: Sudachi fallback by default, or separate WinRT output."""
from common import *
import time,argparse,hashlib,platform,subprocess
from importlib.metadata import distributions
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--require-winrt',action='store_true',help='Fail instead of falling back to another reading engine.')
parser.add_argument('--output-dir',type=Path,default=OUT,help='Prediction and runtime output root; inputs always come from results/reading.')
args=parser.parse_args()
output=args.output_dir
method='sug-winrt' if args.require_winrt else 'sug'
sys.path.insert(0,str(ROOT/'.deps/comparison/sug/src'))
from strange_uta_game.backend.domain import Project,Sentence,Singer
from strange_uta_game.backend.application.ai_timing import PronunciationResolver
from strange_uta_game.backend.infrastructure.parsers.ruby_analyzer import create_analyzer,WinRTAnalyzer,SudachiAnalyzer
source=ROOT/'.deps/comparison/sug'
commit=subprocess.check_output(['git','-c',f'safe.directory={source.as_posix()}','-C',str(source),'rev-parse','HEAD'],text=True).strip()
assert commit==read(ROOT/'configs/comparison-sources.json')['sug']['commit'],'SUG source commit mismatch'
assert not subprocess.check_output(['git','-c',f'safe.directory={source.as_posix()}','-C',str(source),'status','--porcelain'],text=True).strip(),'Modified SUG source'
input_hashes={sid:hashlib.sha256((OUT/'inputs'/f'{sid}.json').read_bytes()).hexdigest() for sid in read(ROOT/'configs/reading.json')['songs']}
for sid,digest in input_hashes.items():
 assert digest==read(ROOT/'configs/reading.json')['input_sha256'][f'{sid}.json'],f'Input changed: {sid}'
runtime=[]
for sid in read(ROOT/'configs/reading.json')['songs']:
 s=read(OUT/'inputs'/f'{sid}.json');t=time.perf_counter();project=Project();project.singers=[Singer(id='s1',name='main')]
 project.sentences=[Sentence.from_text(l['text'],singer_id='s1') for l in s['lines']]
 analyzer=create_analyzer() if args.require_winrt else SudachiAnalyzer()
 if args.require_winrt:
  assert isinstance(analyzer,WinRTAnalyzer),'WinRT unavailable; fallback is forbidden'
  assert analyzer._pykakasi_conv is not None,'Native character-reading reference dependency is missing'
 print('SUG',sid,type(analyzer).__name__,'starting',flush=True)
 plan=PronunciationResolver(analyzer=analyzer,chinese_mode=False).resolve_project(project,fill_missing=True)
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
 dump(output/'predictions'/method/f'{sid}.json',{'song':sid,'method':method,'lines':lines})
 runtime.append({'song':sid,'method':method,'analyzer':type(analyzer).__name__,'seconds':time.perf_counter()-t,'pending_units':len(plan.pending_units),'pending_details':[{'line_idx':u.line_idx,'char_idx':u.char_idx,'char_text':u.char_text} for u in plan.pending_units]})
 print('SUG',sid,len(plan.pending_units),flush=True)
dump(output/'runtime'/f'{method}.json',runtime)
dump(output/f'{method}-environment.json',{'method':method,'source_commit':commit,'python':platform.python_version(),'system':platform.system(),'windows_version':platform.version(),'machine':platform.machine(),'require_winrt':args.require_winrt,'packages':dict(sorted((d.metadata['Name'],d.version) for d in distributions())),'input_sha256':input_hashes,'prediction_sha256':{sid:hashlib.sha256((output/'predictions'/method/f'{sid}.json').read_bytes()).hexdigest() for sid in input_hashes}})
