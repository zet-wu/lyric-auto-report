"""Plot the eight G1 routes from frozen common-text-boundary metrics.

Quantitative grid: threshold coverage, mean timing error, then tail error.
All eight routes and all six requested metrics are retained. Bars are pooled
observed metrics, not estimates across repeated runs; no uncertainty is invented.
Nature-figure QA tools can be supplied with --audit-tools for rendered checks.
"""
from pathlib import Path
import argparse, csv, hashlib, json, os, sys
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--audit-tools', type=Path)
args = parser.parse_args()
out = ROOT/'results/figures'
out.mkdir(parents=True, exist_ok=True)
source = ROOT/'results/comparison/scores/summary.json'
data = json.loads(source.read_text())['G1']
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
assert set(data) == set(labels)
assert all(data[k]['overall']['n'] == 4249 for k in labels)
# Each column has a distinct role: coverage, typical error, tail error.
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
fig, axes = plt.subplots(1, 3, figsize=(183/25.4, 110/25.4), sharey=True)
fig.subplots_adjust(left=.235, right=.98, bottom=.10, top=.87, wspace=.25)
colors = ['#4477AA', '#B9CBE0']
y = np.arange(len(labels))
records=[]
for i, (ax, (title, keys, legend, xlabel, ticks, xmax)) in enumerate(zip(axes, panels)):
    ax.set_title(title, fontsize=7, pad=25, fontfamily=['Droid Sans Fallback', 'DejaVu Sans'])
    for j, key in enumerate(keys):
        vals=np.array([data[k]['overall'][key] for k in labels])
        assert np.isfinite(vals).all()
        best=vals.max() if i==0 else vals.min()
        winners=np.isclose(vals,best,rtol=0,atol=1e-9)
        centers=y + (-.19 if j==0 else .19)
        ax.barh(centers, vals, height=.32, color=colors[j], label=legend[j], zorder=3)
        for route, value, center, winner in zip(labels,vals,centers,winners):
            records.append({'route':route,'metric':key,'value':float(value),'best':bool(winner)})
            if winner:
                ax.text(value+xmax*.025, center, '*', va='center', ha='left', fontsize=10, weight='bold', color='#222222', zorder=4)
    ax.set_xlim(0,xmax);ax.set_xticks(ticks);ax.set_xlabel(xlabel,labelpad=7)
    ax.set_yticks(y, list(labels.values()))
    ax.tick_params(axis='y', length=0, pad=8)
    ax.tick_params(axis='x', length=3, color='#888888')
    ax.set_axisbelow(True)
    ax.legend(loc='lower left',bbox_to_anchor=(0,1.005),ncols=2,fontsize=6.5,
              handlelength=1.1,columnspacing=1.1,borderaxespad=0)
axes[0].set_ylim(len(labels)-.5,-.5)
fig.canvas.draw()
if args.audit_tools:
    sys.path.insert(0,str(args.audit_tools.resolve()))
    from audit_panel_alignment import require_matplotlib_panel_alignment
    require_matplotlib_panel_alignment(fig,json_out=out/'g1-comparison.alignment.json',
        tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=True)
fig.savefig(out/'g1-comparison.svg')
fig.savefig(out/'g1-comparison.pdf')
fig.savefig(out/'g1-comparison.png',dpi=600)
plt.close(fig)
with (out/'g1-comparison.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=['route','metric','value','best']);writer.writeheader();writer.writerows(records)
(out/'g1-comparison.provenance.json').write_text(json.dumps({
    'source':'results/comparison/scores/summary.json','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'group':'G1','boundary':'common text','songs':12,'units_per_route':4249,
    'routes':8,'metrics':6,'rows':len(records),'excluded_routes':[],
    'stars':'Unrounded maximum hit rate or minimum error; absolute tie tolerance 1e-9.',
    'uncertainty':'Pooled descriptive metrics from one fixed experiment; no repeat-based intervals.',
    'design':'Quantitative grid: coverage, mean error, tail error. White background; consistent paired blue palette.',
    'backend':'Python / Matplotlib','size_mm':[183,110],
},ensure_ascii=False,indent=2)+'\n')
print('Exported 8 routes x 6 metrics; best markers:',[(r['route'],r['metric']) for r in records if r['best']])
