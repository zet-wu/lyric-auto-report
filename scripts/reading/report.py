"""Render the current reading experiment with a separate mixed-song cohort."""
from common import *
from collections import Counter
protocol=read(ROOT/'configs/reading.json')
metrics=read(OUT/'metrics.json')
lookup={(r['scope'],r['method'],r['song']):r for r in metrics}
names={'studio':'Lazulite Studio','sudachi':'Sudachi','milikara':'MiliKara（UniDic）','milikara-fallback':'MiliKara（pykakasi 回退）','timing':'Timing','openjtalk':'OpenJTalk','sug':'SUG（Sudachi 回退）','sug-winrt':'SUG（WinRT）','terra-direct':'6.1 Terra 直接注音','terra-corrected':'6.1 Terra 修正 Lazulite Studio'}
def table(scope):
 lines=['| 方法 | 片段匹配 | 片段准确率 | 片段 CER | 整行匹配 | 整行准确率 |','| --- | ---: | ---: | ---: | ---: | ---: |']
 for method in protocol['methods']:
  a=lookup['kanji_spans',method,scope];b=lookup['japanese_lines',method,scope]
  lines.append(f"| {names[method]} | {a['exact']}/{a['n']} | {a['accuracy_pct']:.2f}% | {a['cer_pct']:.2f}% | {b['exact']}/{b['n']} | {b['accuracy_pct']:.2f}% |")
 return lines
refs=read(OUT/'references.json');primary=[r for r in refs if r['song'] in protocol['primary_songs']]
nlines=sum(len(r['lines']) for r in primary)
nwords=sum(len(l['words']) for r in primary for l in r['lines'])
excluded=Counter(r['reason'] for r in read(OUT/'excluded.json') if r['song'] in protocol['primary_songs'])
a=lookup['kanji_spans','studio','PRIMARY'];b=lookup['japanese_lines','studio','PRIMARY']
sug_a=lookup['kanji_spans','sug-winrt','PRIMARY'];sug_b=lookup['japanese_lines','sug-winrt','PRIMARY']
sug_runtime=read(OUT/'runtime/sug-winrt.json');sug_env=read(OUT/'sug-winrt-environment.json')
assert sug_env['require_winrt'] and all(r['analyzer']=='WinRTAnalyzer' for r in sug_runtime)
pending=sum(r['pending_units'] for r in sug_runtime)
text=['# 日语自动注音准确率','',f"12 首日语主组中，SUG Windows WinRT 注音有 {sug_a['exact']}/{sug_a['n']} 个共同正文片段与人工读音完全一致（{sug_a['accuracy_pct']:.2f}%），整行匹配为 {sug_b['exact']}/{sug_b['n']}（{sug_b['accuracy_pct']:.2f}%）。Lazulite Studio 对应为 {a['accuracy_pct']:.2f}% 和 {b['accuracy_pct']:.2f}%。SUG WinRT 自动注音实验在独立 Windows 环境中进行，并按相同规则评分，原 SUG Sudachi 回退结果与 WinRT 分列，其余方法沿用冻结预测；混合歌曲 s11 的日语部分单列。",'',
'## 数据与计分','',
f'主组使用 s01–s10、s12、s15 共 12 首日语歌曲，合计 {nlines} 行、{nwords} 个原始正文分段。混合歌曲 s11《星》另取原始顺序前 10 行日语歌词，其余粤语行不参与。曲目见[测试集](../datasets/README.md)，范围与输入哈希见[协议](../configs/reading.json)。对齐实验 G3 仍使用 12 首主组。','',
'正文从 TTML（保存歌词、注音与时间的标注格式）提取，清除 XML 排版的换行、回车和制表符，保留普通空格。注音方法只接收正文；人工 Ruby（正文附带的读音标注）单独保存用于评分，源 TTML 未修改。','',
f"各方法分词不同，片段表采用原标注与全部十种方法共有的正文边界，合并非共同边界后比较完整读音。主组分母为 {a['n']} 个含汉字且参考为假名的片段；{excluded['no_kanji']} 个无汉字片段、{excluded['reference_not_kana']} 个参考非纯假名片段排除。整行表使用参考全部为假名的 {b['n']} 行，排除 {nlines-b['n']} 行。分母由本次方法集合确定。",'',
'归一化使用 NFKC（统一全角、半角等兼容字符形式）、片假名转平假名、去除标点与空白；保留小假名、长音符和助词拼写。空输出、残留汉字或拉丁字母计为错误。片段准确率为完全匹配数除以片段数。','',
'CER（Character Error Rate，字符错误率）为逐片段 Levenshtein 编辑距离之和除以参考假名字符总数；编辑距离是把预测改成参考所需的最少字符插入、删除和替换次数。CER 越低越好。整行准确率要求该行归一化读音全部匹配。','',
'这衡量人工 Ruby 的书写一致性。Timing、OpenJTalk 的发音前端可能输出「わ／お／ー」，而参考使用「は／を／う」；这些差异保留计分，不能直接解释为声学发音错误。歌曲指定读音以原标注为准。','',
'## 方法与生成条件','',
'| 方法 | 实际调用 |','| --- | --- |',
f"| Lazulite Studio | 固定 `{protocol['source_commits']['studio'][:7] if isinstance(protocol['source_commits']['studio'],str) else protocol['source_commits']['studio']['commit'][:7]}`；Sudachi C 模式选读，JmdictFurigana 按词面与所选读音拆分注音。 |",
'| Sudachi | 直接读取 C 模式 reading_form。 |',
'| MiliKara | rule_segments，显式使用已下载的 UniDic；pykakasi 回退另列。对齐 G3 则使用其原生环境中的 UniDic Lite。 |',
'| Timing | 原生 UniDic 分词及数字、借词、发音覆盖规则，取首选读音。 |',
'| OpenJTalk | pyopenjtalk 文本前端与固定 1.11 词典。 |',
f"| SUG（Sudachi 回退） | 保留原 Linux 运行的 Sudachi 回退预测，经原生 PronunciationResolver 生成计划；13 首共 {sum(r['pending_units'] for r in read(OUT/'runtime/sug.json'))} 个未决单元。运行记录见 [sug.json](../results/reading/runtime/sug.json)。 |",
f"| SUG（WinRT） | 固定 `{sug_env['source_commit'][:7]}`；Windows WinRTAnalyzer，经原生 PronunciationResolver.resolve_project(fill_missing=True) 生成计划，按原始字符收集读音；13 首共 {pending} 个未决单元。pykakasi 仅作为原生读音分配的单字参考。本表评估自动注音计划，非 .sug 保存后保留的时间粒度。 |",
'| 6.1 Terra 直接注音 | 只读整首正文与输入分段，生成假名。 |',
'| 6.1 Terra 修正 Lazulite Studio | 直接条件完成后，读取新生成的 Lazulite Studio 候选并修正，按相同输入分段输出。 |','',
'LLM（大语言模型）统一使用 gpt-6.1-terra、high 推理强度。三批隔离子代理分别处理 s01–s04、s05–s08、s09/s10/s11/s12/s15；每批先完成直接注音，再在同一代理上下文中修正 Lazulite Studio 候选。因此修正条件也保留该代理先前的直接注音上下文。代理不能访问人工参考、音频、时间、其他方法结果、网络或词典；仅允许无参考答案的格式校验。每曲每条件生成一份，未根据评分挑选或修订。26 份新输出的输入、结果哈希见[执行记录](../results/reading/llm-execution.json)。','',
'## 12 首日语主组','']+table('PRIMARY')+['','## 混合歌曲 s11：日语部分','',
'仅比较选定的 10 行日语正文，独立构造共同边界。该单曲结果不计入主组。','']+table('s11')+['','## 结果解释与复核','',
'各路线按表中实际输出比较。片段指标关注整段读音是否一致，CER 反映字符修正量；整行指标还包括助词与原有假名。Terra 的两种条件各只有一次生成，表中结果不估计重复生成的波动。SUG 本次使用 Windows 系统日语注音引擎，其输出可能随系统与日语组件版本变化；环境、依赖和预测哈希见[运行环境](../results/reading/sug-winrt-environment.json)，未决单元见[运行记录](../results/reading/runtime/sug-winrt.json)。','',
'[八路线对齐](comparison.md)保留原 Linux 实验结果，其中 SUG 自动注音条件未改用本次 WinRT 预测；本报告不能据此推断 Windows 注音带来的时间轴变化。其他方法预测、评分分母和时间对齐结果的不变性核验见[独立 Windows 实验核验](../results/reading/sug-winrt-audit.json)。','',
'逐曲指标、片段预测及排除原因分别见 [metrics.json](../results/reading/metrics.json)、[items.json](../results/reading/items.json)、[excluded.json](../results/reading/excluded.json)；完整预测见 [predictions](../results/reading/predictions/)。复现方法见[复现说明](reproduce.md)。']
(ROOT/'reports/auto-reading.md').write_text('\n'.join(text)+'\n',encoding='utf-8',newline='\n')
