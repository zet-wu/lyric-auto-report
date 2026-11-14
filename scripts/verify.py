"""Check a publication checkout using Python's standard library."""
from pathlib import Path
import ast,gzip,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
def read(path):
    if path.suffix=='.gz':
        with gzip.open(path,'rt') as f:return json.load(f)
    return json.loads(path.read_text())
manifest=read(ROOT/'datasets/files.json')
rows=manifest if isinstance(manifest,list) else manifest['files']
for row in rows:
    path=ROOT/row['path']
    assert path.is_file(),row['path']
    assert path.stat().st_size==row['bytes'],row['path']
    with path.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==row['sha256'],row['path']
checked=0
for dirname in ('scripts','configs','reports','results','requirements'):
    for path in (ROOT/dirname).rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts:continue
        assert not path.is_symlink(),path
        if path.suffix=='.py':ast.parse(path.read_text())
        if path.suffix in ('.json','.gz','.sug'):
            value=read(path)
            text=json.dumps(value,ensure_ascii=False,allow_nan=False)
        elif path.suffix in ('.md','.py','.cjs','.txt','.csv','.yaml','.yml'):
            text=path.read_text()
        else:continue
        assert not re.search(r'/(?:home|tmp|opt)/',text),(path,'absolute local path')
        checked+=1
for doc in [ROOT/'README.md',*(ROOT/'reports').glob('*.md'),ROOT/'THIRD_PARTY.md',ROOT/'datasets/README.md',ROOT/'AGENTS.md']:
    text=doc.read_text()
    assert not re.search(r'/(?:home|tmp|opt)/',text),(doc,'absolute local path')
    assert not re.search(r'20\d\d[-/]\d\d[-/]\d\d',text),(doc,'date')
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if '://' in link or link.startswith('#'):continue
        path=doc.parent/link.split('#')[0]
        assert path.exists(),(doc,link)
for kind in ('confirmed-targets',):
    path=ROOT/'results/milikara'/(kind+'.json')
    if path.exists():
        def check(v):
            if isinstance(v,dict):
                if 'wordId' not in v:assert not {'start','end','begin','duration'}.intersection(v),v
                assert all(v.get(k) is None for k in ('beginMs','endMs')),v
                for x in v.values():check(x)
            elif isinstance(v,list):
                for x in v:check(x)
        check(read(path))
print(f'Validated {len(rows)} input files, {checked} text/result files, report links and timestamp-free MiliKara targets.')
