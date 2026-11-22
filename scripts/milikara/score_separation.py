"""Score all separator/target/persistence conditions with fixed denominators."""
from common import *
from evaluate import score, stats
import collections, csv, statistics, numpy as np
sys.path.insert(0, str(ROOT / 'scripts/timing'))
from separator_registry import MODELS

folder = ROOT / 'results/separation-alignment'
refs = {s['id']: s for s in read(OUT / 'references.json')}
groups = collections.defaultdict(list); by_song = []
paths = {p.with_suffix('') if p.suffix == '.gz' else p for p in (folder / 'predictions').rglob('*.json*')}
for path in sorted(paths):
    r = read(path); rows, diagnostics = score(refs[r['song']], r)
    for group in ('all', 'japanese', 'latin'):
        selected = [x for x in rows if group == 'all' or x['language'] == group]
        item = {k: r[k] for k in ('experiment', 'separator', 'persistence', 'mode', 'kind', 'song')}
        item.update(group=group, **stats(selected))
        by_song.append(item)
        if r['song'] != 's13':
            groups[(r['experiment'], group)].append((item, selected))
aggregate = []
for (exp, group), pairs in groups.items():
    pooled = sum([rows for _, rows in pairs], [])
    row = {**pairs[0][0], 'song': 'ALL', **stats(pooled)}
    row['songs'] = len(pairs)
    row['macro100_pct'] = float(np.mean([x['hit100_pct'] for x, _ in pairs if x['n']]))
    aggregate.append(row)
dump(folder / 'metrics.json', {'aggregate': aggregate, 'by_song': by_song})
print('Scored separator conditions', len(paths))
with (folder / 'metrics.csv').open('w') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(aggregate[0]))
    writer.writeheader(); writer.writerows(aggregate)

res_dir = ROOT / 'results/separation-resources'
if all((res_dir / (name + ('-cpu' if dev == 'cpu' else '') + '.json')).exists() for name in MODELS for dev in ('cuda', 'cpu')):
    export = []
    for name in MODELS:
        for device in ('cuda', 'cpu'):
            data = read(res_dir / f"{name}{'-cpu' if device == 'cpu' else ''}.json")
            total = sum(statistics.median(r['seconds'] for r in data['records'] if r['song'] == s['id']) for s in data['inputs'])
            export.append({
                'model': name,
                'device': device,
                'seconds': total,
                'rss_bytes': max(r['rss_bytes'] for r in data['records']),
                'allocated_bytes': max((r['allocated_bytes'] for r in data['records'] if r['allocated_bytes'] is not None), default=None),
                'process_gpu_bytes': max((r.get('process_gpu_bytes') for r in data['records'] if r.get('process_gpu_bytes') is not None), default=None),
                'board_energy_joules': sum(statistics.median(r['board_energy_joules'] for r in data['records'] if r['song'] == song['id']) for song in data['inputs']) if device == 'cuda' else None,
                'input_scope': 'rainbow-30-60' if device == 'cpu' else 'five-full-songs',
                'runs': len(data['records']),
            })
    with (res_dir / 'summary.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(export[0]))
        writer.writeheader(); writer.writerows(export)
    dump(res_dir / 'summary.json', export)
