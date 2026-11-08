"""Require every planned condition, including explicitly recorded failures."""
from pathlib import Path
import gzip,json,collections,itertools,hashlib
ROOT=Path(__file__).resolve().parents[1]
def present(path):return path.is_file() or Path(str(path)+'.gz').is_file()
def read(path):
    if path.is_file():return json.loads(path.read_text())
    with gzip.open(str(path)+'.gz','rt') as f:return json.load(f)
all_ids=[f's{i:02}' for i in range(1,15)]
ids=all_ids[:-1]
primary=[s for s in ids if s not in ('s11','s13')]
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
assert count==897,count
for sep,strategy,sid in itertools.product(('scnet','dttnet','bs_roformer','mel_roformer','windowed'),('concat','padded','full'),ids):
    path=matrix/'predictions'/sep/'nextfire'/strategy/(sid+'.json')
    assert present(path),path
for r in read(matrix/'metrics.json')['aggregate']:
    if r['cohort']=='primary' and r['subset']=='all':
        assert r['songs']==11 and r['n']==4590,r
mili=ROOT/'results/milikara'
groups=collections.defaultdict(set)
for path in (mili/'predictions').glob('*.json*'):
    base=path.with_suffix('') if path.suffix=='.gz' else path
    r=read(base);groups[r['experiment']].add(r['song'])
for exp,songs in groups.items():
    expected=set(primary+['s13'])
    assert songs==expected,(exp,songs,expected)
assert len(groups)==252,len(groups)
assert sum(map(len,groups.values()))==3024,sum(map(len,groups.values()))
for mode in ('global','concat_core','concat_padded'):
    for mask in range(32):assert f'{mode}/f{mask:05b}' in groups
for r in read(mili/'metrics.json'):
    if r['song']=='ALL' and r['group']=='all':assert r['n']==4984,r
folder=ROOT/'results/separation-alignment'
for name,persist,mode,kind in itertools.product(('demucs','scnet','dttnet','bs_roformer','mel_roformer','windowed'),
    ('float','pcm24'),('global','concat_core','concat_padded'),('confirmed-targets',)):
    expected=primary+['s13']
    for sid in expected:
        path=folder/'predictions'/name/persist/(sid+'--'+mode+'--'+kind+'.json')
        assert present(path),path
for model,repeat in itertools.product(('demucs','bs','kim'),(1,2)):
    assert present(matrix/'resource-benchmark'/f'{model}-{repeat}.json')
print('Complete: 42 Timing pipeline cases, 1092 module matrix cases, 432 separation alignment cases,',len(groups),'MiliKara configurations, 6 resource runs.')

for sid,mode,variant in itertools.product(primary,('global','concat_core'),('baseline','cached_window','local_fresh')):
 assert present(ROOT/'results/local-refinement/predictions'/f'{sid}--{mode}--{variant}.json')
for method in ('studio','sudachi','milikara','milikara-fallback','timing','openjtalk','terra-direct','terra-corrected','luna-direct','luna-corrected'):
 for sid in primary:
  inp=read(ROOT/'results/reading/inputs'/f'{sid}.json');pred=read(ROOT/'results/reading/predictions'/method/f'{sid}.json')
  assert len(inp['lines'])==len(pred['lines'])
  for a,b in zip(inp['lines'],pred['lines']):
   assert a['id']==b['id']
   if 'readings' in b:assert len(a['words'])==len(b['readings'])
assert len(read(ROOT/'results/local-refinement/runtime.json')['records'])==22
assert not read(ROOT/'results/reading/errors.json')
print('Complete: 66 manual-reading refinement cases and 110 reading cases.')

for name,digest in read(ROOT/'configs/reading.json')['input_sha256'].items():
 assert hashlib.sha256((ROOT/'results/reading/inputs'/name).read_bytes()).hexdigest()==digest
for sid in primary:
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
  assert current['n']==4590 and current['missing']==base['missing']
  assert current['start_mae_ms']==base['start_mae_ms']
  assert current['hit100']==base['hit100']+current['gained100']-current['lost100']
  final=lookup[(*key,variant,'line_final','ALL')]
  assert final['changed']==0
  assert final['hit100']==lookup[(*key,'baseline','line_final','ALL')]['hit100']
assert len([r for r in gap if r['subset']=='all' and r['song']=='ALL'])==23*6
edits=read(ROOT/'results/mms-gap-fill/edits.json')
for row in edits:
 assert row['before'][0]==row['after'][0] and row['after'][1]>row['before'][1]

native=ROOT/'results/milikara-native'
for sid,condition in itertools.product(all_ids,('auto','manual')):
 result=read(native/'runs'/f'{sid}-{condition}.json')
 assert result['song']==sid and result['condition']==condition
 assert result['status']=='ok' or result.get('error')
 if result['status']=='ok':assert result['export']['units_and_lines_equal']
 for line in result.get('lyrics',{}).get('lines',[]):
  assert line['imported_start_ms'] is None and line['imported_end_ms'] is None and line['anchor'] is None
 for kind in ('text','manual'):
  inp=read(native/'inputs'/kind/f'{sid}.json')
  def untimed(value):
   if isinstance(value,dict):
    assert not {'start','end','start_ms','end_ms','anchor','begin','duration'}.intersection(value)
    for v in value.values():untimed(v)
   elif isinstance(value,list):
    for v in value:untimed(v)
  untimed(inp)
metric=read(native/'metrics.json')
assert len(metric['completion'])==28
for row in metric['aggregate']:
 if row['comparison']=='leaf' and row['language']=='ja':assert row['n']==4871 and row['songs']==11
 if row['comparison']=='leaf' and row['language']=='latin':assert row['n']==113
common=[r for r in metric['aggregate'] if r['comparison']=='common_text' and r['language']=='ja']
assert len({r['n'] for r in common})==1 and all(r['songs']==11 for r in common)
assert len(list((native/'separation').glob('*.json')))==13
print('Complete: 1518 MMS_FA postprocessing cases and 28 native MiliKara alignment cases.')
