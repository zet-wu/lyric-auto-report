# 六种人声分离模型的资源实测

使用固定五首歌曲，每首每个模型先预热，再完成三次 GPU 分离。表中耗时与能量先逐曲取三次的中位数，再对五曲求和；内存与显存取全部运行中的峰值。全部测量在质量实验结束后串行执行。

RSS（Resident Set Size，驻留集大小）是进程驻留在物理内存中的容量；这里统计进程树 RSS 之和，共享页可能重复计入。CUDA allocated 表示框架张量分配。

| 模型 | 五曲 GPU 分离 s | CUDA allocated 峰值 GiB | 进程树 RSS 峰值 GiB | 板卡能量 kJ |
| --- | --- | --- | --- | --- |
| Demucs htdemucs | 15.67 | 1.64 | 1.96 | 3.20 |
| SCNet Small | 38.31 | 1.50 | 2.63 | 7.13 |
| DTTNet | 24.67 | 0.93 | 2.10 | 6.79 |
| BS-RoFormer | 73.53 | 1.49 | 2.17 | 28.16 |
| MelBand RoFormer | 38.57 | 1.73 | 2.10 | 13.35 |
| Windowed RoFormer | 19.13 | 1.39 | 14.90 | 6.39 |

## 配置与计时

计时覆盖输入搬运、模型计算与结果回到 CPU；解码、模型加载和写盘不计入分离耗时。每轮固定随机种子 0，使用 8 个 Torch 线程、batch=1，保留各模型的分块、重叠和归一化设置。每首先用最多 30 秒的片段预热。板卡功率按约 20 ms 间隔采样并积分，包含空闲功耗。

| 模型 | 参数量／百万 | Torch |
| --- | --- | --- |
| Demucs htdemucs | 41.984 | 2.14.0+cu130 |
| SCNet Small | 10.579 | 2.14.0+cu130 |
| DTTNet | 4.958 | 2.14.0+cu130 |
| BS-RoFormer | 159.758 | 2.14.0+cu130 |
| MelBand RoFormer | 228.203 | 2.14.0+cu130 |
| Windowed RoFormer | 228.387 | 2.14.0+cu130 |

模型实际配置与加载后的状态哈希、逐次耗时、显存、RSS、能量及输入身份保存于[原始记录](../results/separation-resources)。五曲清单见[输入配置](../configs/separation-resources-inputs.json)。本轮资源报告仅包含 GPU 测量。端点质量另见[分离与下游对齐](separation-alignment.md)。
