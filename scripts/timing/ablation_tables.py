"""Render the ablation heatmap figure from completed matrix metrics."""
from ablation_common import *
import os
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.hashsalt'] = 'lyric-auto-report'
import matplotlib.pyplot as plt
import numpy as np

m = read(OUT / 'metrics.json')
primary = {(r['separator'], r['backend'], r['strategy'], r['subset']): r for r in m['aggregate'] if r['cohort'] == 'primary'}
strategies = ['concat', 'padded', 'full', 'auto_mms', 'auto_nf', 'human']
labels = ['Core concat', 'Padded concat', 'Full stem', 'MMS windows', 'NextFire windows', 'Human windows']
seps = ['demucs', 'bs', 'kim']
fig, axes = plt.subplots(1, 3, figsize=(16, 6), layout='constrained')
for ax, backend in zip(axes, ['nextfire', 'tifa', 'mms_fa']):
    values = np.array([[primary[(sep, backend, st, 'all')]['macro100'] * 100 for sep in seps] for st in strategies])
    im = ax.imshow(values, vmin=0, vmax=100, cmap='viridis', aspect='auto')
    ax.set_xticks(range(3), ['Demucs', 'BS Karaoke', 'Kim'])
    ax.set_yticks(range(len(strategies)), labels)
    ax.set_title(backend.upper())
    for i in range(len(strategies)):
        for j in range(3):
            ax.text(j, i, f'{values[i, j]:.2f}%', ha='center', va='center', color='black' if values[i, j] > 65 else 'white')
fig.colorbar(im, ax=axes, shrink=.75, label='Both endpoints within 100 ms (%)')
fig.suptitle('12 songs, equal song weights; fixed readings; failures retained\nHuman windows are a diagnostic condition, not an automatic pipeline')
fig.savefig(OUT / 'matrix.png', dpi=170)
fig.savefig(OUT / 'matrix.svg', metadata={'Date': None})
plt.close(fig)
svg = OUT / 'matrix.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
print('rendered matrix figure')
