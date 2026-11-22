"""Sample-exact, discontinuity-aware concatenation mapping; no reference inputs."""
import math
import numpy as np

RATE = 16000

def make_map(segments, length, padded=False):
    intervals = []
    for s in segments:
        a = max(0, math.floor(s['start' if padded else 'core_start'] * RATE))
        b = min(length, math.ceil(s['end' if padded else 'core_end'] * RATE))
        if b > a:
            intervals.append((a, b))
    merged = []
    for a, b in sorted(intervals):
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    offset = 0; result = []
    for a, b in merged:
        result.append({'source_start': a, 'source_end': b, 'concat_start': offset, 'concat_end': offset + b - a})
        offset += b - a
    assert result
    return result

def concatenate(y, mapping):
    result = np.concatenate([y[p['source_start']:p['source_end']] for p in mapping])
    assert len(result) == mapping[-1]['concat_end']
    return result

def map_unit(unit, mapping):
    a = unit['start'] * RATE; b = unit['end'] * RATE
    assert 0 <= a < b <= mapping[-1]['concat_end'] + 1e-5
    fragments = []
    for p in mapping:
        lo = max(a, p['concat_start']); hi = min(b, p['concat_end'])
        if hi > lo + 1e-6:
            fragments.append({
                'start': (p['source_start'] + lo - p['concat_start']) / RATE,
                'end': (p['source_start'] + hi - p['concat_start']) / RATE,
            })
    assert fragments
    return {
        **unit,
        'concat_start': unit['start'],
        'concat_end': unit['end'],
        'start': fragments[0]['start'],
        'end': fragments[-1]['end'],
        'fragments': fragments,
        'crosses_removed_gap': len(fragments) > 1,
        'removed_gap_seconds': sum(y['start'] - x['end'] for x, y in zip(fragments, fragments[1:])),
    }
