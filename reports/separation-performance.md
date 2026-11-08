# 六种人声分离模型的资源实测

Demucs htdemucs 在这组实测中耗时最低；DTTNet 的 CUDA 张量分配峰值最低。五首歌共 1462.551 秒，每首完成三次热运行，表中耗时为逐曲中位数之和。

本表保留已有性能实测。实验音频已随仓库提供，身份见[输入清单](../historical/separation/inputs.json)，逐次测量与汇总见[数据目录](../historical/separation/)。当前测试集的对齐成绩另行重跑和报告。

| 模型 | 五曲 GPU 分离 / 秒 | CUDA allocated 峰值 / GiB | 进程树 RSS 峰值 / GiB | 板卡能量 / kJ | 30 秒片段 CPU 耗时 / 秒 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Demucs htdemucs | 13.55 | 1.64 | 1.90 | 2.61 | 7.96 |
| SCNet Small | 28.91 | 1.50 | 2.71 | 5.85 | 35.12 |
| DTTNet | 21.63 | 0.93 | 2.17 | 6.02 | 70.45 |
| BS-RoFormer | 71.26 | 1.49 | 1.94 | 26.75 | 275.99 |
| MelBand RoFormer | 35.25 | 1.73 | 2.00 | 12.15 | 100.14 |
| Windowed RoFormer | 18.30 | 1.39 | 15.89 | 5.66 | 59.04 |

## 配置与计时

主机为 Linux、AMD EPYC 7502，推理固定 8 线程、不绑核。GPU 报告为 RTX 4090，容量 49140 MiB，驱动 595.58.03；分离环境为 Torch 2.14.1+cu130。具体硬件记录见 [hardware.json](../historical/separation/hardware.json)。

GPU 计时覆盖输入搬运、模型计算和结果回 CPU。解码、权重加载、写盘和活动分析单独记录。所有模型 batch=1，每轮随机种子为 0。CPU 使用 Rainbow Flower 原混音的 [30,60) 秒，FP32、8 线程，统计三次热运行的中位数。

| 模型 | 参数 / M | 权重 / MiB | GPU 精度 | 分块 / 秒 | 重叠 |
| --- | ---: | ---: | --- | ---: | ---: |
| Demucs | 41.984 | 80.2 | FP32 | 7.8 | 25% |
| SCNet Small | 10.579 | 40.5 | AMP FP16 | 11 | 75% |
| DTTNet | 4.958 | 19.1 | AMP FP16 | 5.921 | 75% |
| BS-RoFormer | 159.758 | 609.7 | AMP FP16 | 8 | 50% |
| MelBand RoFormer | 228.203 | 870.8 | AMP FP16 | 8 | 50% |
| Windowed RoFormer | 228.387 | 871.5 | AMP FP16 | 8 | 0% |

这些配置对应发布权重的实际推理方式。DTTNet 比 Demucs 少约 43.5% 的 CUDA allocated 峰值，耗时约为其 1.60 倍。Windowed 的耗时约为普通 MelBand 的 52%，两者同时存在重叠策略差异。

## 读数解释

CUDA allocated 记录框架张量分配；RSS 为进程树 RSS 之和，共享页可能重复计入。峰值监测覆盖分离阶段，不能用于推算含导入和加载阶段的最低内存。板卡能量由 NVML 整卡功率积分得到，包含空闲功耗。CPU 表仅对应指定片段。

这组资源结果支持以 Demucs 为速度基线，同时把 DTTNet 作为显存取舍候选。分离质量和对齐端点需要通过当前测试集的独立结果判断。
