# 人声分离配置与歌词对齐

实验比较十种人声分离配置，评价 GPU 五曲整曲、CPU 固定 30 秒片段的推理成本与固定歌词对齐效果。配置由权重、实现和推理设置共同确定；相同架构的不同权重分别列项。模型下载地址与哈希见[模型清单](../configs/separation-models.json)，源码版本见[源码清单](../configs/sources.json)与[八路线源码清单](../configs/comparison-sources.json)。

| 配置 | 固定权重／实现 | 比较定位 |
| --- | --- | --- |
| Demucs htdemucs | Lazulite 适配器 | 产品默认与速度基线 |
| SCNet Small | MSST，musdb18 checkpoint | 小模型的实际计算成本 |
| DTTNet | MSST，vocalsg32 ep4082 | 专用人声模型 |
| BS-RoFormer viperx | MSST，ep_317_sdr_12.9755 | 人声保留与对齐效果 |
| MelBand RoFormer Kim | MSST，KimberleyJSN MelBandRoformer | 频带结构与权重配置 |
| Windowed RoFormer | 作者实现，mbr-win10-sink8 | 局部注意力与无重叠推理 |
| BS Karaoke | Timing，frazer/becruily | 主唱提取，供 Timing 与 FA-Kara 使用 |
| MDX-Net Inst HQ 3 | SUG，UVR-MDX-NET-Inst_HQ_3 | 八路线中的 ONNX 分离配置 |
| MelBand RoFormer ep_3005 | MiliKara，ep_3005_sdr_11.4360 | MiliKara 原生默认权重 |
| HybridDemucs MUSDB Plus | yohane，HDEMUCS_HIGH_MUSDB_PLUS | yohane 原生分离配置 |

MiliKara 的 MelBand RoFormer 与 Kim 使用不同权重；yohane 的 HybridDemucs 与 htdemucs 也分别评价。Timing 的 Kim Vocals 与表中 Kim 使用相同权重，其封装成本保留在[单曲入口资源报告](resources.md)，不增加为第十一种配置。

## 统一评价条件

GPU 资源实验采用固定五曲整曲，每曲预热后三次重复；CPU 使用《Rainbow Flower》30–60 秒片段，预热后三次重复。输入统一为 44.1 kHz 双声道，有效 batch=1，使用 8 个计算线程；保留分块、重叠和归一化设置。推理计时包括设备搬运与返回 CPU，解码、加载和写盘在计时外。完整指标和统计口径见[资源性能](separation-performance.md)。

下游实验使用 GPU 分离结果、12 首日语歌曲和相同人工读音、NextFire、标准 CTC（Connectionist Temporal Classification，连接时序分类）；CTC 将逐帧发音标签概率与已知读音对应，得到时间边界。两条保存路径分别为浮点读取、PCM24（24 位音频采样）保存后读回，每条路径评价完整人声、核心活动区间拼接和带缓冲拼接。原生分离输出的采样率与保存语义保留，再进入统一下游处理。s13 潮汕话假名结果单列。

资源记录、人声和预测按输入、模型与配置身份核验复用，数据来源保留于[核验清单](../results/separation-alignment/reuse-audit.json)及同目录各配置的人声清单。原始对齐日志中的并行耗时不用于速度排名。

## 下游发现

在浮点读取、核心区间拼接条件下，BS Karaoke 的双端 100 ms 命中率为 85.83%，Demucs 为 83.89%，MiliKara 的 MelBand 为 84.47%，SUG 的 MDX-Net 为 82.57%，yohane 的 HybridDemucs 为 81.32%。分母均为 5370 个日语叶级单元，即标注树中不再细分的最小定时对象；双端命中要求起止两端同时落在阈值内。全部六十个条件及逐曲指标见[分离与下游对齐](separation-alignment.md)。

本组数据中，Demucs 的五曲 GPU 推理合计为 15.67 秒，可作为计算成本较低的基线；BS Karaoke 为 114.00 秒，在上述下游条件下获得更高的双端命中率。yohane 的分离最快（7.87 秒），但相同条件下命中率为 81.32%；选择时应同时考察速度、缺失和逐曲结果。

测试音频没有配套干净人声真值；本实验以人工歌词时间评价下游端点，并保存活动分析、缺失和大误差。这些结果反映分离配置对歌词工作流的影响。产品原生对齐、采用与导出的整体效果见[八路线比较](comparison.md)。
