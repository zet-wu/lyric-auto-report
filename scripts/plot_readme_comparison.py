"""Plot the G1/G2/G3 comparison figures from frozen metrics."""
from pathlib import Path
import argparse, json, os
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--group', choices=['G1', 'G2', 'G3'], default='G1')
args = parser.parse_args()
out = ROOT / 'results/figures'
out.mkdir(parents=True, exist_ok=True)
source = ROOT / 'results/comparison/scores' / ('reading-summary.json' if args.group == 'G3' else 'summary.json')
data = json.loads(source.read_text())[args.group]
stem = args.group.lower() + '-comparison'
labels = {
    'studio-nextfire': 'Lazulite Studio\nNextFire',
    'studio-mms-fa': 'Lazulite Studio\nMMS_FA + smart extension',
    'milikara': 'MiliKara\nNextFire',
    'timing': 'Timing\nBS Karaoke + TIFA',
    'sug-nextfire': 'StrangeUtaGame\nNextFire',
    'sug-mms-fa': 'StrangeUtaGame\nMMS_FA',
    'yohane': 'yohane\nNextFire',
    'fa-kara': 'FA-Kara\nMMS_FA',
}
labels = {k: v for k, v in labels.items() if k in data}
panels = [
    ('双端命中率', ['hit100_pct', 'hit200_pct'], ['100 ms', '200 ms'], 'Percent (higher is better)', [0, 25, 50, 75, 100], 108),
    ('平均绝对误差', ['start_mae_ms', 'end_mae_ms'], ['Start', 'End'], 'ms (lower is better)', [0, 100, 200, 300], 315),
    ('绝对误差 P95', ['start_p95_ms', 'end_p95_ms'], ['Start', 'End'], 'ms (lower is better)', [0, 300, 600, 900], 930),
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
fig.subplots_adjust(left=.235, right=.98, bottom=11 / height_mm, top=1 - 14.3 / height_mm, wspace=.25)
colors = ['#4477AA', '#B9CBE0']
y = np.arange(len(labels))
for i, (ax, (title, keys, legend, xlabel, ticks, xmax)) in enumerate(zip(axes, panels)):
    ax.set_title(title, fontsize=7, pad=25, fontfamily=['Droid Sans Fallback', 'DejaVu Sans'])
    for j, key in enumerate(keys):
        vals = np.array([data[k]['overall'][key] for k in labels])
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
fig.savefig(out / (stem + '.svg'))
svg_path = out / (stem + '.svg')
svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines()) + '\n')
fig.savefig(out / (stem + '.pdf'))
fig.savefig(out / (stem + '.png'), dpi=600)
plt.close(fig)
print(f'Exported {stem} ({len(labels)} routes)')
