"""Render static research tables and figures after completing the matrix."""
from ablation_common import *
import os,collections
os.environ.setdefault('MPLCONFIGDIR',str(ROOT / '.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.hashsalt']='lyric-auto-report'
import matplotlib.pyplot as plt
import numpy as np

m=read(OUT/'metrics.json')
primary={(r['separator'],r['backend'],r['strategy'],r['subset']):r for r in m['aggregate'] if r['cohort']=='primary'}
strategies=['concat','padded','full','auto_mms','auto_nf','human']
labels=['Core concat','Padded concat','Full stem','MMS windows','NextFire windows','Human windows']
seps=['demucs','bs','kim']
fig,axes=plt.subplots(1,3,figsize=(16,6),layout='constrained')
for ax,backend in zip(axes,['nextfire','tifa','mms_fa']):
    values=np.array([[primary[(sep,backend,st,'all')]['macro100']*100 for sep in seps] for st in strategies])
    im=ax.imshow(values,vmin=0,vmax=100,cmap='viridis',aspect='auto')
    ax.set_xticks(range(3),['Demucs','BS Karaoke','Kim']);ax.set_yticks(range(len(strategies)),labels)
    ax.set_title(backend.upper())
    for i in range(len(strategies)):
        for j in range(3):ax.text(j,i,f'{values[i,j]:.2f}%',ha='center',va='center',color='black' if values[i,j]>65 else 'white')
fig.colorbar(im,ax=axes,shrink=.75,label='Both endpoints within 100 ms (%)')
fig.suptitle('11 songs, equal song weights; fixed readings; failures retained\nHuman windows are a diagnostic condition, not an automatic pipeline')
fig.savefig(OUT/'matrix.png',dpi=170);fig.savefig(OUT/'matrix.svg',metadata={'Date':None});plt.close(fig)
svg=OUT/'matrix.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')

lines=['# 自动生成的消融结果表','', '主表为 11 首歌曲等权的双端 100 ms 命中率。MAE（Mean Absolute Error）为平均绝对端点误差。BS Karaoke 为主唱提取权重；后端代码 tifa 和 mms_fa 分别对应 TIFA 与 MMS_FA。策略 concat 为核心人声区间拼接，padded 为带缓冲拼接，full 为完整人声；auto_mms / auto_nf 为两种模型预测的自动行窗口，human 为人工行窗口。','']
for backend in ['nextfire','tifa','mms_fa']:
    lines += [f'## {backend}', '', '| 策略 | Demucs | BS Karaoke | Kim |','| --- | ---: | ---: | ---: |']
    for st in strategies:
        lines.append('| '+st+' | '+' | '.join(f"{primary[(sep,backend,st,'all')]['macro100']*100:.2f}%" for sep in seps)+' |')
    lines.append('')
lines+=['## 全部固定分母结果','','| 分离 | 后端 | 策略 | 100 ms 数/固定分母 | 宏平均 | 200 ms 数 | 缺失 | >1s | 起/止 MAE ms |','| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for (sep,backend,st,subset),r in primary.items():
    if subset!='all':continue
    lines.append(f"| {sep} | {backend} | {st} | {r['hit100']}/{r['n']} | {r['macro100']*100:.2f}% | {r['hit200']} | {r['missing']} | {r['gt1s']} | {r.get('start_mae_ms',0):.2f}/{r.get('end_mae_ms',0):.2f} |")
for subset in ['sustained_600ms','written_long_mark','adjacent_identical_phones','same_phone_at_next_boundary']:
    lines+=['',f'## {subset}','','| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |','| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for (sep,backend,st,sub),r in primary.items():
        if sub!=subset:continue
        lines.append(f"| {sep} | {backend} | {st} | {r['n']} | {r['hit100']} | {r['missing']} | {r.get('end_mae_ms',0):.2f} | {r.get('end_bias_ms',0):.2f} | {r.get('duration_ratio_median',0):.3f} | {r.get('collapsed',0)} |")
lines+=['','## 逐歌曲','','| 分离 | 后端 | 策略 | 歌曲 | 语言子集 | 分母 | 100 ms | 200 ms | 缺失 | >1s |','| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |']
names={s['id']:s['name'] for s in read(OUT/'targets.json')}
for r in m['by_song']:
    if r['subset']!='all':continue
    lines.append(f"| {r['separator']} | {r['backend']} | {r['strategy']} | {names[r['song']]} | {r['cohort']} | {r['n']} | {r['hit100']} | {r['hit200']} | {r['missing']} | {r['gt1s']} |")
(OUT/'tables.md').write_text('\n'.join(lines)+'\n')
print('rendered tables and matrix')
