# 人声分离模型选择

人声分离直接影响歌词对齐所能利用的演唱信息。本仓库围绕三个问题选择候选：处理整首歌需要多少时间和内存，演唱是否完整保留，以及分离结果能否改善后续歌词端点。

候选覆盖 Demucs、SCNet Small、DTTNet、BS-RoFormer、MelBand RoFormer 和 Windowed RoFormer。Timing 链路另使用 BS Karaoke 与 Kim Vocals。每个名称对应具体权重和推理配置；下载地址、哈希及源码版本分别列在 [模型清单](../configs/separation-models.json) 和 [源码清单](../configs/sources.json)。

| 候选 | 比较目的 | 固定实现 |
| --- | --- | --- |
| Demucs htdemucs | 产品默认后端与速度基线 | Lazulite 适配器 |
| SCNet Small | 检验小权重是否降低实际计算成本 | MSST |
| DTTNet vocals | 检验专用人声模型的显存与速度 | MSST |
| BS-RoFormer viperx | 检验人声保留与下游端点收益 | MSST |
| MelBand RoFormer | 检验频带结构及发布权重的下游表现 | MSST |
| Windowed RoFormer | 检验局部注意力与无重叠推理的成本 | 作者实现 |
| BS Karaoke | 复现 Timing 的主唱提取链路 | Timing |
| Kim Vocals | 分离输出对照 | Timing |

Kim Vocals 与表中的 MelBand RoFormer 使用相同权重，分别通过 Timing 和 MSST 的推理配置运行，作为两条推理路径记录。BS Karaoke 与 viperx BS-RoFormer 使用不同权重。

Lazulite 的分离输出经过人声活动分析、音频拼接和强制对齐。歌曲中的弱唱、长音与背景演唱会影响活动边界，因此分离质量需要结合目标工作流判断。分离器输出相同声道数、采样率和长度，能够让比较集中于人声内容；推理时保留各权重发布的分块和重叠设置。

六模型本轮资源测试见[性能报告](separation-performance.md)。当前测试集的下游对齐重跑结果与分离配置一起发布。音频没有配套干净人声真值，本仓库用人工歌词时间评价下游端点，并记录活动覆盖和缺失；这些指标回答歌词工作流问题。

源码入口：[Lazulite](https://github.com/wuchenyanmo/Lazulite)、[MSST](https://github.com/ZFTurbo/Music-Source-Separation-Training)、[Windowed RoFormer](https://github.com/smulelabs/windowed-roformer)、[Timing](https://github.com/Zennmn/Timing)。
