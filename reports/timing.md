# Timing 完整链路与细对齐诊断

本轮使用 12 首日语歌曲评价 Timing 的正文自动读音管线，另用人工读音与人工行窗口诊断细对齐。公平比较各产品人工读音、统一分离与自动读音条件的主结果见[八路线三组比较](comparison.md)。

完整链路与模块诊断使用固定的共用研究环境（Transformers 4.57.6）；主比较中的 Timing 另在 Transformers 5.15.0 环境复测。两种环境的实测范围分别保存，不能混用指标。

## 正文输入的完整链路

三种条件分别采用无时间正文配 Demucs、可信人工行时间配 Demucs、以及 BS Karaoke 配无时间正文。可信人工行时间条件属于定位诊断。Lazulite Studio 此处使用人工 Ruby（附在正文上的读音标注）投影，与 Timing 的正文自动转换是两种输入形式；表中保留这个工作流差异。

双端命中要求起点和终点同时在阈值内。MAE（Mean Absolute Error，平均绝对误差）为有效端点与参考之差的绝对值均值；P95 是绝对误差的第 95 百分位数。缺失或无效单元保留在命中率分母，MAE 与 P95 只计算有效端点。任一端点绝对误差超过 1 秒即记为大误差项。

| 条件 | 分母 | 100 ms 命中 | 200 ms 命中 | 起／止 MAE ms | 起／止绝对误差 P95 ms | 缺失 | >1 秒 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lazulite Studio 人工读音投影 | 4329 | 3614（83.48%） | 4051（93.58%） | 53.64 / 65.06 | 125.02 / 194.00 | 9 | 42 |
| Timing／无时间正文＋Demucs | 4329 | 891（20.58%） | 1073（24.79%） | 133.98 / 147.74 | 123.00 / 232.00 | 3179 | 19 |
| Timing／人工行时间＋Demucs | 4329 | 1165（26.91%） | 1365（31.53%） | 181.83 / 188.57 | 144.80 / 298.40 | 2842 | 40 |
| Timing／无时间正文＋BS Karaoke | 4329 | 1197（27.65%） | 1403（32.41%） | 66.79 / 67.10 | 116.00 / 183.35 | 2835 | 7 |

| Timing 条件 | 完成歌曲 |
| --- | --- |
| 无时间正文＋Demucs | 4/12 |
| 人工行时间＋Demucs | 5/12 |
| 无时间正文＋BS Karaoke | 5/12 |

表格按原正文对象边界计分；失败歌曲保留全部分母。粗定位占位输出不作为有效细对齐结果。Lazulite Studio 当前产品采用后的原标注细项另见主比较报告。

## 原生失败

| 歌曲 | 条件 | 首个阻断错误 |
| --- | --- | --- |
| s01 | 无时间正文＋Demucs | ValueError: 无法转换日语读音：サァ |
| s01 | 人工行时间＋Demucs | ValueError: Skipping 'line_026': G2P failed: "Script token 'ぃ' not found in script-to-phoneme dict." |
| s01 | 无时间正文＋BS Karaoke | ValueError: 无法转换日语读音：サァ |
| s15 | 无时间正文＋Demucs | ValueError: 第 35 行未找到可用的歌词发音证据，请检查歌词或提供逐句时间。 |
| s02 | 无时间正文＋Demucs | ValueError: 第 40 行有无法安全分段的过长单元，请提供逐句时间。 |
| s02 | 人工行时间＋Demucs | KeyError: "Script token '*' not found in script-to-phoneme dict." |
| s02 | 无时间正文＋BS Karaoke | ValueError: 第 40 行有无法安全分段的过长单元，请提供逐句时间。 |
| s03 | 无时间正文＋Demucs | ValueError: 无法转换日语读音：* |
| s03 | 人工行时间＋Demucs | KeyError: "Script token '*' not found in script-to-phoneme dict." |
| s03 | 无时间正文＋BS Karaoke | ValueError: 无法转换日语读音：* |
| s04 | 无时间正文＋Demucs | ValueError: 第 40 行有无法安全分段的过长单元，请提供逐句时间。 |
| s04 | 人工行时间＋Demucs | KeyError: "Script token '*' not found in script-to-phoneme dict." |
| s04 | 无时间正文＋BS Karaoke | KeyError: "Script token '*' not found in script-to-phoneme dict." |
| s05 | 无时间正文＋Demucs | ValueError: 无法转换日语读音：隱 |
| s05 | 人工行时间＋Demucs | KeyError: "Script token '*' not found in script-to-phoneme dict." |
| s05 | 无时间正文＋BS Karaoke | ValueError: 无法转换日语读音：隱 |
| s07 | 无时间正文＋Demucs | ValueError: 第 35 行未找到可用的歌词发音证据，请检查歌词或提供逐句时间。 |
| s07 | 人工行时间＋Demucs | KeyError: "Script token '*' not found in script-to-phoneme dict." |
| s07 | 无时间正文＋BS Karaoke | ValueError: 第 1 行有无法安全分段的过长单元，请提供逐句时间。 |
| s09 | 无时间正文＋Demucs | ValueError: 无法转换日语读音：* |
| s09 | 人工行时间＋Demucs | KeyError: "Script token '*' not found in script-to-phoneme dict." |
| s09 | 无时间正文＋BS Karaoke | ValueError: 无法转换日语读音：* |

完整调用栈与成功输出见[逐曲目录](../results/timing/timing)。这些失败保留原生行为；输入读音、定位窗口或显示映射的拒绝都会影响完整链路覆盖率。

## 固定读音与人工窗口

只选可编译的纯假名配对单元，NextFire 与 TIFA 使用相同 Demucs 人声、人工读音和人工行窗口。这项实验排除了自动读音和粗定位的差异，不能直接代表无人工时间输入的完整流程。

| 条件 | 分母 | 100 ms 命中 | 200 ms 命中 | 起／止 MAE ms | 起／止绝对误差 P95 ms | 缺失 | >1 秒 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nextfire | 5021 | 4017（80.00%） | 4658（92.77%） | 50.22 / 62.63 | 146.00 / 211.00 | 0 | 25 |
| tifa | 5021 | 4186（83.37%） | 4807（95.74%） | 49.13 / 58.29 | 113.00 / 155.00 | 0 | 15 |

## 预测窗口内的 TIFA 细化

细化窗口从首轮预测生成；无有效候选或未通过接受检查时保留首轮输出。实际窗口和采用决定分别保存在协议与指标中。

| 条件 | 分母 | 100 ms 命中 | 200 ms 命中 | 起／止 MAE ms | 起／止绝对误差 P95 ms | 缺失 | >1 秒 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 5021 | 4260（84.84%） | 4711（93.83%） | 48.32 / 58.39 | 124.58 / 186.49 | 7 | 42 |
| hybrid | 5021 | 4054（80.74%） | 4716（93.93%） | 62.26 / 71.48 | 126.32 / 194.87 | 3 | 40 |

## 复核与语种补测

[完整链路指标](../results/timing/metrics.json)、[共同文本边界](../results/timing/paired-common-units.json)、[固定窗口指标](../results/timing/controlled-metrics.json)与[细化采用记录](../results/timing/hybrid-metrics.json)保存本轮结果。日粤混合与潮汕话标注不进入日语主组。人工窗口下的原生粤语补测见[粤语指标](../results/timing/yue-native-metrics.json)；英语诊断见[英语指标](../results/timing/english-metrics.json)。
