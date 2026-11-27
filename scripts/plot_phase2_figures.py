"""Generate Phase 2 thematic figures (M2 multilingual, M3 AAC persistence, M4 tempo correlation, M7 MiliKara ablation, M8 cross-model refinement, M10 agent MCP refinement)."""
from pathlib import Path
import argparse, json, os
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation
import numpy as np

OUT = ROOT / 'results/figures'
OUT.mkdir(parents=True, exist_ok=True)
CJK_FONT = ['Droid Sans Fallback', 'DejaVu Sans']

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Droid Sans Fallback'],
    'font.size': 6.5,
    'axes.labelsize': 6.5,
    'xtick.labelsize': 6.5,
    'ytick.labelsize': 6.5,
    'axes.linewidth': 0.6,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'legend.frameon': False,
    'pdf.fonttype': 42,
    'svg.fonttype': 'none',
    'savefig.facecolor': 'white',
})


def add_panel_label(ax, label, x_pt=-10, y_pt=22):
    offset = ScaledTranslation(x_pt / 72, y_pt / 72, ax.figure.dpi_scale_trans)
    ax.text(0, 1, label, transform=ax.transAxes + offset, fontsize=8, fontweight='bold', va='bottom', ha='left')


def save_fig(fig, stem):
    fig.canvas.draw()
    width_pt, height_pt = (float(v) * 72 for v in fig.get_size_inches())
    axes = [ax for ax in fig.axes if ax.get_visible()]
    top_spread = max(ax.get_position().y1 * height_pt for ax in axes) - min(ax.get_position().y1 * height_pt for ax in axes)
    bottom_spread = max(ax.get_position().y0 * height_pt for ax in axes) - min(ax.get_position().y0 * height_pt for ax in axes)
    width_spread = max((ax.get_position().x1 - ax.get_position().x0) * width_pt for ax in axes) - min((ax.get_position().x1 - ax.get_position().x0) * width_pt for ax in axes)
    assert max(top_spread, bottom_spread, width_spread) <= 1.5, (top_spread, bottom_spread, width_spread)  # audit_layout_manifest(row_alignment)
    svg_path = OUT / f'{stem}.svg'
    fig.savefig(svg_path)
    svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines()) + '\n')
    fig.savefig(OUT / f'{stem}.pdf')
    (OUT / f'{stem}.pdf').unlink(missing_ok=True)
    fig.savefig(OUT / f'{stem}.png', dpi=600)
    plt.close(fig)
    print(f'Exported {stem}.svg and {stem}.png')


def plot_multilingual():
    m2 = json.loads((ROOT / 'results/M2/summary.json').read_text())
    pg = json.loads((ROOT / 'results/M2/phonetic-groups.json').read_text())['metrics']
    pg_map = {(r['condition'], r['phonetic_group']): r for r in pg}
    surf_map = {(r['condition'], r['song'], r['scope']): r for r in m2['surface']}

    fig, axes = plt.subplots(1, 2, figsize=(183 / 25.4, 76 / 25.4))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.19, top=0.77, wspace=0.20)

    conds = [
        ('bs-mms-fa', 'Studio BS + MMS_FA + smart ext.', '#0F4D92'),
        ('demucs-mms-fa', 'Studio Demucs + MMS_FA + smart ext.', '#42949E'),
        ('bs-nextfire', 'Studio BS + NextFire', '#B64342'),
        ('demucs-nextfire', 'Studio Demucs + NextFire', '#E9A6A1'),
    ]

    ax = axes[0]
    add_panel_label(ax, 'a', x_pt=-12, y_pt=23)
    ax.set_title('非日语不同音节类型的双端 100 ms 命中率', fontsize=7, pad=23, fontfamily=CJK_FONT)
    groups = [
        ('open_cv', '开音节\nOpen CV'),
        ('nasal_coda', '鼻音韵尾\nNasal coda'),
        ('stop_coda', '入声塞音尾\nStop coda'),
        ('non_ja_phoneme', '日语缺失音素\nNon-JA'),
    ]
    x = np.arange(len(groups))
    w = 0.19
    for idx, (ckey, clabel, color) in enumerate(conds):
        vals = [pg_map[(ckey, gkey)]['hit100_pct'] for gkey, _ in groups]
        offset = (idx - 1.5) * w
        ax.bar(x + offset, vals, width=w * 0.92, color=color, label=clabel, zorder=3)
    ax.set_xticks(x, [glabel for _, glabel in groups], fontfamily=CJK_FONT, fontsize=6.0)
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel('Joint 100 ms hit rate (%)')
    ax.tick_params(axis='x', length=0, pad=5)
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.6, handlelength=1.1, columnspacing=0.8, borderaxespad=0)

    ax = axes[1]
    add_panel_label(ax, 'b', x_pt=-12, y_pt=23)
    ax.set_title('跨语种曲目与分段双端 100 ms 命中率 (Demucs 组)', fontsize=7, pad=23, fontfamily=CJK_FONT)
    conds_b = [
        ('demucs-mms-fa', 'Studio Demucs + MMS_FA + smart ext.', '#42949E'),
        ('demucs-sug-mms-fa', 'SUG Demucs + MMS_FA', '#8BCF8B'),
        ('demucs-nextfire', 'Studio Demucs + NextFire', '#B64342'),
        ('demucs-sug', 'SUG Demucs + NextFire', '#E9A6A1'),
    ]
    slices = [
        ('m01', 'all', 'm01\n国语'),
        ('m02', 'all', 'm02\n国语'),
        ('y01', 'spoken', 'y01\n口白'),
        ('y01', 'sung', 'y01\n歌唱'),
        ('y02', 'all', 'y02\n粤语'),
        ('jy01', 'ja', 'jy01\n日语'),
        ('jy01', 'yue', 'jy01\n粤语'),
        ('t01', 'all', 't01\n潮州'),
    ]
    x2 = np.arange(len(slices))
    for idx, (ckey, clabel, color) in enumerate(conds_b):
        vals = [surf_map[(ckey, sid, sc)]['hit100_pct'] for sid, sc, _ in slices]
        offset = (idx - 1.5) * w
        ax.bar(x2 + offset, vals, width=w * 0.92, color=color, label=clabel, zorder=3)
    ax.set_xticks(x2, [slabel for _, _, slabel in slices], fontfamily=CJK_FONT, fontsize=5.8)
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel('Joint 100 ms hit rate (%)')
    ax.tick_params(axis='x', length=0, pad=5)
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.6, handlelength=1.1, columnspacing=0.8, borderaxespad=0)

    save_fig(fig, 'm2-multilingual-phonetics')


def plot_aac():
    m3 = json.loads((ROOT / 'results/M3/summary.json').read_text())
    cohorts = {(r['condition'], r['cohort']): r for r in m3['cohorts']}
    cb = json.loads((ROOT / 'results/M3/core-boundaries.json').read_text())['songs']

    fig, axes = plt.subplots(1, 2, figsize=(183 / 25.4, 72 / 25.4))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.19, top=0.77, wspace=0.20)

    ax = axes[0]
    add_panel_label(ax, 'a', x_pt=-12, y_pt=23)
    ax.set_title('无损浮点 WAV vs 192 kbps AAC-LC M4A 下游对齐命中率', fontsize=7, pad=23, fontfamily=CJK_FONT)
    categories = [
        ('demucs', 'nextfire', 'ja', 'JA (20)\nDemucs\nNextFire'),
        ('bs', 'nextfire', 'ja', 'JA (20)\nBS Karaoke\nNextFire'),
        ('demucs', 'mms-fa', 'ja', 'JA (20)\nDemucs\nMMS_FA'),
        ('bs', 'mms-fa', 'ja', 'JA (20)\nBS Karaoke\nMMS_FA'),
        ('demucs', 'mms-fa', 'non_ja', 'Non-JA (6)\nDemucs\nMMS_FA'),
        ('bs', 'mms-fa', 'non_ja', 'Non-JA (6)\nBS Karaoke\nMMS_FA'),
    ]
    x = np.arange(len(categories))
    w = 0.34
    float_vals = [cohorts[(f'{sep}-float-{be}', coh)]['hit100_pct'] for sep, be, coh, _ in categories]
    aac_vals = [cohorts[(f'{sep}-aac-{be}', coh)]['hit100_pct'] for sep, be, coh, _ in categories]
    ax.bar(x - w / 2, float_vals, width=w * 0.92, color='#0F4D92', label='Float WAV (lossless)', zorder=3)
    ax.bar(x + w / 2, aac_vals, width=w * 0.92, color='#8BCF8B', label='AAC-LC 192 kbps M4A', zorder=3)
    for xi, fv, av in zip(x, float_vals, aac_vals):
        delta = av - fv
        sign = '+' if delta > 0 else ''
        ax.text(xi, max(fv, av) + 1.8, f'{sign}{delta:.2f}%', ha='center', va='bottom', fontsize=5.6, color='#272727')
    ax.set_xticks(x, [lbl for _, _, _, lbl in categories], fontsize=5.6)
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel('Joint 100 ms hit rate (%)')
    ax.tick_params(axis='x', length=0, pad=5)
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.8, handlelength=1.1, columnspacing=1.0, borderaxespad=0)

    ax = axes[1]
    add_panel_label(ax, 'b', x_pt=-12, y_pt=23)
    ax.set_title('26 首歌曲人声活跃片段边界平均偏移分布', fontsize=7, pad=23, fontfamily=CJK_FONT)
    groups_cb = [
        ('BS Karaoke\nStart shift', [r['core_start_mean_abs_ms'] for r in cb if r['separator'] == 'bs'], '#0F4D92'),
        ('BS Karaoke\nEnd shift', [r['core_end_mean_abs_ms'] for r in cb if r['separator'] == 'bs'], '#3775BA'),
        ('Demucs\nStart shift', [r['core_start_mean_abs_ms'] for r in cb if r['separator'] == 'demucs'], '#42949E'),
        ('Demucs\nEnd shift', [r['core_end_mean_abs_ms'] for r in cb if r['separator'] == 'demucs'], '#8BCF8B'),
    ]
    x2 = np.arange(len(groups_cb))
    for idx, (gname, vals, color) in enumerate(groups_cb):
        arr = np.array(vals, dtype=float)
        med = float(np.median(arr))
        q25, q75 = float(np.percentile(arr, 25)), float(np.percentile(arr, 75))
        jitter = np.linspace(-0.14, 0.14, len(arr))
        order = np.argsort(arr)
        ax.scatter(np.full(len(arr), idx) + jitter, arr[order], s=14, color=color, alpha=0.75, edgecolors='none', zorder=3)
        ax.plot([idx - 0.22, idx + 0.22], [med, med], color='#272727', lw=1.6, zorder=4)
        ax.plot([idx, idx], [q25, q75], color='#272727', lw=1.2, zorder=4)
        ax.text(idx, max(arr) + 6, f'Med {med:.1f} ms', ha='center', va='bottom', fontsize=5.8, color='#272727')
    ax.set_xticks(x2, [g[0] for g in groups_cb], fontsize=6.0)
    ax.set_ylim(-5, 180)
    ax.set_yticks([0, 40, 80, 120, 160])
    ax.set_ylabel('Mean core boundary shift per song (ms)')
    ax.tick_params(axis='x', length=0, pad=5)
    ax.tick_params(axis='y', length=3, color='#888888')

    save_fig(fig, 'm3-aac-persistence')


def plot_tempo():
    m4 = json.loads((ROOT / 'results/M4/summary.json').read_text())
    bins = m4['duration_bins']
    bin_order = ['<120', '120-250', '250-500', '500-1000', '>1000']
    bin_names = ['<120 ms', '120-250 ms', '250-500 ms', '500-1,000 ms', '>1,000 ms']
    bin_labels = [f"{label}\n(n={next(row['n'] for row in bins if row['duration_bin_ms'] == key):,})" for label, key in zip(bin_names, bin_order)]
    bin_map = {(r['condition'], r['duration_bin_ms']): r for r in bins}

    fig, axes = plt.subplots(1, 2, figsize=(183 / 25.4, 72 / 25.4))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.19, top=0.77, wspace=0.20)

    conds = [
        ('bs-mms-fa', 'BS Karaoke + MMS_FA + smart ext.', '#0F4D92', '-'),
        ('demucs-mms-fa', 'Demucs + MMS_FA + smart ext.', '#42949E', '--'),
        ('bs-nextfire', 'BS Karaoke + NextFire', '#B64342', '-'),
        ('demucs-nextfire', 'Demucs + NextFire', '#E9A6A1', '--'),
    ]

    x = np.arange(len(bin_order))

    ax = axes[0]
    add_panel_label(ax, 'a', x_pt=-12, y_pt=23)
    ax.set_title('不同真实音节时长下的双端 100 ms 命中率', fontsize=7, pad=23, fontfamily=CJK_FONT)
    for ckey, clabel, color, ls in conds:
        vals = [bin_map[(ckey, b)]['hit100_pct'] for b in bin_order]
        ax.plot(x, vals, color=color, linestyle=ls, marker='o', markersize=4, lw=1.4, label=clabel, zorder=3)
    ax.set_xticks(x, bin_labels, fontsize=5.8)
    ax.set_ylim(40, 100)
    ax.set_yticks([40, 55, 70, 85, 100])
    ax.set_ylabel('Joint 100 ms hit rate (%)')
    ax.tick_params(axis='x', length=3, color='#888888')
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.8, handlelength=1.3, columnspacing=0.9, borderaxespad=0)

    ax = axes[1]
    add_panel_label(ax, 'b', x_pt=-12, y_pt=23)
    ax.set_title('不同音节时长下的起点与终点平均误差 (BS Karaoke)', fontsize=7, pad=23, fontfamily=CJK_FONT)
    mae_series = [
        ('bs-mms-fa', 'start_mae_ms', 'MMS_FA + smart ext. Start', '#0F4D92', '-', 'o'),
        ('bs-mms-fa', 'end_mae_ms', 'MMS_FA + smart ext. End', '#3775BA', '--', 's'),
        ('bs-nextfire', 'start_mae_ms', 'NextFire Start', '#B64342', '-', '^'),
        ('bs-nextfire', 'end_mae_ms', 'NextFire End', '#E9A6A1', '--', 'v'),
    ]
    for ckey, mkey, mlabel, color, ls, mk in mae_series:
        vals = [bin_map[(ckey, b)][mkey] for b in bin_order]
        ax.plot(x, vals, color=color, linestyle=ls, marker=mk, markersize=4, lw=1.4, label=mlabel, zorder=3)
    ax.set_xticks(x, bin_labels, fontsize=5.8)
    ax.set_ylim(0, 220)
    ax.set_yticks([0, 50, 100, 150, 200])
    ax.set_ylabel('Mean absolute error (ms)')
    ax.tick_params(axis='x', length=3, color='#888888')
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.8, handlelength=1.3, columnspacing=0.9, borderaxespad=0)

    save_fig(fig, 'm4-tempo-duration-bins')


def plot_milikara():
    m7 = json.loads((ROOT / 'results/M7/summary.json').read_text())['metrics']
    m7_map = {r['condition']: r for r in m7 if r['song'] == 'ALL' and r['scope'] == 'japanese'}

    fig, axes = plt.subplots(1, 2, figsize=(183 / 25.4, 74 / 25.4))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.19, top=0.77, wspace=0.20)

    soft_codes = ['soft-000', 'soft-001', 'soft-010', 'soft-011', 'soft-100', 'soft-101', 'soft-110', 'soft-111']
    x = np.arange(len(soft_codes))

    ax = axes[0]
    add_panel_label(ax, 'a', x_pt=-12, y_pt=23)
    ax.set_title('8 种停顿与静音软代价组合下的双端 100 ms 命中率', fontsize=7, pad=23, fontfamily=CJK_FONT)
    tracks = [
        ('bs_nextfire', 'BS Karaoke + NextFire', '#B64342', '-', 'o'),
        ('bs_mms_fa_smart', 'BS Karaoke + MMS_FA + smart ext.', '#0F4D92', '-', 's'),
        ('concat_core', 'Demucs + NextFire', '#E9A6A1', '--', '^'),
        ('demucs_mms_fa_smart', 'Demucs + MMS_FA + smart ext.', '#42949E', '--', 'v'),
    ]
    for prefix, label, color, ls, mk in tracks:
        vals = [m7_map[f'{prefix}/{sc}']['hit100_pct'] for sc in soft_codes]
        ax.plot(x, vals, color=color, linestyle=ls, marker=mk, markersize=4, lw=1.4, label=label, zorder=3)
    ax.set_xticks(x, [sc.replace('soft-', '') for sc in soft_codes], fontsize=6.0)
    ax.set_xlabel('Soft-cost bits (line_gap, rest_gap, rest_token)')
    ax.set_ylim(75, 90)
    ax.set_yticks([75, 80, 85, 90])
    ax.set_ylabel('Joint 100 ms hit rate (%)')
    ax.tick_params(axis='x', length=3, color='#888888')
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.8, handlelength=1.3, columnspacing=0.9, borderaxespad=0)

    ax = axes[1]
    add_panel_label(ax, 'b', x_pt=-12, y_pt=23)
    ax.set_title('解码开关对照：软代价全开、自由尾部与分隔符并入空白', fontsize=7, pad=23, fontfamily=CJK_FONT)
    groups = [
        ('bs_nextfire', 'BS\nNextFire', True),
        ('concat_core', 'Demucs\nNextFire', True),
        ('bs_mms_fa_smart', 'BS\nMMS_FA\n(延长)', False),
        ('demucs_mms_fa_smart', 'Demucs\nMMS_FA\n(延长)', False),
        ('bs_mms_fa_raw', 'BS\nMMS_FA\n(原始)', False),
        ('demucs_mms_fa_raw', 'Demucs\nMMS_FA\n(原始)', False),
    ]
    x2 = np.arange(len(groups))
    w = 0.19
    bars_cfg = [
        ('soft-000', 'Standard CTC (soft-000)', '#0F4D92'),
        ('soft-111', 'All soft costs (soft-111)', '#42949E'),
        ('free_tail', 'Free tail (+free_tail)', '#8BCF8B'),
        ('delimiter', 'Merge delimiter (+delimiter)', '#B64342'),
    ]
    for idx, (ckey, clabel, color) in enumerate(bars_cfg):
        xs, vals = [], []
        for g_idx, (prefix, _, has_delim) in enumerate(groups):
            if ckey == 'delimiter' and not has_delim:
                continue
            xs.append(g_idx + (idx - 1.5 if has_delim else idx - 1.0) * w)
            vals.append(m7_map[f'{prefix}/{ckey}']['hit100_pct'])
        ax.bar(xs, vals, width=w * 0.9, color=color, label=clabel, zorder=3)
    ax.set_xticks(x2, [g[1] for g in groups], fontfamily=CJK_FONT, fontsize=5.6)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel('Joint 100 ms hit rate (%)')
    ax.tick_params(axis='x', length=0, pad=5)
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.8, handlelength=1.1, columnspacing=0.9, borderaxespad=0)

    save_fig(fig, 'm7-milikara-ablation')


def plot_refinement():
    m8 = json.loads((ROOT / 'results/M8/summary.json').read_text())['metrics']
    m8_map = {(r.get('separator', 'demucs'), r['trigger'], r['strategy']): r for r in m8}

    triggers = [
        ('same_vowel_imbalance', '同元音/同读音时长失衡'),
        ('legacy_conf', '一期旧置信度规则'),
        ('short_unit_30ms', '含 <30 ms 极短单元'),
        ('combined_30ms', '30 ms 极短或同元音失衡'),
        ('short_unit_40ms', '含 <40 ms 极短单元'),
        ('combined_40ms', '40 ms 极短或同元音失衡'),
        ('oracle_top_k', '按真实误差挑出最差行'),
    ]
    triggers = [(key, f"{label}\n(Demucs {m8_map[('demucs', key, 'nextfire_baseline')]['triggered_lines']} 行 / BS {m8_map[('bs', key, 'nextfire_baseline')]['triggered_lines']} 行)") for key, label in triggers]
    strategies = [
        ('nextfire_local', 'NextFire local window re-align', '#B64342'),
        ('mms_fa_local', 'MMS_FA + smart ext. local window', '#0F4D92'),
        ('mms_fa_global_swap', 'MMS_FA + smart ext. global line swap', '#42949E'),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(183 / 25.4, 84 / 25.4), sharey=True)
    fig.subplots_adjust(left=0.23, right=0.985, bottom=0.14, top=0.77, wspace=0.16)

    y = np.arange(len(triggers))
    h = 0.25

    for p_idx, (sep, p_label, title) in enumerate([
        ('demucs', 'a', 'Demucs'),
        ('bs', 'b', 'BS Karaoke'),
    ]):
        ax = axes[p_idx]
        add_panel_label(ax, p_label, x_pt=-14, y_pt=23)
        baseline = m8_map[(sep, 'same_vowel_imbalance', 'nextfire_baseline')]['hit100_pct']
        ax.set_title(f'{title} 组：相对首轮 ({baseline:.2f}%) 的净增命中数', fontsize=7, pad=23, fontfamily=CJK_FONT)
        ax.axvline(0, color='#888888', lw=0.8, linestyle='--', zorder=1)
        for idx, (skey, slabel, color) in enumerate(strategies):
            vals = [m8_map[(sep, tkey, skey)]['net_gain'] for tkey, _ in triggers]
            pcts = [m8_map[(sep, tkey, skey)]['hit100_pct'] for tkey, _ in triggers]
            centers = y + (idx - 1) * h
            ax.barh(centers, vals, height=h * 0.9, color=color, label=slabel if p_idx == 0 else None, zorder=3)
            for yi, val, pct in zip(centers, vals, pcts):
                sign = '+' if val > 0 else ''
                ha = 'left' if val >= 0 else 'right'
                pad = 4 if val >= 0 else -4
                label_txt = f'{sign}{val} ({pct:.2f}%)' if val > 0 else f'{sign}{val}'
                ax.text(val + pad, yi, label_txt, va='center', ha=ha, fontsize=5.5, color='#272727')
        if p_idx == 0:
            ax.set_yticks(y, [tlbl for _, tlbl in triggers], fontfamily=CJK_FONT, fontsize=5.8)
            ax.tick_params(axis='y', length=0, pad=6)
            ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.8, handlelength=1.1, columnspacing=0.9, borderaxespad=0)
        else:
            ax.tick_params(axis='y', length=0)
        ax.set_xlim(-145, 240)
        ax.set_xticks([-100, -50, 0, 50, 100, 150])
        ax.set_xlabel('Net unit change in joint 100 ms hits (fixed - broken)')
        ax.tick_params(axis='x', length=3, color='#888888')
        ax.spines['left'].set_visible(False)

    axes[0].set_ylim(len(triggers) - 0.5, -0.5)
    save_fig(fig, 'm8-local-refinement')


def plot_agent():
    m10 = json.loads((ROOT / 'results/M10/summary.json').read_text())
    m10_map = {(r['condition'], r['song'], r['scope']): r for r in m10['metrics']}
    base_map = {(r['source_module'], r['condition'], r['song'], r['scope']): r for r in m10['baselines']}

    fig, axes = plt.subplots(1, 2, figsize=(183 / 25.4, 76 / 25.4))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.19, top=0.76, wspace=0.20)

    songs_a = [
        ('j18', 'j18 真紅の刃\n(n=402 JA)'),
        ('j08', 'j08 光陰の海原\n(n=377)'),
        ('j14', 'j14 Spica\n(n=351)'),
        ('ALL', '三曲合计\n(n=1,130)'),
    ]
    series_a = [
        ('M1', 'G3-studio-bs-nextfire', 'M1 G3 pure-text auto', '#E9A6A1'),
        ('M8', 'bs-combined_40ms-mms_fa_global_swap', 'M8 cross-model swap (human reading)', '#42949E'),
        ('M10', 'initial', 'M10 Agent initial (NextFire)', '#3775BA'),
        ('M10', 'final', 'M10 Agent final (MCP visual refine)', '#0F4D92'),
    ]

    ax = axes[0]
    add_panel_label(ax, 'a', x_pt=-12, y_pt=24)
    ax.set_title('三首代表曲目的双端 100 ms 命中率对比 (日语主评估单元)', fontsize=7, pad=24, fontfamily=CJK_FONT)
    x = np.arange(len(songs_a))
    w = 0.19
    for idx, (src, ckey, clabel, color) in enumerate(series_a):
        vals = [
            m10_map[(ckey, sid, 'reading_units')]['hit100_pct'] if src == 'M10'
            else base_map[(src, ckey, sid, 'reading_units')]['hit100_pct']
            for sid, _ in songs_a
        ]
        offset = (idx - 1.5) * w
        bars = ax.bar(x + offset, vals, width=w * 0.92, color=color, label=clabel, zorder=3)
        if src == 'M10' and ckey == 'final':
            init_vals = [m10_map[('initial', sid, 'reading_units')]['hit100_pct'] for sid, _ in songs_a]
            for xi, bar, fv, iv in zip(x + offset, bars, vals, init_vals):
                ax.text(xi, fv + 1.5, f'{fv:.1f}%\n(+{fv - iv:.1f})', ha='center', va='bottom', fontsize=5.3, color='#0F4D92', fontweight='bold')
    ax.set_xticks(x, [lbl for _, lbl in songs_a], fontfamily=CJK_FONT, fontsize=5.8)
    ax.set_ylim(0, 115)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel('Joint 100 ms hit rate (%)')
    ax.tick_params(axis='x', length=0, pad=5)
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=2, fontsize=5.5, handlelength=1.1, columnspacing=0.8, borderaxespad=0)

    ax = axes[1]
    add_panel_label(ax, 'b', x_pt=-12, y_pt=24)
    ax.set_title('视觉精调前后的起点/终点 MAE 与综合 P95 误差', fontsize=7, pad=24, fontfamily=CJK_FONT)
    songs_b = [
        ('j18', 'all_reading_units', 'j18 全量\n(n=413)'),
        ('j08', 'reading_units', 'j08\n(n=377)'),
        ('j14', 'reading_units', 'j14\n(n=351)'),
        ('ALL', 'all_reading_units', '三曲全量\n(n=1,141)'),
    ]
    x2 = np.arange(len(songs_b))
    series_b = [
        ('initial', 'start_mae_ms', 'Initial Start MAE', '#E9A6A1'),
        ('final', 'start_mae_ms', 'Final Start MAE', '#0F4D92'),
        ('initial', 'end_mae_ms', 'Initial End MAE', '#B64342'),
        ('final', 'end_mae_ms', 'Final End MAE', '#42949E'),
    ]
    for idx, (st, mkey, mlabel, color) in enumerate(series_b):
        vals = [m10_map[(st, sid, sc)][mkey] for sid, sc, _ in songs_b]
        offset = (idx - 1.5) * w
        ax.bar(x2 + offset, vals, width=w * 0.92, color=color, label=mlabel, zorder=3)
    p95_init = [m10_map[('initial', sid, sc)]['abs_p95_ms'] for sid, sc, _ in songs_b]
    p95_final = [m10_map[('final', sid, sc)]['abs_p95_ms'] for sid, sc, _ in songs_b]
    ax.plot(x2 - 0.5 * w, p95_init, color='#767676', linestyle='--', marker='o', markersize=3.5, lw=1.1, label='Initial P95', zorder=4)
    ax.plot(x2 + 0.5 * w, p95_final, color='#272727', linestyle='-', marker='s', markersize=3.5, lw=1.2, label='Final P95', zorder=5)
    for idx_pt, (xi, pv) in enumerate(zip(x2 + 0.5 * w, p95_final)):
        offsets = [(-0.08, 7), (-0.18, 7), (0.0, 8), (0.14, 7)]
        dx, dy = offsets[idx_pt]
        ax.text(xi + dx, pv + dy, f'{pv:.0f} ms', ha='center', va='bottom', fontsize=5.4, color='#272727', fontweight='bold')
    ax.set_xticks(x2, [lbl for _, _, lbl in songs_b], fontfamily=CJK_FONT, fontsize=5.8)
    ax.set_ylim(0, 250)
    ax.set_yticks([0, 50, 100, 150, 200, 250])
    ax.set_ylabel('Absolute endpoint error (ms)')
    ax.tick_params(axis='x', length=0, pad=5)
    ax.tick_params(axis='y', length=3, color='#888888')
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), ncols=3, fontsize=5.4, handlelength=1.0, columnspacing=0.65, borderaxespad=0)

    save_fig(fig, 'm10-agent-mcp-refinement')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', choices=['all', 'm2', 'm3', 'm4', 'm7', 'm8', 'm10'], default='all')
    args = parser.parse_args()
    if args.only in ('all', 'm2'):
        plot_multilingual()
    if args.only in ('all', 'm3'):
        plot_aac()
    if args.only in ('all', 'm4'):
        plot_tempo()
    if args.only in ('all', 'm7'):
        plot_milikara()
    if args.only in ('all', 'm8'):
        plot_refinement()
    if args.only in ('all', 'm10'):
        plot_agent()
