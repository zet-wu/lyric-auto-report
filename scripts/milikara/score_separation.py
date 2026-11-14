"""Score all separator/target/persistence conditions with fixed denominators."""
from common import *
from evaluate import score,stats
import collections,csv,numpy as np
folder=ROOT/'results/separation-alignment'
refs={s['id']:s for s in read(OUT/'references.json')}
groups=collections.defaultdict(list);by_song=[]
paths={p.with_suffix('') if p.suffix=='.gz' else p for p in (folder/'predictions').rglob('*.json*')}
for path in sorted(paths):
 r=read(path);rows,diagnostics=score(refs[r['song']],r)
 for group in ('all','japanese','latin'):
  selected=[x for x in rows if group=='all' or x['language']==group]
  item={k:r[k] for k in ('experiment','separator','persistence','mode','kind','song')}
  item.update(group=group,**stats(selected))
  by_song.append(item)
  if r['song']!='s13':groups[(r['experiment'],group)].append((item,selected))
aggregate=[]
for (exp,group),pairs in groups.items():
 pooled=sum([rows for _,rows in pairs],[])
 row={**pairs[0][0],'song':'ALL',**stats(pooled)}
 row['songs']=len(pairs)
 row['macro100_pct']=float(np.mean([x['hit100_pct'] for x,_ in pairs if x['n']]))
 aggregate.append(row)
dump(folder/'metrics.json',{'aggregate':aggregate,'by_song':by_song})
print('Scored separator conditions',len(paths))
with (folder/'metrics.csv').open('w') as stream:
 writer=csv.DictWriter(stream,fieldnames=list(aggregate[0]))
 writer.writeheader();writer.writerows(aggregate)
lines=['# 十种分离配置下游完整结果','','主组为 12 首日语歌曲。表中 100 ms 为歌曲等权宏平均；单元计数和缺失见 CSV。路径代码 float 为浮点音频，pcm24 为 24 位音频采样保存后读回；core 为核心人声区间拼接，padded 为带缓冲拼接，full 为完整人声。','','| 分离器 | 路径 | 音频 | 目标 | 语言组 | 单元 | 100 ms 宏平均 | 100 ms 个数 | 缺失 |','| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |']
for r in aggregate:
 lines.append(f"| {r['separator']} | {r['persistence']} | {r['mode']} | {r['kind']} | {r['group']} | {r['n']} | {r['macro100_pct']:.2f}% | {r['hit100']} | {r['missing_or_nonpositive']} |")
(folder/'tables.md').write_text('\n'.join(lines)+'\n')
