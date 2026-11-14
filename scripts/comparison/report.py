from common import *
from collections import Counter
NAMES={'studio-nextfire':'Lazulite Studio + NextFire','studio-mms-fa':'Lazulite Studio + MMS_FA + 智能延长','milikara':'MiliKara（NextFire）','timing':'Timing（BS Karaoke + TIFA）','sug-nextfire':'SUG（NextFire）','sug-mms-fa':'SUG（MMS_FA）','yohane':'yohane（NextFire）','fa-kara':'FA-Kara（MMS_FA）'}
readings=read(OUT/'scores/reading-summary.json');scores=read(OUT/'scores/summary.json');states=read(OUT/'scores/status.json');pins=read(ROOT/'configs/comparison-sources.json')
assert not any(s['status']=='pending' for s in states),'Do not publish unfinished runs'
def val(x):return '—' if x is None else f'{x:.2f}'
def table(metrics, reading=False, merges=False):
 out=['| 路线 | 100 ms 命中 | 200 ms 命中 | MAE 起 / 止 ms | 绝对误差 P95 起 / 止 ms | 缺失 | >1 s |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
 for route,m in metrics.items():
  out.append(f"| {NAMES[route]} | {m['hit100']}/{m['n']}（{val(m['hit100_pct'])}%） | {m['hit200']}/{m['n']}（{val(m['hit200_pct'])}%） | {val(m['start_mae_ms'])} / {val(m['end_mae_ms'])} | {val(m['start_p95_ms'])} / {val(m['end_p95_ms'])} | {m['missing']} | {m['over1s']} |")
 if reading or merges:
  extra=' 合并边界 / 涉及单元 |' if reading else ' 合并边界 |'
  out[0]+=extra;out[1]+=' ---: |'
  for i,m in enumerate(metrics.values(),2):out[i]+=f" {m['merged_boundaries']} / {m['merged_units']} |" if reading else f" {m['merged_boundaries']} |"
 return out
text=['# 八条路线的歌词对齐准确率','','12 首日语歌曲、三组输入条件。每组分别报告组内共同正文边界和参考读音单元两张表；100 ms、200 ms 均要求起止两端同时命中，缺失保留在分母。MAE（Mean Absolute Error，平均绝对误差）及绝对误差 P95（第 95 百分位数）按起点／终点分列，只统计有效预测。超过 1 s 按至少一端超限计数。','','输入、边界构造、叠唱处理及原生导出语义见[方法](methods.md)。逐项误差、分区、逐曲指标及失败状态分别位于 [scores](../results/comparison/scores/)。','']
for group,title in [('G1','人工读音 + 各自人声分离'),('G2','人工读音 + 统一 BS Karaoke'),('G3','自动读音 + 各自人声分离')]:
 text+=['## '+group+'：'+title,'','### 共同正文边界','']+table({k:x['overall'] for k,x in scores[group].items()},merges=True)+['','### 读音单元（人工标注分母）','']+table({k:x['overall'] for k,x in readings[group].items()},reading=True)+['']
text+=['正文表的合并边界数是共同分区合并掉的原正文内部边界数。读音表固定原标注中 5370 个日语读音单元；“合并边界 / 涉及单元”分别表示原生输出没有保留的内部读音边界数，以及因此计入缺失的人工单元数。例如两个单元合为一个，记 1 个合并边界、2 个缺失单元；这些单元仍留在分母。整曲失败、无效时间及读音对应不唯一也计缺失，分类见 [reading-summary.json](../results/comparison/scores/reading-summary.json)。','','Timing 的各自分离器就是 BS Karaoke，FA-Kara 使用外部 BS Karaoke；这两条路线在 G1、G2 复用相同结果。G3 不含 yohane 与 FA-Kara。','','## 正文边界：单曲与叠唱','','s15 为《リトルミラクル -Grip it tight-》，包含 44 行主歌词、14 行背景歌词。背景词不作为目标。先单列 s15 的全曲与叠唱区间结果，再汇总全部 12 首歌曲中与背景歌词重叠的主歌词区间；后者包括 s03、s06、s07、s15。']
for group in scores:
 text+=['','### '+group+'：s15 全曲','']+table({k:x['s15'] for k,x in scores[group].items()})
 text+=['','### '+group+'：s15 叠唱区间主歌词','']+table({k:x['s15_overlap'] for k,x in scores[group].items()})
 text+=['','### '+group+'：全部歌曲叠唱区间主歌词','']+table({k:x['overlap'] for k,x in scores[group].items()})
text+=['','逐曲双端 100 ms 命中率如下；完整六项逐曲指标见 [summary.json](../results/comparison/scores/summary.json)。','']
for group in scores:
 text+=['### '+group+' 逐曲','', '| 歌曲 | '+' | '.join(NAMES[k] for k in scores[group])+' |','| --- | '+' | '.join('---:' for _ in scores[group])+' |']
 for s in songs():text.append('| '+s['id']+' | '+' | '.join(val(x['per_song'][s['id']]['hit100_pct'])+'%' for x in scores[group].values())+' |')
 text+=['']
text+=['读音单元的逐曲及叠唱指标见 [reading-summary.json](../results/comparison/scores/reading-summary.json)，逐项映射、合并与缺失原因见 [reading-items.json.gz](../results/comparison/scores/reading-items.json.gz)。Lazulite Studio 人工读音的原标注细项及宏平均（先逐曲计算，再对歌曲等权平均）见 [studio-leaf-summary.json](../results/comparison/scores/studio-leaf-summary.json)。','']
text+=['## 完成情况与原生失败','','整曲失败的项目保留全部参考分母。环境安装、输入格式适配、缓存损坏等问题修复后重跑，不作为算法失败。','', '| 组别 | 路线 | 有结果歌曲 / 12 |','| --- | --- | ---: |']
for group in scores:
 for route in scores[group]:text.append(f"| {group} | {NAMES[route]} | {sum(x['status']=='ok' for x in states if x['group']==group and x['route']==route)}/12 |")
failures=[x for x in states if x['status']!='ok'];text+=['','失败明细：','']
for x in failures:
 error=next((l for l in reversed(x.get('error','').splitlines()) if l.strip()),'未返回结果')
 text.append(f"- {x['group']} / {NAMES[x['route']]} / {x['song']}：`{error.replace('`','')}`")
text+=['','## 输入适配与读音','','人工组读取原 TTML 的整词注音；“明日→あす”“生命→いのち”等共享注音保留为整词，不按汉字猜分。输入核验未发现需要补写的日语汉字读音，因此人工补齐清单为空，原始 TTML 未修改。','','SUG 通过原生领域对象输入正文与 Ruby（附在正文上的读音标注），绕开 TTML 导入对多字共享注音的拆分损失，再使用原生注音计划、模型与采用命令，最终保存并重新加载 .sug 项目评分。项目中相邻节奏点构成最小时间区间，句末使用保存的句末点；Ruby 分段按节奏点索引对应。自动组使用原生逐行注音器，自动补出的读音不会写回工程，部分汉字只保存一个节奏点，按实际保存粒度统计合并缺失。[68 份原生项目](../results/comparison/sug/projects)及[保存／加载核验](../results/comparison/sug-project-audit.json)随结果发布。','','Timing 人工组使用显式读音接口：长音符与前一假名连接，独立小写元音转为等价全尺寸元音，英文词片段恢复完整单词；英语缺词使用 TIFA 随附的词典／LSTM 发音转换器。整曲 MMS 声学定位产生窗口，再调用原生 TIFA 显式读音路径。该接口适配没有调用 LLM，也没有传入人工时间。自动组直接运行原生无时间正文管线。','','yohane 接收人工读音的罗马字格式，罗马化只转换已给定的读音；不重新选择汉字读法。FA-Kara 使用原生假名文本及整词注音语法，显式罗马字按接口要求转为小写。评分读取原生 ASS 导出并累计卡拉 OK 时值（[导出核验](../results/comparison/export-audit.json)）；该导出会将部分尾点连接到下一项目起点，不能以导出前的中间时间替代。','','MiliKara 使用默认重试机制，部分行会采用原曲；采用来源在原生导出中保存。自动组实际使用其运行环境中的 UniDic Lite。比较使用各自默认字典，不把统一字典替换成原生配置。','','## 固定版本','','| 项目 | 提交 |','| --- | --- |']
for k,v in pins.items():text.append(f"| [{'Lazulite Studio' if k=='studio' else k}]({v['url'].removesuffix('.git')}) | `{v['commit']}` |")
text+=['','Lazulite Studio 两条路线均关闭间隙合并，只有 MMS_FA 开启智能延长：取 FA-Kara 静音搜索、全部片段核心区终点 core_end（含长片段内部寻谷分界）、下一有效单元起点中的最早候选，末尾以音频终点封顶。本轮复用未变更的 GPU 声学结果，重新调用当前产品后处理和前端采用，72 个条件的核验见 [记录](../results/comparison/studio-postprocessing-audit.json)。SUG 分离权重固定 UVR-MDX-NET-Inst_HQ_3。所有对齐和分离均在 GPU 上运行，未采用 Whisper 或 Qwen 对齐路径。质量实验并行运行，日志耗时不用于速度排名。','','运行方式为 Linux 源码接口适配：调用各项目的对齐、采用与导出，未测试官方 GUI 安装包。Timing、yohane 使用 Transformers 5.15.0；SUG 使用 5.15.0、audio-separator 0.47.0 与 librosa 0.10.2.post1；FA-Kara 使用 librosa 0.11.0，其 MMS_FA 路径不调用 Transformers。Torch／torchaudio 使用记录中的本机 CUDA 版本，FA-Kara 的 Windows 冻结环境与 yohane 的 CLI 可选依赖组合没有原样复刻；Timing 源码在 Python 3.13 调用，区别于其应用声明的 Python 3.12 范围。','','复现入口及环境记录见[复现说明](reproduce.md)与[环境清单](../results/comparison/environment.json)。']
(ROOT/'reports/comparison.md').write_text('\n'.join(text)+'\n')
