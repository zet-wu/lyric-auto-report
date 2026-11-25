"""Check dataset completeness, JSON syntax, local path leakage and required outputs."""
import argparse
import gzip
import json
from shared import ROOT, read, sha

parser = argparse.ArgumentParser()
parser.add_argument('--stage', choices=['0', '2'], default='2')
args = parser.parse_args()
manifest = read(ROOT / 'datasets/files.json')
rows = manifest if isinstance(manifest, list) else manifest['files']
for row in rows:
    path = ROOT / row['path']
    assert path.is_file() and path.stat().st_size == row['bytes'], row['path']
    assert sha(path) == row['sha256'], row['path']
assert len(rows) == 52, 'Expected 26 audio/annotation pairs'
checked = 0
for dirname in ('scripts', 'configs', 'results', 'datasets'):
    for path in (ROOT / dirname).rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        if path.name.endswith('.json.gz'):
            with gzip.open(path, 'rt', encoding='utf-8') as stream:
                value = json.load(stream)
            text = json.dumps(value, ensure_ascii=False, allow_nan=False)
        elif path.suffix == '.json':
            text = json.dumps(read(path), ensure_ascii=False, allow_nan=False)
        elif path.suffix in ('.py', '.csv', '.ts', '.cjs'):
            text = path.read_text(encoding='utf-8')
        else:
            continue
        assert '/' + 'home/' not in text, (path.relative_to(ROOT).as_posix(), 'local absolute path')
        checked += 1
required = [f'results/reading/inputs/j{i:02}.json' for i in range(1, 21)]
required += ['results/timing/reference.json', 'results/reading/references.json.gz']
if args.stage == '2':
    required += ['results/EXPERIMENT_INDEX.json']
    required += [f'results/M{i}/summary.json' for i in range(1, 10)]
    required += [f'results/M{i}/metrics.csv' for i in range(1, 10)]
for relative in required:
    assert (ROOT / relative).is_file(), relative
print(f'Validated {len(rows)} dataset files, {checked} data/code files, {len(required)} required outputs (Stage {args.stage}).')
