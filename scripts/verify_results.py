"""Require every planned condition, including explicitly recorded failures."""
from pathlib import Path
import gzip,json,collections,itertools,hashlib,sys,csv,statistics,math
sys.path.insert(0,str(Path(__file__).resolve().parent/"timing"))
from separator_registry import MODELS as SEPARATORS, LEGACY
ROOT=Path(__file__).resolve().parents[1]
def present(path):return path.is_file() or Path(str(path)+'.gz').is_file()
def read(path):
    if path.is_file():return json.loads(path.read_text())
    with gzip.open(str(path)+'.gz','rt') as f:return json.load(f)
all_ids=sorted(read(ROOT/'configs/dataset-ids.json').values())
ids=[s for s in all_ids if s!='s14']
primary=[s for s in ids if s not in ('s11','s13')]
reading_ids=read(ROOT/'configs/reading.json')['songs']
paired_n=sum(g['paired'] for s in read(ROOT/'results/ablation/targets.json') if s['id'] in primary for l in s['lines'] for g in l['groups'])
leaf_n=sum(len(l['reference']) for s in read(ROOT/'results/milikara/references.json') if s['id'] in primary for l in s['lines'])
for sid in all_ids:
    assert present(ROOT/'results/timing/baseline'/(sid+'.json'))
    for mode in ('untimed','trusted','lead_untimed'):
        folder=ROOT/'results/timing/timing'
        assert sum(present(folder/name) for name in (f'{sid}-{mode}.json',f'{sid}-{mode}-error.json'))==1,(sid,mode)
matrix=ROOT/'results/ablation'
count=0
for sep,backend,strategy,sid in itertools.product(('demucs','bs','kim'),('nextfire','mms_fa','tifa'),
    ('concat','padded','full','auto_nf','auto_mms','human','fixed_cores','auto_mms_pause'),ids):
    if sep=='demucs' and strategy=='fixed_cores':continue
    path=matrix/'predictions'/sep/backend/strategy/(sid+'.json')
    assert present(path),path
    count+=1
assert count==23*3*len(ids),count
for sep,strategy,sid in itertools.product(('scnet','dttnet','bs_roformer','mel_roformer','windowed'),('concat','padded','full'),ids):
    path=matrix/'predictions'/sep/'nextfire'/strategy/(sid+'.json')
    assert present(path),path
for r in read(matrix/'metrics.json')['aggregate']:
    if r['cohort']=='primary' and r['subset']=='all':
        assert r['songs']==len(primary) and r['n']==paired_n,r
mili=ROOT/'results/milikara'
groups=collections.defaultdict(set)
for path in (mili/'predictions').glob('*.json*'):
    base=path.with_suffix('') if path.suffix=='.gz' else path
    r=read(base);groups[r['experiment']].add(r['song'])
for exp,songs in groups.items():
    expected=set(primary+['s13'])
    assert songs==expected,(exp,songs,expected)
assert len(groups)==252,len(groups)
assert sum(map(len,groups.values()))==252*(len(primary)+1),sum(map(len,groups.values()))
for mode in ('global','concat_core','concat_padded'):
    for mask in range(32):assert f'{mode}/f{mask:05b}' in groups
for r in read(mili/'metrics.json'):
    if r['song']=='ALL' and r['group']=='all':assert r['n']==leaf_n,r
folder=ROOT/'results/separation-alignment'
for name,persist,mode,kind in itertools.product(SEPARATORS,
    ('float','pcm24'),('global','concat_core','concat_padded'),('confirmed-targets',)):
    expected=primary+['s13']
    for sid in expected:
        path=folder/'predictions'/name/persist/(sid+'--'+mode+'--'+kind+'.json')
        assert present(path),path
for model,repeat in itertools.product(('demucs','bs','kim'),(1,2)):
    assert present(matrix/'resource-benchmark'/f'{model}-{repeat}.json')
print('Complete:',len(all_ids)*3,'Timing pipeline cases;',count+15*len(ids),'module matrix cases;',60*(len(primary)+1),'separation alignment cases;',len(groups),'MiliKara configurations.')

for sid,mode,variant in itertools.product(primary,('global','concat_core'),('baseline','cached_window','local_fresh')):
 assert present(ROOT/'results/local-refinement/predictions'/f'{sid}--{mode}--{variant}.json')
for method in read(ROOT/'configs/reading.json')['methods']:
 for sid in reading_ids:
  inp=read(ROOT/'results/reading/inputs'/f'{sid}.json');pred=read(ROOT/'results/reading/predictions'/method/f'{sid}.json')
  assert len(inp['lines'])==len(pred['lines'])
  for a,b in zip(inp['lines'],pred['lines']):
   assert a['id']==b['id']
   if 'readings' in b:assert len(a['words'])==len(b['readings'])
local_metrics=read(ROOT/'results/local-refinement/metrics.json')
assert len(local_metrics)==6*(len(primary)+1)*3
for row in local_metrics:
 if row['song']=='ALL' and row['group']=='all':assert row['n']==leaf_n,row
assert len(read(ROOT/'results/local-refinement/runtime.json')['records'])==2*len(primary)
assert not read(ROOT/'results/reading/errors.json')
protocol=read(ROOT/'configs/reading.json')
reading_metrics=read(ROOT/'results/reading/metrics.json')
expected_reading_rows=set(itertools.product(('kanji_spans','japanese_lines'),protocol['methods'],['ALL','PRIMARY',*reading_ids]))
assert len(reading_metrics)==len(expected_reading_rows)
assert {(r['scope'],r['method'],r['song']) for r in reading_metrics}==expected_reading_rows
assert len(read(ROOT/'results/reading/inputs/s11.json')['lines'])==10
for record in read(ROOT/'results/reading/llm-execution.json')['records']:
 sid=record['song'];condition=record['condition']
 assert hashlib.sha256((ROOT/'results/reading/predictions'/('terra-'+condition)/(sid+'.json')).read_bytes()).hexdigest()==record['output_sha256']
 assert record['input_sha256']==protocol['input_sha256'][sid+'.json']
 if condition=='corrected':assert record['studio_candidate_sha256']==protocol['studio_prediction_sha256'][sid+'.json']
print('Complete:',6*len(primary),'refinement cases;',len(read(ROOT/'configs/reading.json')['methods'])*len(reading_ids),'reading cases.')

for name,digest in read(ROOT/'configs/reading.json')['input_sha256'].items():
 assert hashlib.sha256((ROOT/'results/reading/inputs'/name).read_bytes()).hexdigest()==digest
for sid in reading_ids:
 inp=read(ROOT/'results/reading/inputs'/f'{sid}.json')
 for row in inp['lines']:
  assert set(row)=={'id','text','words'} and ''.join(row['words'])==row['text']
  assert not any(c in row['text'] for c in '\n\r\t')

# Postprocessing must preserve the established MMS_FA baseline and every start/missing value.
gap=read(ROOT/'results/mms-gap-fill/metrics.json')
old=read(matrix/'metrics.json')['aggregate']
variants=set(read(ROOT/'configs/mms-gap-fill.json')['variants'])
lookup={(r['separator'],r['strategy'],r['variant'],r['subset'],r['song']):r for r in gap}
for original in old:
 if (original['backend'],original['cohort'],original['subset'])!=('mms_fa','primary','all'):continue
 key=(original['separator'],original['strategy'])
 base=lookup[(*key,'baseline','all','ALL')]
 for field in ('n','valid','missing','hit100','hit200'):
  assert base[field]==original[field],(key,field)
 assert abs(base['macro100']-original['macro100'])<1e-12
 for variant in variants:
  current=lookup[(*key,variant,'all','ALL')]
  assert current['n']==paired_n and current['missing']==base['missing']
  assert current['start_mae_ms']==base['start_mae_ms']
  assert current['hit100']==base['hit100']+current['gained100']-current['lost100']
  final=lookup[(*key,variant,'line_final','ALL')]
  assert final['changed']==0
  assert final['hit100']==lookup[(*key,'baseline','line_final','ALL')]['hit100']
assert len([r for r in gap if r['subset']=='all' and r['song']=='ALL'])==23*6
edits=read(ROOT/'results/mms-gap-fill/edits.json')
for row in edits:
 assert row['before'][0]==row['after'][0] and row['after'][1]>row['before'][1]

for name,device in itertools.product(SEPARATORS,('cpu','cuda')):
 suffix='-cpu' if device=='cpu' else ''
 record=read(ROOT/'results/separation-resources'/(name+suffix+'.json'))
 assert len(record['records'])==(3 if device=='cpu' else 15)
 assert record['threads']==8
 assert {(x['song'],x['repeat']) for x in record['records']}=={(s['id'],k) for s in record['inputs'] for k in (1,2,3)}
 assert all(x['seconds']>0 and x['rss_bytes']>0 for x in record['records'])
 if device=='cuda':
  assert record['gpu']=='NVIDIA GeForce RTX 4090'
  assert all(x['board_energy_joules']>0 for x in record['records'])
  field='process_gpu_bytes' if name=='sug' else 'allocated_bytes'
  assert all(x[field]>0 for x in record['records'])
 else:
  assert record['inputs']==read(ROOT/'configs/separation-cpu-inputs.json')
  assert all(x['duration']==30 and x['output_shape']==[2,1323000] and x['output_finite'] for x in record['records'])
  assert record['device']=='cpu' and record['gpu'] is None
  assert all(x['allocated_bytes'] is None and x['board_energy_joules'] is None for x in record['records'])
 if name=='sug':
  expected='CPUExecutionProvider' if device=='cpu' else 'CUDAExecutionProvider'
  assert record['identity']['providers'][0]==expected
for name in SEPARATORS:
 gpu=read(ROOT/'results/separation-resources'/(name+'.json'))
 cpu=read(ROOT/'results/separation-resources'/(name+'-cpu.json'))
 for key in ('state_sha256','weight_sha256'):
  assert gpu['identity'].get(key)==cpu['identity'].get(key),(name,key)
resource_summary=read(ROOT/'results/separation-resources/summary.json')
assert len(resource_summary)==20
assert {(r['model'],r['device']) for r in resource_summary}==set(itertools.product(SEPARATORS,('cpu','cuda')))
with (ROOT/'results/separation-resources/summary.csv').open() as stream:
 csv_rows=list(csv.DictReader(stream))
assert csv_rows==[{k:'' if v is None else str(v) for k,v in r.items()} for r in resource_summary]
for row in resource_summary:
 raw=read(ROOT/'results/separation-resources'/(row['model']+('-cpu' if row['device']=='cpu' else '')+'.json'))
 expected=sum(statistics.median(x['seconds'] for x in raw['records'] if x['song']==song['id']) for song in raw['inputs'])
 assert math.isclose(row['seconds'],expected,rel_tol=1e-12)
 assert row['runs']==len(raw['records'])
for name in ('bs','sug','milikara','yohane'):
 manifest=read(ROOT/'results/separation-alignment'/('stems-'+name+'.json'))
 assert {r['song'] for r in manifest['records']}==set(primary+['s13'])
 audit=manifest['native_equivalence']
 assert audit['max_absolute_difference']<=audit['tolerance']
summary=read(ROOT/'results/separation-alignment/metrics.json')
legacy_metrics={key:sorted((row for row in values if row['separator'] in LEGACY),key=lambda row:json.dumps(row,sort_keys=True)) for key,values in summary.items()}
assert hashlib.sha256(json.dumps(legacy_metrics,sort_keys=True).encode()).hexdigest()==read(ROOT/'results/separation-alignment/reuse-audit.json')['legacy_metrics_sha256']
with (ROOT/'results/separation-alignment/metrics.csv').open() as stream:
 assert list(csv.DictReader(stream))==[{k:str(v) for k,v in r.items()} for r in summary['aggregate']]
rows=[r for r in summary['aggregate'] if r['group']=='japanese']
assert len(rows)==60 and all(r['songs']==12 and r['n']==5370 for r in rows)
for path,expected in read(ROOT/'results/separation-alignment/reuse-audit.json')['preserved_files'].items():
 with (ROOT/path).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==expected,path
print('Complete:',23*6*len(primary),'MMS_FA postprocessing cases; 180 separator warm runs; 780 separator predictions.')
import subprocess,sys
subprocess.run([sys.executable,str(ROOT/'scripts/comparison/verify.py')],check=True)
