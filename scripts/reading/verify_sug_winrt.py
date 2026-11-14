"""Audit a SUG-only refresh against a pre-run local snapshot."""
from common import *
import argparse,hashlib,math,subprocess

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--baseline',type=Path,required=True)
parser.add_argument('--capture',action='store_true',help='Save the protected files and reading scores before the refresh.')
args=parser.parse_args()
baseline=args.baseline
if args.capture:
 assert not baseline.exists(),'Choose a new baseline directory; existing snapshots must not be overwritten'
 paths=subprocess.check_output(['git','-c',f'safe.directory={ROOT.as_posix()}','ls-files','-z','results','datasets','configs'],cwd=ROOT).decode('utf-8').split('\0')
 dump(baseline/'hashes.json',{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths if p})
 for name in ('metrics','items','lines','excluded','errors'):
  (baseline/f'{name}.json').write_bytes((OUT/f'{name}.json').read_bytes())
 print('Saved pre-run baseline:',baseline)
 sys.exit(0)
hashes=read(baseline/'hashes.json')
allowed={'results/reading/'+name+'.json' for name in ('metrics','items','lines')}
allowed.update({'configs/reading.json','results/reading/runtime/sug-winrt.json','results/reading/sug-winrt-environment.json','results/reading/sug-winrt-audit.json'})
allowed.update('results/reading/predictions/sug-winrt/'+sid+'.json' for sid in read(ROOT/'configs/reading.json')['songs'])
changed=[]
for path,digest in hashes.items():
 if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:
  assert path in allowed,('Unexpected changed input or result',path)
  changed.append(path)

def semantic(value):
 return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()

checks={}
for name in ('metrics','items','lines'):
 old=read(baseline/f'{name}.json');new=read(OUT/f'{name}.json')
 other_new=[r for r in new if r['method']!='sug-winrt']
 fields=other_new[0].keys()
 other_old=[{k:r[k] for k in fields} for r in old if r['method']!='sug-winrt']
 assert other_old==other_new,('Other method scores changed',name)
 checks[name]={'other_method_rows':len(other_new),'other_method_semantic_sha256':semantic(other_new),'current_semantic_sha256':semantic(new)}
 if name in ('items','lines'):
  keys=('song','line','a','b','source','method','reference') if name=='items' else ('song','line','source','method','reference')
  assert [[r[k] for k in keys] for r in other_old]==[[r[k] for k in keys] for r in other_new],('Scoring partitions changed',name)
for name in ('excluded','errors'):
 assert (baseline/f'{name}.json').read_bytes()==(OUT/f'{name}.json').read_bytes(),name

# Independently recompute edit counts with a full matrix, and check that scored
# strings actually come from the saved SUG predictions on the frozen spans.
def edits(left,right):
 matrix=[[0]*(len(right)+1) for _ in range(len(left)+1)]
 for i in range(len(left)+1):matrix[i][0]=i
 for j in range(len(right)+1):matrix[0][j]=j
 for i in range(1,len(left)+1):
  for j in range(1,len(right)+1):
   matrix[i][j]=min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+(left[i-1]!=right[j-1]))
 return matrix[-1][-1]

protocol=read(ROOT/'configs/reading.json')
predictions={sid:{r['id']:r for r in read(OUT/'predictions/sug-winrt'/f'{sid}.json')['lines']} for sid in protocol['songs']}
metrics=[r for r in read(OUT/'metrics.json') if r['method']=='sug-winrt']
for scope,name in [('kanji_spans','items'),('japanese_lines','lines')]:
 rows=[r for r in read(OUT/f'{name}.json') if r['method']=='sug-winrt']
 for row in rows:
  parts=predictions[row['song']][row['line']]['parts']
  if scope=='kanji_spans':parts=[p for p in parts if row['a']<=p['a'] and p['b']<=row['b']]
  assert clean(''.join(p['reading'] for p in parts))==row['prediction']
  assert edits(row['reference'],row['prediction'])==row['edits']
  assert (row['reference']==row['prediction'])==row['exact']
 for metric in [r for r in metrics if r['scope']==scope]:
  sid=metric['song']
  selected=[r for r in rows if sid=='ALL' or sid=='PRIMARY' and r['song'] in protocol['primary_songs'] or r['song']==sid]
  exact=sum(r['exact'] for r in selected);denom=len(selected)
  chars=sum(len(r['reference']) for r in selected);errors=sum(r['edits'] for r in selected)
  assert (metric['n'],metric['exact'],metric['edits'],metric['reference_characters'])==(denom,exact,errors,chars)
  assert math.isclose(metric['accuracy_pct'],100*exact/denom)
  assert math.isclose(metric['cer_pct'],100*errors/chars)
  assert math.isclose(metric['kana_coverage_pct'],100*sum(kana(r['prediction']) for r in selected)/denom)

env=read(OUT/'sug-winrt-environment.json');runtime=read(OUT/'runtime/sug-winrt.json')
assert env['require_winrt'] and env['system']=='Windows'
assert env['source_commit']==read(ROOT/'configs/comparison-sources.json')['sug']['commit']
normalize_name=lambda s:re.sub('[-_.]+','-',s).lower()
installed={normalize_name(k):v for k,v in env['packages'].items()}
for line in (ROOT/'requirements/reading-sug-winrt-lock.txt').read_text(encoding='utf-8').splitlines():
 if line and not line.startswith('#'):
  name,version=line.split('==')
  assert installed[normalize_name(name)]==version,(name,version)
for sid,digest in env['input_sha256'].items():
 assert digest==protocol['input_sha256'][f'{sid}.json']==hashlib.sha256((OUT/'inputs'/f'{sid}.json').read_bytes()).hexdigest()
assert [r['song'] for r in runtime]==protocol['songs']
assert all(r['analyzer']=='WinRTAnalyzer' and r['pending_units']==len(r['pending_details']) for r in runtime)
for sid,digest in env['prediction_sha256'].items():
 assert hashlib.sha256((OUT/'predictions/sug-winrt'/f'{sid}.json').read_bytes()).hexdigest()==digest
before=[{k:r[k] for k in metrics[0]} for r in read(OUT/'metrics.json') if r['method']=='sug' and r['song'] in ('PRIMARY','s11')]
after=[r for r in metrics if r['song'] in ('PRIMARY','s11')]
audit={'scope':'SUG Sudachi fallback retained alongside Windows WinRT; other prediction values and timing experiments unchanged','baseline_file_count':len(hashes),'unchanged_baseline_files':len(hashes)-len(changed),'changed_baseline_files':sorted(changed),'other_predictions_unchanged':True,'timing_results_unchanged':True,'scoring_partitions_unchanged':True,'excluded_and_errors_unchanged':True,'independent_sug_score_check':True,'score_checks':checks,'songs':len(runtime),'lines':sum(len(v) for v in predictions.values()),'pending_units':sum(r['pending_units'] for r in runtime),'before_metrics':before,'after_metrics':after}
dump(OUT/'sug-winrt-audit.json',audit)
print(json.dumps({k:v for k,v in audit.items() if k not in ('score_checks','before_metrics','after_metrics','changed_baseline_files')},ensure_ascii=False,indent=2))
