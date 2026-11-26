"""Plot the G1/G2/G3 comparison figures from Phase 2 M1 frozen metrics and predictions."""
from pathlib import Path
from collections import defaultdict
import argparse, json, math, os, re, sys, unicodedata
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/comparison'))
from shared import read, exists
import sug_saved
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def norm(s): return ''.join(c for c in unicodedata.normalize('NFKC', s).lower() if c.isalnum() or c == 'ー')
def valid(a, b): return isinstance(a, (int, float)) and isinstance(b, (int, float)) and math.isfinite(a + b) and 0 <= a < b
def kana(text):
    text = unicodedata.normalize('NFKC', text).lower()
    return ''.join(chr(ord(c) - 96) if 'ァ' <= c <= 'ヶ' else c for c in text if c.isalnum() or c == 'ー')
def primary_ja(text):
    clean = ''.join(char for char in unicodedata.normalize('NFKC', text) if char.isalnum() or char in "ー'’")
    return bool(re.fullmatch('[ぁ-ゖァ-ヺー]+', clean))
def row(text, a, b, scale=1): return {'text': text, 'start': a / scale if a is not None else None, 'end': b / scale if b is not None else None}
def segment(text, units, a=None, b=None): return {'text': text, 'units': units, 'start': a, 'end': b}
def envelope(parts):
    if not parts or any(not valid(x['start'], x['end']) for x in parts): return None, None
    return min(x['start'] for x in parts), max(x['end'] for x in parts)
def positioned(parts, expected):
    out = []; pos = 0
    for w in parts:
        text = norm(w['text'])
        if not text: continue
        out.append({**w, 'a': pos, 'b': pos + len(text)}); pos += len(text)
    assert ''.join(norm(w['text']) for w in parts) == norm(expected), (expected, ''.join(w['text'] for w in parts))
    return out
def span(timing):
    a, b = timing.get('start'), timing.get('end')
    return (a['time'], b['time']) if a and b and valid(a['time'], b['time']) else (None, None)
def unique_boundaries(a, b):
    n, m = len(a), len(b)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): f[i][0] = i
    for j in range(m + 1): f[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1): f[i][j] = min(f[i - 1][j] + 1, f[i][j - 1] + 1, f[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    z = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): z[i][m] = n - i
    for j in range(m + 1): z[n][j] = m - j
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1): z[i][j] = min(z[i + 1][j] + 1, z[i][j + 1] + 1, z[i + 1][j + 1] + (a[i] != b[j]))
    mapping = {}
    for i in range(n + 1):
        js = [j for j in range(m + 1) if f[i][j] + z[i][j] == f[n][m]]
        if len(js) == 1: mapping[i] = js[0]
    mapping[0] = 0; mapping[n] = m
    return mapping


def load_g3_reading_metrics(route_keys):
    refs = {s['id']: s for s in read(ROOT / 'results/timing/reference.json')}
    ja_ids = read(ROOT / 'configs/phase2.json')['dataset']['ja']
    out_data = {}
    for cond in route_keys:
        all_rows = []
        for sid in ja_ids:
            song = refs[sid]
            pred = None
            if 'studio-' in cond:
                path = ROOT / f'results/M1/predictions/{cond}/{sid}.json.gz'
                r = read(path)
                if r.get('status') == 'ok' and 'projection' in r:
                    times = r.get('object_timings', {})
                    mapping = {entry['unit_id']: entry for entry in r['projection']['mapping']}
                    out_lines = {}
                    for line in r['projection']['request']['lines']:
                        groups = defaultdict(list)
                        for unit in line['units']: groups[tuple(unit['source_range'])].append(unit)
                        parts = []
                        for (a, b), units in sorted(groups.items()):
                            us = [row(u['reading'], *span(times.get(mapping[u['unit_id']]['object_id'], {})), 1) for u in units]
                            parts.append(segment(line['text'][a:b], us, *envelope(us)))
                        out_lines[line['line_id']] = parts
                    pred = [out_lines.get(l['id'], []) for l in song['lines']]
            else:
                tool = cond.split('-', 1)[1]
                model = ''
                if tool == 'sug-mms-fa':
                    tool = 'sug'
                    model = '-mms-fa'
                elif tool == 'sug':
                    model = '-nextfire'
                path = ROOT / f'results/comparison/{"milikara/runs" if tool == "milikara" else tool}/{sid}-{tool}{model}-auto.json.gz'
                if exists(path):
                    r = read(path)
                    if r.get('status') == 'ok':
                        if tool == 'sug': pred = sug_saved.saved_segments(r)
                        elif tool == 'milikara':
                            ex = r['export']; times = {x['unit_id']: x for x in ex['units']}; pred = []
                            for l in ex['lyrics']['lines']:
                                if not l['sing']: continue
                                pred.append([segment(w['surface'], [row(u['reading'], times.get(u['id'], {}).get('start_ms'), times.get(u['id'], {}).get('end_ms'), 1000) for u in w['units']]) for w in l['segments']])
            for li, line in enumerate(song['lines']):
                rows = {u['id']: {'start': u['start'], 'end': u['end'], 'valid': False, 'ds': None, 'de': None} for u in line['leaves'] if primary_ja(u['text']) and valid(u['start'], u['end'])}
                if pred is None: all_rows.extend(rows.values()); continue
                gold = positioned(line['words'], line['text']); parts = positioned(pred[li], line['text'])
                edges = sorted({0, *[w['b'] for w in gold]} & {0, *[p['b'] for p in parts]})
                for left, right in zip(edges, edges[1:]):
                    gw = [w for w in gold if left <= w['a'] and w['b'] <= right]; pw = [p for p in parts if left <= p['a'] and p['b'] <= right]
                    gids = {w['id'] for w in gw}; gu = [u for u in line['leaves'] if u['word_id'] in gids and kana(u['text'])]
                    native_units = []; opaque = False
                    for p in pw:
                        us = p['units']
                        if not us:
                            cov = [w for w in gw if p['a'] <= w['a'] and w['b'] <= p['b']]
                            if cov and cov[0]['a'] == p['a'] and cov[-1]['b'] == p['b']:
                                ids = {w['id'] for w in cov}; us = [row(''.join(u['text'] for u in gu if u['word_id'] in ids), p['start'], p['end'])]
                            elif norm(p['text']): opaque = True
                        native_units.extend(us)
                    if opaque: native_units = [row(''.join(u['text'] for u in gu), *envelope(pw))]
                    pu = []; pos = 0
                    for u in native_units:
                        rd = kana(u['text'])
                        if rd: pu.append({**u, 'a': pos, 'b': pos + len(rd)}); pos += len(rd)
                    ga = []; pos = 0
                    for u in gu:
                        rd = kana(u['text'])
                        if rd: ga.append({**u, 'a': pos, 'b': pos + len(rd), 'normalized': rd}); pos += len(rd)
                    gs = ''.join(u['normalized'] for u in ga)
                    if len(pu) == 1 and gs: pu = [{**pu[0], 'text': gs, 'a': 0, 'b': len(gs)}]
                    ps = ''.join(kana(u['text']) for u in pu)
                    if not gs or not ps: continue
                    mapping = unique_boundaries(gs, ps); pe = {0, *[u['b'] for u in pu]}
                    for u in ga:
                        if u['id'] not in rows: continue
                        a, b = mapping.get(u['a']), mapping.get(u['b'])
                        if a is None or b is None or b <= a or a not in pe or b not in pe: continue
                        us = [p for p in pu if a <= p['a'] and p['b'] <= b]; x, y = envelope(us)
                        ok = bool(us) and us[0]['a'] == a and us[-1]['b'] == b and valid(x, y)
                        if ok: rows[u['id']].update(valid=True, ds=x - u['start'], de=y - u['end'])
                all_rows.extend(rows.values())
        good = [x for x in all_rows if x['valid']]; n = len(all_rows)
        a = np.array([abs(x['ds']) * 1000 for x in good]); b = np.array([abs(x['de']) * 1000 for x in good])
        h100 = sum(max(abs(x['ds']), abs(x['de'])) <= .100000001 for x in good)
        h200 = sum(max(abs(x['ds']), abs(x['de'])) <= .200000001 for x in good)
        out_data[cond] = {
            'hit100_pct': 100 * h100 / n, 'hit200_pct': 100 * h200 / n,
            'start_mae_ms': float(a.mean()), 'end_mae_ms': float(b.mean()),
            'start_p95_ms': float(np.percentile(a, 95)), 'end_p95_ms': float(np.percentile(b, 95)),
        }
    return out_data


parser = argparse.ArgumentParser()
parser.add_argument('--group', choices=['G1', 'G2', 'G3'], default='G1')
args = parser.parse_args()
out = ROOT / 'results/figures'
out.mkdir(parents=True, exist_ok=True)
source = ROOT / 'results/M1/summary.json'
summary = json.loads(source.read_text())
stem = args.group.lower() + '-comparison'
labels = {
    'studio-bs-nextfire': 'Lazulite Studio\nBS Karaoke + NextFire',
    'studio-demucs-nextfire': 'Lazulite Studio\nDemucs + NextFire',
    'studio-demucs-mms_fa-smart': 'Lazulite Studio\nBS Karaoke + MMS_FA + smart ext.' if args.group == 'G2' else 'Lazulite Studio\nDemucs + MMS_FA + smart ext.',
    'fa-kara': 'FA-Kara\nBS Karaoke + MMS_FA',
    'sug': 'StrangeUtaGame\nBS Karaoke + NextFire' if args.group == 'G2' else 'StrangeUtaGame\nMDX-Net + NextFire',
    'sug-mms-fa': 'StrangeUtaGame\nBS Karaoke + MMS_FA' if args.group == 'G2' else 'StrangeUtaGame\nMDX-Net + MMS_FA',
    'yohane': 'yohane\nBS Karaoke + NextFire' if args.group == 'G2' else 'yohane\nHybridDemucs + NextFire',
    'milikara': 'MiliKara\nBS Karaoke + NextFire' if args.group == 'G2' else 'MiliKara\nMelBand + NextFire',
    'timing': 'Timing\nBS Karaoke + TIFA',
}
if args.group == 'G2':
    labels.pop('studio-demucs-nextfire', None)
if args.group == 'G3':
    for excluded in ('fa-kara', 'timing', 'yohane'):
        labels.pop(excluded, None)
    labels = {f'{args.group}-{k}': v for k, v in labels.items()}
    data = load_g3_reading_metrics(list(labels.keys()))
else:
    data = {
        row['condition']: row
        for row in summary['surface']
        if row['song'] == 'ALL' and row['scope'] == 'all' and row['condition'].startswith(args.group + '-')
    }
    labels = {f'{args.group}-{k}': v for k, v in labels.items() if f'{args.group}-{k}' in data}

panels = [
    ('a', '双端命中率', ['hit100_pct', 'hit200_pct'], ['100 ms', '200 ms'], 'Percent (higher is better)', [0, 25, 50, 75, 100], 108),
    ('b', '平均绝对误差', ['start_mae_ms', 'end_mae_ms'], ['Start', 'End'], 'ms (lower is better)', [0, 100, 200, 300], 315),
    ('c', '绝对误差 P95', ['start_p95_ms', 'end_p95_ms'], ['Start', 'End'], 'ms (lower is better)', [0, 300, 600, 900], 900),
]
plt.rcParams.update({
    'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans', 'Droid Sans Fallback'],
    'font.size': 6.5, 'axes.labelsize': 6.5, 'xtick.labelsize': 6.5,
    'ytick.labelsize': 6.5, 'axes.linewidth': 0.6,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.spines.left': False, 'legend.frameon': False,
    'pdf.fonttype': 42, 'svg.fonttype': 'none',
    'savefig.facecolor': 'white',
})
height_mm = 110 * (.23 + .77 * len(labels) / 8)
fig, axes = plt.subplots(1, 3, figsize=(183 / 25.4, height_mm / 25.4), sharey=True)
fig.subplots_adjust(left=.255, right=.98, bottom=11 / height_mm, top=1 - 14.3 / height_mm, wspace=.24)
colors = ['#4477AA', '#B9CBE0']
y = np.arange(len(labels))
from matplotlib.transforms import ScaledTranslation
for i, (ax, (p_label, title, keys, legend, xlabel, ticks, xmax)) in enumerate(zip(axes, panels)):
    offset = ScaledTranslation(-6 / 72, 22 / 72, fig.dpi_scale_trans)
    ax.text(0, 1, p_label, transform=ax.transAxes + offset, fontsize=8, fontweight='bold', va='bottom', ha='left')
    ax.set_title(title, fontsize=7, pad=22, fontfamily=['Droid Sans Fallback', 'DejaVu Sans'])
    for j, key in enumerate(keys):
        vals = np.array([data[k][key] for k in labels], dtype=float)
        best = vals.max() if i == 0 else vals.min()
        winners = np.isclose(vals, best, rtol=0, atol=1e-9)
        centers = y + (-.19 if j == 0 else .19)
        ax.barh(centers, vals, height=.32, color=colors[j], label=legend[j], zorder=3)
        for route, value, center, winner in zip(labels, vals, centers, winners):
            if winner:
                ax.text(value + xmax * .025, center, '*', va='center', ha='left', fontsize=10, weight='bold', color='#222222', zorder=4)
    ax.set_xlim(0, xmax); ax.set_xticks(ticks); ax.set_xlabel(xlabel, labelpad=7)
    ax.set_yticks(y, list(labels.values()))
    ax.tick_params(axis='y', length=0, pad=8)
    ax.tick_params(axis='x', length=3, color='#888888')
    ax.set_axisbelow(True)
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.005), ncols=2, fontsize=6.5, handlelength=1.1, columnspacing=1.1, borderaxespad=0)
axes[0].set_ylim(len(labels) - .5, -.5)
fig.canvas.draw()
width_pt, height_pt = (float(v) * 72 for v in fig.get_size_inches())
top_spread = max(ax.get_position().y1 * height_pt for ax in axes) - min(ax.get_position().y1 * height_pt for ax in axes)
bottom_spread = max(ax.get_position().y0 * height_pt for ax in axes) - min(ax.get_position().y0 * height_pt for ax in axes)
width_spread = max((ax.get_position().x1 - ax.get_position().x0) * width_pt for ax in axes) - min((ax.get_position().x1 - ax.get_position().x0) * width_pt for ax in axes)
assert max(top_spread, bottom_spread, width_spread) <= 1.5, (top_spread, bottom_spread, width_spread)  # audit_layout_manifest(row_alignment)
fig.savefig(out / (stem + '.svg'))
svg_path = out / (stem + '.svg')
svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines()) + '\n')
fig.savefig(out / (stem + '.pdf'))
(out / (stem + '.pdf')).unlink(missing_ok=True)
fig.savefig(out / (stem + '.png'), dpi=600)
plt.close(fig)
print(f'Exported {stem} ({len(labels)} routes)')
