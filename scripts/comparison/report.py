from common import *
from collections import Counter
import argparse
parser=argparse.ArgumentParser();parser.add_argument("--g3-data-only",action="store_true");parser.add_argument("--g3-tables-only",action="store_true");parser.add_argument("--tables-only",action="store_true");args=parser.parse_args()
NAMES={'studio-nextfire':'Lazulite Studio + NextFire','studio-mms-fa':'Lazulite Studio + MMS_FA + 智能延长','milikara':'MiliKara（NextFire）','timing':'Timing（BS Karaoke + TIFA）','sug-nextfire':'SUG（NextFire）','sug-mms-fa':'SUG（MMS_FA）','yohane':'yohane（NextFire）','fa-kara':'FA-Kara（MMS_FA）'}
ROUTES={
 'studio-nextfire':('Lazulite Studio','Demucs htdemucs','NextFire'),
 'studio-mms-fa':('Lazulite Studio','Demucs htdemucs','MMS_FA + 智能延长'),
 'milikara':('MiliKara','MelBand RoFormer ep_3005','NextFire'),
 'timing':('Timing','BS Karaoke','TIFA'),
 'sug-nextfire':('SUG','MDX-Net Inst HQ 3','NextFire'),
 'sug-mms-fa':('SUG','MDX-Net Inst HQ 3','MMS_FA'),
 'yohane':('yohane','HybridDemucs MUSDB Plus','NextFire'),
 'fa-kara':('FA-Kara','BS Karaoke','MMS_FA'),
}
def route_cells(route,group):
 project,separator,aligner=ROUTES[route]
 return ' | '.join((project,'BS Karaoke' if group=='G2' else separator,aligner))
readings=read(OUT/'scores/reading-summary.json');scores=read(OUT/'scores/summary.json');states=read(OUT/'scores/status.json');pins=read(ROOT/'configs/comparison-sources.json')
assert not any(s['status']=='pending' for s in states),'Do not publish unfinished runs'
def val(x):return '—' if x is None else f'{x:.2f}'
def table(metrics, group, reading=False, merges=False):
 out=['| 项目 | 人声分离模型 | 对齐模型 | 100 ms 命中 | 200 ms 命中 | MAE 起 / 止 ms | 绝对误差 P95 起 / 止 ms | 缺失 | >1 s |','| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
 for route,m in metrics.items():
  out.append(f"| {route_cells(route,group)} | {m['hit100']}/{m['n']}（{val(m['hit100_pct'])}%） | {m['hit200']}/{m['n']}（{val(m['hit200_pct'])}%） | {val(m['start_mae_ms'])} / {val(m['end_mae_ms'])} | {val(m['start_p95_ms'])} / {val(m['end_p95_ms'])} | {m['missing']} | {m['over1s']} |")
 if reading or merges:
  extra=' 合并边界 / 涉及单元 |' if reading else ' 合并边界 |'
  out[0]+=extra;out[1]+=' ---: |'
  for i,m in enumerate(metrics.values(),2):out[i]+=f" {m['merged_boundaries']} / {m['merged_units']} |" if reading else f" {m['merged_boundaries']} |"
 return out
text=['# 八条路线的歌词对齐准确率', '', '12 首日语歌曲、三组输入条件。每组分别报告组内共同正文边界和人工读音边界两张表；100 ms、200 ms 均要求起止两端同时命中，缺失保留在分母。MAE（Mean Absolute Error，平均绝对误差）及绝对误差 P95（第 95 百分位数）按起点／终点分列，只统计有效预测。超过 1 s 按至少一端超限计数。', '', '由于某些路线在对齐时会将某些读音单元合并（如长音、促音等），因此输出的总单元数量，即准确率的分母会不一致。因此本报告每一组提供两个表，共同正文边界指将所有路线的结果的单元边界取交集，仅计算这些共同边界的准确率；人工读音边界则使用源参考歌词的总单元数量，将被合并的单元记为缺失。', '', '正文表的合并边界数是共同分区合并掉的原正文内部边界数。读音表固定原标注中 5370 个日语读音单元；“合并边界 / 涉及单元”分别表示原生输出没有保留的内部读音边界数，以及因此计入缺失的人工单元数。例如两个单元合为一个，记 1 个合并边界、2 个缺失单元；这些单元仍留在分母。整曲失败、无效时间及读音对应不唯一也计缺失，分类见 [reading-summary.json](../results/comparison/scores/reading-summary.json)。', '', 'Timing 的各自分离器就是 BS Karaoke，FA-Kara 使用外部 BS Karaoke；这两条路线在 G1、G2 复用相同结果。G3 不含 yohane 与 FA-Kara。', '', '输入、边界构造、叠唱处理及原生导出语义见[方法](methods.md)。逐项误差、分区、逐曲指标及失败状态分别位于 [scores](../results/comparison/scores/)。', '']
for group,title in [('G1','人工读音 + 各自人声分离'),('G2','人工读音 + 统一 BS Karaoke'),('G3','自动读音 + 各自人声分离')]:
 text+=['## '+group+'：'+title,'','### 共同正文边界','']+table({k:x['overall'] for k,x in scores[group].items()},group,merges=True)+['','### 人工读音边界','']+table({k:x['overall'] for k,x in readings[group].items()},group,reading=True)+['']
# Reaggregate frozen item-level predictions; percentiles cannot be averaged across songs.
from score import measure
from score_reading import metrics as reading_metrics
excluded_songs={r['song'] for r in states if r['group']=='G3' and r['route'] in ('sug-nextfire','sug-mms-fa') and r['status']!='ok'}
body_items=read(OUT/'scores/items.json')
reading_items=read(OUT/'scores/reading-items.json')
subset_body={};subset_reading={}
for route in scores['G3']:
 selected=[r for r in body_items if r['group']=='G3' and r['route']==route and r['song'] not in excluded_songs]
 subset_body[route]={**measure(selected),'merged_boundaries':sum(r['merged_boundaries'] for r in selected)}
 selected=[r for r in reading_items if r['group']=='G3' and r['route']==route and r['song'] not in excluded_songs]
 subset_reading[route]=reading_metrics(selected)
text+=['在这一组中，SUG 由于 `s01` `s05` 这两首歌曲的个别词注音失败，导致整曲失败。Timing 的整曲失败则更多。为了进一步比较 SUG 在全自动流程下的实际效果，统计剔除了 `s01` `s05` 两首 SUG 失败歌曲的结果如下：','','以下六条路线统一剔除 s01、s05，保留其余 10 首歌和原 G3 共同正文分区，共 1830 个正文区间、4478 个人工读音单元。Timing 在剩余歌曲中的 5 首整曲失败仍计入分母。所有指标由已保存的逐项预测重新汇总；MAE 和 P95 按有效预测计算。','','### 共同正文边界（剔除 s01、s05）','']+table(subset_body,'G3',merges=True)+['','### 人工读音边界（剔除 s01、s05）','']+table(subset_reading,'G3',reading=True)+['']
text+=['## 正文边界：叠唱','','汇总全部 12 首歌曲中与背景歌词重叠的主歌词区间，涉及 s03、s06、s07、s15；背景词不作为目标。']
for group in scores:
 text+=['','### '+group+'：全部歌曲叠唱区间主歌词','']+table({k:x['overlap'] for k,x in scores[group].items()},group)
text+=['','逐曲双端 100 ms 命中率如下；完整六项逐曲指标见 [summary.json](../results/comparison/scores/summary.json)。','']
for group in scores:
 song_ids=[s['id'] for s in songs()]
 text+=['### '+group+' 逐曲','', '| 项目 | 人声分离模型 | 对齐模型 | '+' | '.join(song_ids)+' |','| --- | --- | --- | '+' | '.join('---:' for _ in song_ids)+' |']
 for route,x in scores[group].items():text.append('| '+route_cells(route,group)+' | '+' | '.join(val(x['per_song'][sid]['hit100_pct'])+'%' for sid in song_ids)+' |')
 text+=['']
text+=['读音单元的逐曲及叠唱指标见 [reading-summary.json](../results/comparison/scores/reading-summary.json)，逐项映射、合并与缺失原因见 [reading-items.json.gz](../results/comparison/scores/reading-items.json.gz)。Lazulite Studio 人工读音的原标注细项及宏平均（先逐曲计算，再对歌曲等权平均）见 [studio-leaf-summary.json](../results/comparison/scores/studio-leaf-summary.json)。','']
text+=['## 完成情况与原生失败','','整曲失败的项目保留全部参考分母。环境安装、输入格式适配、缓存损坏等问题修复后重跑，不作为算法失败。','', '| 组别 | 项目 | 人声分离模型 | 对齐模型 | 有结果歌曲 / 12 |','| --- | --- | --- | --- | ---: |']
for group in scores:
 for route in scores[group]:text.append(f"| {group} | {route_cells(route,group)} | {sum(x['status']=='ok' for x in states if x['group']==group and x['route']==route)}/12 |")
failures=[x for x in states if x['status']!='ok'];text+=['','失败明细：','']
for x in failures:
 error=next((l for l in reversed(x.get('error','').splitlines()) if l.strip()),'未返回结果')
 text.append(f"- {x['group']} / {NAMES[x['route']]} / {x['song']}：`{error.replace('`','')}`")
text+=['','## 输入适配与读音','','人工组读取原 TTML 的整词注音；“明日→あす”“生命→いのち”等共享注音保留为整词，不按汉字猜分。输入核验未发现需要补写的日语汉字读音，因此人工补齐清单为空，原始 TTML 未修改。','','SUG 通过原生领域对象输入正文与 Ruby（附在正文上的读音标注），绕开 TTML 导入对多字共享注音的拆分损失，再使用原生注音计划、模型与采用命令，最终保存并重新加载 .sug 项目评分。项目中相邻节奏点构成最小时间区间，句末使用保存的句末点；Ruby 分段按节奏点索引对应。自动组使用原生逐行注音器，自动补出的读音不会写回工程，部分汉字只保存一个节奏点，按实际保存粒度统计合并缺失。[68 份原生项目](../results/comparison/sug/projects)及[保存／加载核验](../results/comparison/sug-project-audit.json)随结果发布。','','Timing 人工组使用显式读音接口：长音符与前一假名连接，独立小写元音转为等价全尺寸元音，英文词片段恢复完整单词；英语缺词使用 TIFA 随附的词典／LSTM 发音转换器。整曲 MMS 声学定位产生窗口，再调用原生 TIFA 显式读音路径。该接口适配没有调用 LLM，也没有传入人工时间。自动组直接运行原生无时间正文管线。','','yohane 接收人工读音的罗马字格式，罗马化只转换已给定的读音；不重新选择汉字读法。FA-Kara 使用原生假名文本及整词注音语法，显式罗马字按接口要求转为小写。评分读取原生 ASS 导出并累计卡拉 OK 时值（[导出核验](../results/comparison/export-audit.json)）；该导出会将部分尾点连接到下一项目起点，不能以导出前的中间时间替代。','','MiliKara 使用默认重试机制，部分行会采用原曲；采用来源在原生导出中保存。自动组实际使用其运行环境中的 UniDic Lite。比较使用各自默认字典，不把统一字典替换成原生配置。','','## 固定版本','','| 项目 | 提交 |','| --- | --- |']
for k,v in pins.items():text.append(f"| [{'Lazulite Studio' if k=='studio' else k}]({v['url'].removesuffix('.git')}) | `{v['commit']}` |")
text+=['','Lazulite Studio 两条路线均关闭间隙合并，只有 MMS_FA 开启智能延长：取 FA-Kara 静音搜索、全部片段核心区终点 core_end（含长片段内部寻谷分界）、下一有效单元起点中的最早候选，末尾以音频终点封顶。本轮复用未变更的 GPU 声学结果，重新调用当前产品后处理和前端采用，72 个条件的核验见 [记录](../results/comparison/studio-postprocessing-audit.json)。SUG 分离权重固定 UVR-MDX-NET-Inst_HQ_3。所有对齐和分离均在 GPU 上运行，未采用 Whisper 或 Qwen 对齐路径。质量实验并行运行，日志耗时不用于速度排名。','','运行方式为 Linux 源码接口适配：调用各项目的对齐、采用与导出，未测试官方 GUI 安装包。Timing、yohane 使用 Transformers 5.15.0；SUG 使用 5.15.0、audio-separator 0.47.0 与 librosa 0.10.2.post1；FA-Kara 使用 librosa 0.11.0，其 MMS_FA 路径不调用 Transformers。Torch／torchaudio 使用记录中的本机 CUDA 版本，FA-Kara 的 Windows 冻结环境与 yohane 的 CLI 可选依赖组合没有原样复刻；Timing 源码在 Python 3.13 调用，区别于其应用声明的 Python 3.12 范围。','','复现入口及环境记录见[复现说明](reproduce.md)与[环境清单](../results/comparison/environment.json)。']
report_path=ROOT/'reports/comparison.md'
if args.g3_data_only or args.g3_tables_only or args.tables_only:
 # Preserve user-edited prose and all G1/G2 tables. Only refresh G3 data.
 def tables(lines):
  result={};section=heading='';i=0
  while i<len(lines):
   line=lines[i]
   if line.startswith('## '):section=line;heading=''
   elif line.startswith('### '):heading=line
   if line.startswith('|'):
    start=i
    while i<len(lines) and lines[i].startswith('|'):i+=1
    result[section,heading]=(start,i,lines[start:i]);continue
   i+=1
  return result
 old=report_path.read_text().splitlines();new_tables=tables(text);replacements=[]
 for key,(start,end,rows) in tables(old).items():
  section,heading=key
  if args.tables_only or section.startswith('## G3：') or heading.startswith('### G3'):
   replacements.append((start,end,new_tables[key][2]))
  elif section=='## 完成情况与原生失败':
   fresh={tuple(row.split('|')[1:5]):row for row in new_tables[key][2] if row.startswith('| G3 |')}
   replacements.append((start,end,[fresh[tuple(row.split('|')[1:5])] if row.startswith('| G3 |') else row for row in rows if not row.startswith('| G3 |') or tuple(row.split('|')[1:5]) in fresh]))
 for start,end,rows in reversed(replacements):old[start:end]=rows
 # Failure entries are result data; remove resolved failures and refresh remaining ones.
 new_failures=[line for line in text if line.startswith('- G3 /')]
 indices=[i for i,line in enumerate(old) if line.startswith('- G3 /')]
 if indices and not (args.g3_tables_only or args.tables_only):
  insert=indices[0];old=[line for line in old if not line.startswith('- G3 /')]
  old[insert:insert]=new_failures
 text=old
report_path.write_text('\n'.join(text)+'\n')
