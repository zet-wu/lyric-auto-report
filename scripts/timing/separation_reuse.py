"""Validate frozen assets and record immutable results retained by the experiment."""
from separator_registry import *
import hashlib, json, gzip, subprocess

def digest(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()
def read(path):
    if path.suffix=='.gz':
        with gzip.open(path,'rt') as f:return json.load(f)
    return json.loads(path.read_text())
assets=read(ROOT/'configs/separation-models.json')
for asset in assets:
    assert digest(ROOT/asset['path'])==asset['sha256'],asset['path']
for group in ('configs/sources.json','configs/comparison-sources.json'):
    for name,identity in read(ROOT/group).items():
        folder=ROOT/'.deps'/('comparison' if 'comparison-' in group else '')/name
        if 'comparison-' not in group and (ROOT/'.deps/comparison'/name).exists():folder=ROOT/'.deps/comparison'/name
        if folder.exists() and 'commit' in identity:
            assert subprocess.check_output(['git','-C',str(folder),'rev-parse','HEAD'],text=True).strip()==identity['commit'],name
for song in read(ROOT/'configs/separation-resources-inputs.json'):
    assert digest(ROOT/song['audio'])==song['sha256']
files={}
for name in LEGACY:
    resource=ROOT/'results/separation-resources'/f'{name}.json'
    data=read(resource)
    assert len(data['records'])==15 and data['gpu']=='NVIDIA GeForce RTX 4090' and data['threads']==8
    files[str(resource.relative_to(ROOT))]=digest(resource)
    for path in (ROOT/'results/separation-alignment/predictions'/name).rglob('*.json*'):
        files[str(path.relative_to(ROOT))]=digest(path)
for path in (ROOT/'results/comparison/scores').glob('*'):
    if path.is_file():files[str(path.relative_to(ROOT))]=digest(path)
# Re-running the audit checks previously recorded identities rather than blessing changes.
out=ROOT/'results/separation-alignment/reuse-audit.json'
metrics=read(ROOT/'results/separation-alignment/metrics.json')
legacy_metrics={key:sorted((row for row in rows if row['separator'] in LEGACY),key=lambda row:json.dumps(row,sort_keys=True)) for key,rows in metrics.items()}
metrics_hash=hashlib.sha256(json.dumps(legacy_metrics,sort_keys=True).encode()).hexdigest()
record={'legacy_metrics_sha256':metrics_hash,'assets':assets,'preserved_files':files,'resource_records':90,
        'downstream_predictions':sum('/predictions/' in p for p in files),
        'policy':'Frozen input/assets and preserved result hashes; native adapters verified separately. CPU records are independent measurements.'}
if out.exists():assert read(out)==record,'Previously audited results or identities changed'
else:out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('Verified assets and retained results:',len(files))
